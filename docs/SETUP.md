# Setup: what Sayandip does, and when

Claude cannot sign up for accounts, type passwords or OTPs, solve CAPTCHAs, pay, or do KYC. Every item below is yours; Claude asks for each one only when the work reaches it and tells you exactly what to click or type.

**Keys never go into chat.** Copy `.env.example` to `.env` and fill it in yourself, or run `gh secret set NAME` in your own terminal (it asks for the value privately). Claude is blocked from reading `.env`.

**Already on this PC (checked 24 Nov 2026):** Git with Git LFS, GitHub CLI, Node 24 and pnpm, Docker Desktop (on WSL 2, capped at 6 GB by your `.wslconfig`, which suits this laptop), kubectl, Helm, Terraform, Python, VS Code, Java (JDKs 8, 17, 20, 21 and 23), Android Studio with the Android SDK (API 33-36, emulator, adb), and Blender 5.3 with the Blender Lab MCP extension. Nothing big to install.

## Java on this PC: leave it exactly as it is
Hadoop 3.2.4 and Hive 3.1.2 are pinned to Java 8 inside Hadoop's own config (`hadoop-env.cmd`). Spark 3.5.8, Kafka 3.4.0 and Cassandra 3.11.0 use your user-level JAVA_HOME, which already points to Java 21 (`C:\Users\Sayan\.jdks\temurin-21`). This project never changes JAVA_HOME or PATH and never installs a system-wide JDK: the backend downloads its own Java 25 through Gradle (kept in `C:\Users\Sayan\.gradle\jdks`), and Android builds point at JDK 17 for that one command only. Your big-data tools are unaffected.

Cassandra 3.11 cannot start on Java 21 (its startup flags use garbage collectors that newer Java removed), so on 24 Nov 2026 it was pinned to Java 8 in its own launchers, the way Hadoop is: `C:\cassandra\bin\cassandra.bat` and `cassandra.in.bat` (used by nodetool and the sstable tools) now set `JAVA_HOME=C:\Java\jdk1.8.0_481`. The originals are kept as `*.bak-before-java8-pin`. Verified: Java 8 starts with all 15 of Cassandra's JVM options; Java 21 refuses them.

## Do now (before or during Phase 0): about 30 minutes, ₹0
| # | What | Why |
|---|---|---|
| 1 | Sign in the GitHub CLI | Claude creates the private repo, pull requests and CI |
| 2 | Nothing to do for Java | See the section above |
| 3 | Docker Desktop starts with Windows (currently off) | Local Postgres and Redis, and the integration tests |
| 4 | One Android emulator, **or** USB debugging on your phone | Claude installs and tests the app itself |
| 5 | Blender ready | 3D assets for the hero demo |
| 6 | GitHub Student Developer Pack: **done**, benefits active until 10 Feb 2028 | GitHub Pro (unlimited private repos, more CI minutes), Copilot, partner offers such as Azure for Students; the new chat checks the offers page when choosing hosting and the domain |
| 7 | Cloudflare account | DNS, CDN, bot protection, file storage, email forwarding |
| 8 | Expo account | Cloud builds of the app later; reserves your name |
| 9 | Read your Broadridge contract | Outside-work and IP clauses decide how we run this project |

### Step by step
**1. GitHub CLI**
1. Open PowerShell and run `gh auth login`.
2. Choose: GitHub.com, then HTTPS, then Yes (authenticate Git with your GitHub credentials), then "Login with a web browser".
3. Copy the 8-character code it shows and press Enter; in the browser page that opens (github.com/login/device), paste the code and click Authorize.
4. Check with `gh auth status`: it should say you're logged in as Sayandip-Jana-1018.

**3. Docker Desktop**
1. Open Docker Desktop and click the gear icon (Settings) at the top right.
2. General: tick "Start Docker Desktop when you sign in to your computer". Apply.
3. Check with `docker run --rm hello-world`: it prints "Hello from Docker!".

**4. Emulator or phone** (do the phone if you can; the emulator is the fallback)
- *Phone:* Settings, About phone, tap Build number 7 times (Samsung: About phone, Software information, Build number; Xiaomi/Redmi/POCO: tap OS version; OnePlus/Realme/OPPO: About device, Version, Build number) and enter your PIN. Then Developer options (under System or Additional settings): turn on USB debugging (Xiaomi: also "Install via USB"). Plug in with a data cable and tap Allow on "Allow USB debugging?", ticking "Always allow from this computer". Check: `& "$env:LOCALAPPDATA\Android\Sdk\platform-tools\adb.exe" devices` lists the phone as "device".
- *Emulator:* Android Studio, More Actions, Virtual Device Manager (inside a project: View, Tool Windows, Device Manager). Click +, choose Phone, Pixel 8 (or Medium Phone), Next. Download the API 36 (Android 16) x86_64 image with Google Play or Google APIs, accept the licence, Next, Finish. Press the play button to boot it once. If it complains about hardware acceleration: Windows search "Turn Windows features on or off", tick "Windows Hypervisor Platform", OK, restart.

**5. Blender**
1. Open Blender 5.3; Edit, Preferences, Add-ons; search "MCP". You have two copies (one from Blender Lab, one under "user default"): keep the Blender Lab one ticked and untick the other.
2. When the new chat asks, keep Blender open and, if the extension shows a connect or start button, press it. Claude checks the link by reading the scene. For scripted builds and renders the connector can also run Blender in the background.

**6. GitHub Student Developer Pack** (done: verified on 10 Feb 2026, benefits until 10 Feb 2028; steps kept for reference)
1. Add your LPU email to GitHub (github.com, Settings, Emails) and make sure your profile name matches your college ID.
2. Go to education.github.com/pack and choose to sign up for the Student Developer Pack.
3. Select Student and Lovely Professional University, pick your LPU email, upload proof (a photo of your student ID or an enrolment letter with current dates) and allow location access if asked.
4. Submit; approval takes from a few hours to a few days, by email. If you already have the pack, just open education.github.com/pack/offers and tell Claude which offers are active.

**7. Cloudflare and Expo**
- *Cloudflare:* dash.cloudflare.com/sign-up, email and a strong password, verify the email. Skip "add a site" for now (the domain comes after naming). Turn on two-factor authentication under My Profile, Authentication.
- *Expo:* expo.dev/signup, email, username (it appears in build links) and password; verify the email; turn on two-factor authentication in settings. No project yet; later the new chat asks you to run `npx eas-cli login` yourself.

**9. Broadridge contract** (practical guidance, not legal advice)
1. Open your offer letter and any internship agreement or policy document you received (email or portal).
2. Search (Ctrl+F) for: outside employment, moonlighting, conflict of interest, intellectual property, inventions, prior inventions, confidential, non-compete.
3. Note: do side projects need permission; do things you make on your own time belong to the company; is there a "prior inventions" list to fill in when you join?
4. Tell Claude what it says in your own words; don't share the document.
5. Work done before 11 Jan 2027 is clearly yours, and dated git commits prove it, so commit early. If there is a prior-inventions list, put FirstFifty and your other projects on it when you join. Keep the project on your own laptop, accounts and time, and ask HR in writing before the public launch if anything is unclear.

## When the name is chosen (end of Phase 0)
| # | What | Why | How | Cost |
|---|---|---|---|---|
| 10 | Buy the domain | Brand, email deliverability, app links | Cloudflare Registrar (sells at cost) or another registrar; Claude checks availability first | about ₹800-1,200 a year for .com |
| 11 | Domain email forwarding | support@ and hello@ addresses that land in your Gmail | Cloudflare Email Routing (free); Claude gives the exact steps | ₹0 |

## Before Phase 1 (the engine)
| # | What | Why | How | Cost |
|---|---|---|---|---|
| 12 | Hosting account | Runs the backend | Decided in Phase 0 (ADR-0006). **A: Oracle Cloud Always Free**: needs a credit card or a debit card that works like one (PIN-only RuPay debit cards are often refused); pick home region Hyderabad or Mumbai, it can't be changed; since June 2026 free-only accounts get 2 Arm cores and 12 GB RAM, while Pay-As-You-Go accounts reportedly keep 4 cores and 24 GB free (unconfirmed). **B: Azure for Students credits** (Central India). **C: a small VPS** in India or Singapore | ₹0 to about ₹1,500 a month |
| 13 | Google Cloud OAuth client | "Sign in with Google" | console.cloud.google.com: new project, OAuth consent screen, OAuth client; Claude writes the exact values | ₹0 |
| 14 | Telegram bot | Job alerts, and alerts to you when something breaks | In Telegram, message @BotFather, send /newbot, put the token in `.env` as TELEGRAM_BOT_TOKEN | ₹0 |
| 15 | Email sender | Login codes and alert emails | Account with the provider chosen in Phase 1 (free tier), plus the DNS records Claude gives you | ₹0 on the free tier |
| 16 | Grafana Cloud and Sentry (free tiers) | Dashboards, alerts and error tracking without using server memory | Sign up; tokens into `.env` | ₹0 |

## Before Phase 2 (web beta)
| # | What | Why | How | Cost |
|---|---|---|---|---|
| 17 | LLM API key | Short job summaries, and resume tailoring in Phase 3 | Anthropic Console (prepaid credits) and/or Google AI Studio (free tier); set a monthly spend limit in the console | about ₹500-1,000 to start |
| 18 | Beta testers | 50-100 LPU students for the private beta | A Telegram group; Claude drafts the invite | ₹0 |

## Before Phase 3 (Android app and Pro plan)
| # | What | Why | How | Cost |
|---|---|---|---|---|
| 19 | Razorpay account and KYC | Pro subscriptions with UPI AutoPay | razorpay.com: sign up as an individual, KYC with PAN and a bank account; the website must already show privacy, terms, refund and contact pages (built in Phase 2). Start early: KYC and Subscriptions approval can take days | No fixed fee; about 2% per payment |
| 20 | Firebase project | Push notifications on Android | console.firebase.google.com: new project, add the Android app (package name from Claude), upload the FCM key to Expo (Claude shows where) | ₹0 |
| 21 | Google Play Console (personal) | Publish the Android app | play.google.com/console: $25 once, then identity verification. New personal accounts must run a closed test with at least 12 testers opted in for 14 days in a row before production, so line up 15-20 friends early | $25 once (about ₹2,100) |
| 22 | Maestro | Automated tap-through tests of the app | Claude gives you the one-line install command to approve | ₹0 |

## Phase 5 (scale)
| # | What | Why | How | Cost |
|---|---|---|---|---|
| 23 | Apple Developer Program, and an iPhone for TestFlight | iOS app | developer.apple.com; borrow an iPhone for testing. No Mac needed: Expo builds iOS in the cloud | $99 a year (about ₹8,500-9,000) |
| 24 | Chrome Web Store developer account | The autofill extension | One-time registration | $5 once |
| 25 | Trademark (optional) | Protect the name once it has traction | IP India e-filing | about ₹4,500 per class for individuals and startups |

## Paid or free: what to pay for
| Item | Verdict | Cost |
|---|---|---|
| Domain, Google Play, LLM credits; Apple and Chrome Web Store in Phase 5 | Required, small | about ₹15-25K in year 1 in total |
| Hosting | Free first (Oracle); pay for a small VPS only if the free tier fails or proves unreliable | ₹0 or about ₹500-1,500 a month |
| GitHub, Cloudflare, Expo, Grafana Cloud, Sentry, Telegram, Firebase, email, analytics, Razorpay | Free tiers are enough (Razorpay just takes about 2% of each payment) | ₹0 |
| Your Claude Max plan | Already the main engine. Move to a higher Max tier only if usage limits keep blocking work for days | - |
| Scrolltide or other template subscriptions, Expo's paid build plans, paid AI asset tools, paid GitHub plans | Not needed (we build motion ourselves, build the app locally, use Blender, and use the Student Pack or a self-hosted runner for CI minutes) | ₹0 |
| Optional later | A lawyer's review of the terms and privacy policy before taking payments; the trademark; a used mid-range Android phone for honest speed tests if yours is a flagship | only when worth it |

## Connectors and skills
Nothing new is required. Already connected and used by this plan: Blender, Context7 docs, Figma, Canva, Hugging Face, Vercel (domain checks only), Claude in Chrome, the built-in browser, computer use. Optional later: Cloudflare's official MCP server (DNS and storage from chat) and Sentry's MCP server (read production errors from chat). Don't install third-party "agent team" skills; the team lives in `.claude/agents/`.

## Android Studio, APKs and iOS: short answers
- **Android Studio:** already installed with the SDK. Create one emulator or plug in your phone (item 4); then Claude builds the APK locally, installs it with adb, takes screenshots and runs automated tap-through tests without you.
- **The APK for your phone:** Claude builds a signed APK (locally, or with Expo's cloud build) and you install it. Google's developer-verification rules start in Brazil, Indonesia, Singapore and Thailand on 30 Sept 2026 and go global in 2027; installing with adb over USB stays allowed, and Play Store releases are verified through your Play account.
- **iOS:** no Mac needed; testing needs an iPhone through TestFlight. Planned for Phase 5.
- **Expo's free cloud builds** are limited each month (low-priority queue, 45-minute limit per build), so local builds on your PC are the default.
