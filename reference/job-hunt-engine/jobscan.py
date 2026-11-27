"""Sayandip's job scanner.

Reads official company job boards (Greenhouse, Lever, Ashby, SmartRecruiters, Workday,
Oracle HCM, Amazon, Microsoft, Google, Atlassian), keeps entry-level software roles in
Bengaluru / Hyderabad / Kolkata / remote-India, scores them, and records which ones are new.

Usage:  python jobscan.py            # scan, write out/scan_<date>.md and update data/
        python jobscan.py --all      # also list matches already seen before
Only the Python standard library is used.
"""
import concurrent.futures as cf
import datetime as dt
import html
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "out")
os.makedirs(DATA, exist_ok=True)
os.makedirs(OUT, exist_ok=True)
TODAY = dt.date.today().isoformat()
UA = {"User-Agent": "Mozilla/5.0 (personal job scanner)", "Accept": "application/json"}
ERRORS = []

# ---------------------------------------------------------------- filters
PREF_CITY = re.compile(r"bengaluru|bangalore|hyderabad|kolkata|calcutta", re.I)
INDIA = re.compile(r"\bindia\b|\bIND\b|\bIN\b", re.I)
REMOTE = re.compile(r"remote|anywhere|work from home|wfh", re.I)
OTHER_IN_CITY = re.compile(r"pune|gurgaon|gurugram|noida|delhi|mumbai|chennai|ahmedabad|mohali|chandigarh|jaipur|kochi|coimbatore|indore|trivandrum|thiruvananthapuram|vadodara|nagpur|bhubaneswar|mysore|mysuru|vizag|visakhapatnam", re.I)

TECH = re.compile(r"software|\bsde\b|\bswe\b|developer|engineer|engineering|programmer|member of technical staff|\bmts\b|full[ -]?stack|backend|back-end|frontend|front-end|\bml\b|machine learning|\bai\b|data scientist", re.I)
NON_TECH = re.compile(
    r"sales|account (exec|manager|director)|marketing|recruit|talent|\bhr\b|human resources|people partner|legal|counsel|paralegal|"
    r"finance|accountant|accounting|payroll|tax\b|audit|treasury|customer success|customer support|support engineer|technical support|"
    r"\bsupport\b|technician|designer|product manager|program manager|project manager|business analyst|operations|\bops\b|"
    r"solutions? engineer|sales engineer|pre-?sales|consultant|partner manager|evangelist|advocate|writer|content|"
    r"hardware|asic|analog|\brtl\b|verification|physical design|layout|mechanical|electrical|firmware|embedded|validation|silicon|"
    r"circuit|\bdft\b|\bsoc\b|fpga|board|signal integrity|test engineer|\bqa\b|quality|sdet|automation test|manual test|"
    r"network engineer|field engineer|data center|facilities|procurement|supply chain|logistics|compliance|risk analyst|"
    r"trust and safety|policy|insurance|actuar|clinical|medical|pharma|lawyer|executive assistant|administrator|"
    r"delivery manager|scrum|implementation|onboarding|customer engineer|escalation|service desk|helpdesk|"
    r"technical services|services engineer|people systems|economist|reliability engineer \(cre\)|customer reliability|\badmin\b|"
    r"integration developer|boomi|\bgtm\b|research specialist|user research|network operation|\bmgr\b|salesforce developer|"
    r"servicenow developer|\bsap\b|\berp\b|\bcrm\b|desktop|systems administrator|it engineer", re.I)
NOT_HIS_FOCUS = re.compile(r"front[- ]?end|full[- ]?stack|fullstack|\bui\b|web developer|react native|\breact\b|angular|\bvue\b|"
                           r"mobile|android|\bios\b|flutter|\bswift\b|kotlin|\bgame\b|unity developer|designer", re.I)
# his focus (21 Nov 2026): SDE roles first (Java / Spring Boot backend), then DevOps / cloud / platform, plus GenAI
FOCUS = re.compile(r"\bsde\b|\bswe\b|software (development )?engineer|software developer|member of technical staff|\bmts\b|"
                   r"\bjava\b|spring|backend|back-end|devops|\bsre\b|site reliability|cloud|platform|infrastructure|\binfra\b|"
                   r"kubernetes|\bk8s\b|microservice|distributed|gen ?ai|generative|\bllm\b|\bai engineer|applied ai|agent", re.I)
SENIOR = re.compile(
    r"\b(senior|sr\.?|staff|principal|lead|leader|manager|director|head|architect|vp|vice president|distinguished|fellow|chief|expert)\b|"
    r"\b(ii|iii|iv)\b|\b(sde|swe|engineer|developer|mts)\s*[-–]?\s*(2|3|4|5)\b|\bl[4-9]\b|\bic[3-9]\b|\bp[4-9]0\b|"
    r"\bsmts\b|\blmts\b|\bpmts\b|\bexperienced\b|\bintermediate\b|\bmgr\b|mid[- ]level", re.I)
NEWGRAD = re.compile(r"new grad|university|graduate|campus|fresher|early career|early-career|entry[ -]level|\b2027\b|class of 2027|"
                     r"recent grad|\b0\s*[-–to]+\s*[12]\s*(years|yrs)|\bsde[ -]?1\b|\bsde[ -]?i\b|engineer\s*[-–]?\s*(1|i)\b|\bic[12]\b|associate (software )?engineer", re.I)
INTERN = re.compile(r"\binterns?(hip)?\b|apprentice|trainee", re.I)
EXP = re.compile(r"(\d{1,2})\s*\+?\s*(?:[-–]|to)?\s*(\d{1,2})?\s*\+?\s*(?:years|yrs)", re.I)
SKILLS = ["java", "spring", "microservices", "python", "typescript", "javascript", "react", "next.js", "node", "fastapi", "sql", "postgres", "redis",
          "docker", "kubernetes", "aws", "gcp", "terraform", "jenkins", "machine learning", "pytorch", "llm", "distributed"]


def clean(text):
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def loc_class(loc):
    """Return 'pref', 'remote-india', or None (reject)."""
    if PREF_CITY.search(loc):
        return "pref"
    india = bool(INDIA.search(loc)) or bool(OTHER_IN_CITY.search(loc))
    if REMOTE.search(loc) and india:
        return "remote-india"
    if re.fullmatch(r"\s*india\s*", loc, re.I):
        return "remote-india"  # country-only posting, usually flexible or multi-city
    return None


def title_ok(title):
    if not TECH.search(title) or NON_TECH.search(title) or NOT_HIS_FOCUS.search(title):
        return False
    if SENIOR.search(title) and not NEWGRAD.search(title):
        return False
    return True


def min_years(desc):
    """Smallest 'N years' figure mentioned near the word experience, or None."""
    best = None
    for m in EXP.finditer(desc or ""):
        ctx = desc[max(0, m.start() - 80): m.end() + 80].lower()
        if "experience" not in ctx and "exp" not in ctx:
            continue
        n = int(m.group(1))
        if n > 15:
            continue
        best = n if best is None else min(best, n)
    return best


# ---------------------------------------------------------------- http
def fetch(url, body=None, headers=None, raw=False, tries=2):
    h = dict(UA)
    h.update(headers or {})
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        h["Content-Type"] = "application/json"
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers=h)
            with urllib.request.urlopen(req, timeout=30) as r:
                txt = r.read().decode("utf-8", "ignore")
                return txt if raw else json.loads(txt)
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 429:
                time.sleep(6 * (i + 1))
                continue
            raise
        except Exception as e:  # network hiccup
            last = e
            time.sleep(2)
    raise last


def job(src, jid, title, loc, url, posted="", desc="", extra=None):
    d = {"key": f"{src['ats']}:{src.get('slug') or src.get('tenant') or src['name']}:{jid}", "company": src["name"],
         "tier": src["tier"], "ats": src["ats"], "title": clean(title), "location": clean(loc), "url": url,
         "posted": (posted or "")[:10], "desc": desc}
    d.update(extra or {})
    return d


# ---------------------------------------------------------------- sources
def s_greenhouse(src):
    d = fetch(f"https://boards-api.greenhouse.io/v1/boards/{src['slug']}/jobs")
    out = []
    for j in d.get("jobs", []):
        out.append(job(src, j["id"], j["title"], (j.get("location") or {}).get("name", ""), j["absolute_url"], j.get("updated_at", "")))
    return out


def d_greenhouse(src, j):
    jid = j["key"].rsplit(":", 1)[1]
    d = fetch(f"https://boards-api.greenhouse.io/v1/boards/{src['slug']}/jobs/{jid}")
    return clean(d.get("content", ""))


def s_lever(src):
    d = fetch(f"https://api.lever.co/v0/postings/{src['slug']}?mode=json")
    out = []
    for j in d:
        cat = j.get("categories", {}) or {}
        locs = [cat.get("location", "")] + (cat.get("allLocations") or [])
        if j.get("workplaceType") == "remote":
            locs.append("Remote " + str(j.get("country", "")))
        desc = clean(j.get("descriptionPlain", "") + " " + " ".join(clean(l.get("content", "")) for l in j.get("lists", [])))
        posted = dt.datetime.fromtimestamp(j.get("createdAt", 0) / 1000).date().isoformat() if j.get("createdAt") else ""
        out.append(job(src, j["id"], j["text"], " / ".join(x for x in locs if x), j["hostedUrl"], posted, desc,
                       {"commitment": cat.get("commitment", "")}))
    return out


def s_ashby(src):
    d = fetch(f"https://api.ashbyhq.com/posting-api/job-board/{src['slug']}?includeCompensation=true")
    out = []
    for j in d.get("jobs", []):
        locs = [j.get("location", "")] + [x.get("location", "") for x in j.get("secondaryLocations", []) or []]
        addr = (j.get("address") or {}).get("postalAddress") or {}
        locs.append(addr.get("addressCountry", ""))
        if j.get("isRemote"):
            locs.append("Remote")
        comp = (j.get("compensation") or {}).get("compensationTierSummary", "")
        out.append(job(src, j.get("id"), j["title"], " / ".join(x for x in locs if x), j.get("jobUrl"), j.get("publishedAt", ""),
                       clean(j.get("descriptionPlain") or j.get("descriptionHtml", "")), {"comp": comp, "commitment": j.get("employmentType", "")}))
    return out


def s_smartrecruiters(src):
    out, offset = [], 0
    while True:
        d = fetch(f"https://api.smartrecruiters.com/v1/companies/{src['slug']}/postings?country=in&limit=100&offset={offset}")
        for j in d.get("content", []):
            l = j.get("location", {}) or {}
            loc = ", ".join(x for x in [l.get("city"), l.get("region"), l.get("country")] if x) + (" Remote" if l.get("remote") else "")
            out.append(job(src, j["id"], j["name"], loc, f"https://jobs.smartrecruiters.com/{src['slug']}/{j['id']}", j.get("releasedDate", ""),
                           extra={"commitment": (j.get("typeOfEmployment") or {}).get("label", "")}))
        offset += 100
        if offset >= d.get("totalFound", 0) or offset > 500:
            return out


def d_smartrecruiters(src, j):
    jid = j["key"].rsplit(":", 1)[1]
    d = fetch(f"https://api.smartrecruiters.com/v1/companies/{src['slug']}/postings/{jid}")
    secs = (d.get("jobAd") or {}).get("sections", {})
    return clean(" ".join((secs.get(k) or {}).get("text", "") for k in ("jobDescription", "qualifications", "additionalInformation")))


WD_STATE = {"fails": 0}


def s_workday(src):
    if WD_STATE["fails"] >= 3:  # circuit breaker: Workday is throttling this network today
        ERRORS.append(f"{src['name']} (workday): skipped, Workday throttled this run")
        return []
    base = f"https://{src['tenant']}.{src['wd']}.myworkdayjobs.com"
    api = f"{base}/wday/cxs/{src['tenant']}/{src['site']}"
    out = []
    for q in ("software engineer India", "graduate India"):
        try:
            d = fetch(f"{api}/jobs", {"appliedFacets": {}, "limit": 20, "offset": 0, "searchText": q}, tries=1)
            WD_STATE["fails"] = 0
        except Exception as e:
            if "429" in str(e):
                WD_STATE["fails"] += 1
            ERRORS.append(f"{src['name']} (workday '{q}'): {str(e)[:60]}")
            break
        for j in d.get("jobPostings", []):
            path = j.get("externalPath", "")
            out.append(job(src, path.rsplit("_", 1)[-1] or path, j.get("title", ""), j.get("locationsText", ""),
                           f"{base}/{src['site']}{path}", j.get("postedOn", ""), extra={"wd_path": path}))
        time.sleep(3)
    uniq = {j["key"]: j for j in out}
    return list(uniq.values())


def d_workday(src, j):
    base = f"https://{src['tenant']}.{src['wd']}.myworkdayjobs.com"
    d = fetch(f"{base}/wday/cxs/{src['tenant']}/{src['site']}{j['wd_path']}", tries=1)
    info = d.get("jobPostingInfo", {})
    locs = [info.get("location", "")] + (info.get("additionalLocations") or [])
    j["location"] = clean(" / ".join(x for x in locs if x)) or j["location"]
    j["posted"] = (info.get("startDate") or j["posted"])[:10]
    time.sleep(2)
    return clean(info.get("jobDescription", ""))


def s_amazon(src):
    out = []
    for q in ("software development engineer", "software engineer", "university graduate"):
        url = ("https://www.amazon.jobs/en/search.json?" + urllib.parse.urlencode(
            {"base_query": q, "loc_query": "India", "country": "IND", "result_limit": 100, "sort": "recent"}))
        d = fetch(url)
        for j in d.get("jobs", []):
            desc = clean(j.get("basic_qualifications", "") + " " + j.get("preferred_qualifications", "") + " " + j.get("description_short", ""))
            out.append(job(src, j.get("id_icims") or j.get("id"), j["title"], f"{j.get('city', '')}, {j.get('country_code', '')}",
                           "https://www.amazon.jobs" + j.get("job_path", ""), j.get("posted_date", ""), desc))
    return list({j["key"]: j for j in out}.values())


def s_microsoft(src):
    out = []
    for start in (0, 10, 20, 30, 40):
        d = fetch("https://apply.careers.microsoft.com/api/pcsx/search?" + urllib.parse.urlencode(
            {"domain": "microsoft.com", "query": "software engineer", "location": "India", "start": start, "sort_by": "timestamp"}))
        pos = (d.get("data") or {}).get("positions", [])
        for p in pos:
            posted = dt.datetime.fromtimestamp(p.get("postedTs", 0)).date().isoformat() if p.get("postedTs") else ""
            out.append(job(src, p.get("displayJobId") or p.get("id"), p.get("name", ""), " / ".join(p.get("locations", [])),
                           f"https://apply.careers.microsoft.com/careers/job/{p.get('id')}", posted))
        if len(pos) < 10:
            break
    return out


def s_atlassian(src):
    d = fetch("https://www.atlassian.com/endpoint/careers/listings")
    out = []
    for j in d:
        locs = j.get("locations") or []
        out.append(job(src, j.get("id"), j.get("title", ""), " / ".join(locs),
                       (j.get("portalJobPost") or {}).get("portalUrl") or f"https://www.atlassian.com/company/careers/details/{j.get('id')}",
                       desc=clean(j.get("overview", "") + " " + j.get("responsibilities", "") + " " + j.get("qualifications", ""))))
    return out


def s_google(src):
    out = []
    for q in ("software engineer", "software developer"):
        url = ("https://www.google.com/about/careers/applications/jobs/results/?" + urllib.parse.urlencode(
            [("location", "Bangalore India"), ("location", "Hyderabad Telangana India"), ("location", "India"),
             ("target_level", "EARLY"), ("q", q)]))
        page = fetch(url, raw=True, headers={"Accept": "text/html"})
        links = list(re.finditer(r'href="jobs/results/(\d+)-([^"?]*)[^"]*"', page))
        prev = 0
        for m in links:
            chunk = page[prev:m.start()]
            prev = m.end()
            t = re.findall(r'<h3 class="QJPWVe">(.*?)</h3>', chunk)
            locs = re.findall(r">([^<>]{2,80}India[^<>]{0,40})<", chunk)
            if not t:
                continue
            out.append(job(src, m.group(1), t[-1], " / ".join(dict.fromkeys(locs)) or "India",
                           f"https://www.google.com/about/careers/applications/jobs/results/{m.group(1)}-{m.group(2)}"))
    return list({j["key"]: j for j in out}.values())


def s_oracle(src):
    url = (f"https://{src['host']}/hcmRestApi/resources/latest/recruitingCEJobRequisitions?onlyData=true&expand=requisitionList.secondaryLocations"
           f"&finder=findReqs;siteNumber={src['site']},limit=100,keyword=software%20engineer%20India,sortBy=POSTING_DATES_DESC")
    d = fetch(url)
    out = []
    for item in d.get("items", []):
        for r in item.get("requisitionList", []):
            locs = [r.get("PrimaryLocation", "")] + [x.get("Name", "") for x in r.get("secondaryLocations", []) or []]
            out.append(job(src, r.get("Id"), r.get("Title", ""), " / ".join(x for x in locs if x), src["joburl"].format(id=r.get("Id")),
                           r.get("PostedDate", ""), clean(r.get("ShortDescriptionStr", ""))))
    return out


def s_workable(src):
    d = fetch(f"https://apply.workable.com/api/v1/widget/accounts/{src['slug']}")
    out = []
    for j in d.get("jobs", []):
        locs = [", ".join(x for x in [j.get("city"), j.get("state"), j.get("country")] if x)]
        locs += [", ".join(x for x in [l.get("city"), l.get("region"), l.get("country")] if x) for l in j.get("locations") or []]
        if j.get("telecommuting"):
            locs.append("Remote " + str(j.get("country", "")))
        out.append(job(src, j.get("shortcode"), j.get("title", ""), " / ".join(x for x in locs if x),
                       j.get("url") or f"https://apply.workable.com/{src['slug']}/j/{j.get('shortcode')}/", j.get("published_on", ""),
                       extra={"commitment": j.get("employment_type", "")}))
    return out


def s_recruitee(src):
    d = fetch(f"https://{src['slug']}.recruitee.com/api/offers/")
    out = []
    for j in d.get("offers", []):
        loc = " / ".join(x for x in [j.get("location"), j.get("city"), j.get("country")] if x) + (" Remote" if j.get("remote") else "")
        out.append(job(src, j.get("id"), j.get("title", ""), loc, j.get("careers_url", ""), j.get("published_at", ""),
                       clean(j.get("description", "") + " " + j.get("requirements", "")), {"commitment": j.get("employment_type_code", "")}))
    return out


SOURCES = {"greenhouse": s_greenhouse, "lever": s_lever, "ashby": s_ashby, "smartrecruiters": s_smartrecruiters, "workday": s_workday,
           "amazon": s_amazon, "microsoft": s_microsoft, "atlassian": s_atlassian, "google": s_google, "oracle": s_oracle,
           "workable": s_workable, "recruitee": s_recruitee}
DETAILS = {"greenhouse": d_greenhouse, "smartrecruiters": d_smartrecruiters, "workday": d_workday}


# ---------------------------------------------------------------- pipeline
def collect(src):
    try:
        return SOURCES[src["ats"]](src)
    except Exception as e:
        ERRORS.append(f"{src['name']} ({src['ats']}): {str(e)[:80]}")
        return []


def score(j):
    s = {"A": 3, "B": 2, "C": 0.5}[j["tier"]]
    text = j["title"] + " " + j.get("desc", "")
    if NEWGRAD.search(j["title"]):
        s += 2.5
    elif NEWGRAD.search(j.get("desc", "")[:3000]):
        s += 1
    lc = j["location"].lower()
    s += 2 if ("bengaluru" in lc or "bangalore" in lc or "kolkata" in lc) else 1.5 if "hyderabad" in lc else 1
    y = j.get("min_years")
    if y is None or y == 0:
        s += 1
    elif y == 1:
        s += 0.3
    elif y == 2:
        s -= 1.5
    if FOCUS.search(j["title"]):
        s += 1.5
    elif FOCUS.search(j.get("desc", "")[:4000]):
        s += 0.5
    if re.search(r"spring", text, re.I):
        s += 0.5
    hits = [k for k in SKILLS if k in text.lower()]
    j["skill_hits"] = hits[:8]
    s += min(len(hits), 6) * 0.25
    if j.get("type") == "internship":
        s -= 0.5
    return round(s, 2)


def main():
    show_all = "--all" in sys.argv
    cfg = json.load(open(os.path.join(HERE, "companies.json"), encoding="utf-8"))
    srcs = cfg["sources"]
    by_name = {}
    t0 = time.time()

    fast = [s for s in srcs if s["ats"] != "workday"]
    slow = [s for s in srcs if s["ats"] == "workday"]
    raw = []
    with cf.ThreadPoolExecutor(16) as ex:
        for res in ex.map(collect, fast):
            raw.extend(res)
    for s in slow:  # Workday rate-limits hard: one tenant at a time
        raw.extend(collect(s))
        time.sleep(2)
    for s in srcs:
        by_name[(s["ats"], s.get("slug") or s.get("tenant") or s["name"], s["name"])] = s

    # first pass: title + location
    cand = []
    for j in raw:
        if not title_ok(j["title"]):
            continue
        if j["ats"] != "workday" and not loc_class(j["location"]):
            continue
        if j["ats"] == "workday" and not (loc_class(j["location"]) or "location" in j["location"].lower()):
            continue
        cand.append(j)

    # second pass: fetch descriptions where the list endpoint had none (bounded)
    seen = json.load(open(os.path.join(DATA, "seen.json"))) if os.path.exists(os.path.join(DATA, "seen.json")) else {}

    def src_of(j):
        for (ats, slug, name), s in by_name.items():
            if ats == j["ats"] and name == j["company"]:
                return s

    def enrich(j):
        if not j.get("desc") and j["ats"] in DETAILS and (j["key"] not in seen or show_all):
            try:
                j["desc"] = DETAILS[j["ats"]](src_of(j), j)
            except Exception as e:
                ERRORS.append(f"detail {j['company']}: {str(e)[:60]}")
        return j

    fast_c = [j for j in cand if j["ats"] != "workday"]
    slow_c = [j for j in cand if j["ats"] == "workday"]
    with cf.ThreadPoolExecutor(12) as ex:
        fast_c = list(ex.map(enrich, fast_c))
    slow_c = [enrich(j) for j in slow_c[:40]]

    matches = []
    for j in fast_c + slow_c:
        lc = loc_class(j["location"])
        if not lc:
            continue
        j["loc_class"] = lc
        j["min_years"] = min_years(j.get("desc", ""))
        if j["min_years"] is not None and j["min_years"] >= 3:
            continue
        j["type"] = "internship" if (INTERN.search(j["title"]) or "intern" in j.get("commitment", "").lower()) else "full-time"
        if j["type"] == "internship" or j["tier"] == "C":
            continue  # interning at Broadridge Jan-Jul 2027; only 20 LPA+ full-time roles
        j["score"] = score(j)
        matches.append(j)

    matches.sort(key=lambda x: -x["score"])
    for j in matches:
        j["stretch"] = bool(j["min_years"] is not None and j["min_years"] >= 2)
    new_all = [j for j in matches if j["key"] not in seen]
    new = [j for j in new_all if not j["stretch"]]
    stretch = [j for j in new_all if j["stretch"]]
    for j in matches:
        seen.setdefault(j["key"], TODAY)
    json.dump(seen, open(os.path.join(DATA, "seen.json"), "w"), indent=0)

    # jobs.json keeps every match ever found plus status set by the daily review
    db_path = os.path.join(DATA, "jobs.json")
    db = json.load(open(db_path, encoding="utf-8")) if os.path.exists(db_path) else {}
    for j in matches:
        rec = db.get(j["key"], {"status": "new", "first_seen": TODAY})
        rec.update({k: j.get(k) for k in ("company", "tier", "title", "location", "url", "posted", "score", "min_years", "type",
                                            "skill_hits", "comp", "loc_class", "stretch")})
        rec["last_seen"] = TODAY
        db[j["key"]] = rec
    json.dump(db, open(db_path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)

    # report
    lines = [f"# Job scan {TODAY}", "",
             f"Sources scanned: {len(srcs)} | postings read: {len(raw)} | entry-level matches: {len(matches)} | NEW today: {len(new)} (+{len(stretch)} stretch) | {time.time() - t0:.0f}s", ""]
    for title, rows in (("NEW matches", new), ("Stretch: new roles asking ~2 years (lower odds)", stretch), ("All current matches", matches if show_all else [])):
        if not rows:
            continue
        lines += [f"## {title}", "", "| # | Score | Company (tier) | Role | Location | Exp asked | Type | Posted | Link |", "|---|---|---|---|---|---|---|---|---|"]
        for i, j in enumerate(rows, 1):
            yrs = "-" if j["min_years"] is None else f"{j['min_years']}+ yrs"
            lines.append(f"| {i} | {j['score']} | {j['company']} ({j['tier']}) | {j['title']} | {j['location'][:60]} | {yrs} | {j['type']} | {j['posted']} | [apply]({j['url']}) |")
        lines.append("")
    if ERRORS:
        lines += ["## Sources that failed this run", ""] + [f"- {e}" for e in ERRORS[:40]]
    rep = os.path.join(OUT, f"scan_{TODAY}.md")
    open(rep, "w", encoding="utf-8").write("\n".join(lines))
    json.dump(new + stretch, open(os.path.join(OUT, f"new_{TODAY}.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("\n".join(lines[:4]))
    print(f"report: {rep}")
    print(f"errors: {len(ERRORS)}")


if __name__ == "__main__":
    main()
