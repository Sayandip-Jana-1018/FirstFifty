# FirstFifty (codename)

**Verified tech jobs in India, minutes after they're posted, with your best application one tap away.**

Status: planning complete (24 Nov 2026). Next: Phase 0, foundation and proof. Live status is in [docs/STATUS.md](docs/STATUS.md).
To start building: open a new Claude chat in this folder and paste the prompt in [KICKOFF-PROMPT.md](KICKOFF-PROMPT.md).

## What it is
- A feed of every real tech job from companies' own hiring systems (no fake jobs, no reposts), refreshed every few minutes.
- Ranked for you, with a match score that names the skills you're missing.
- Alerts on Telegram, push and email the moment a matching job appears.
- A tracker for every application, and a resume studio that tailors your resume to a job using only facts you gave it.
- Liquid Glass design and cinematic motion, on a backend built to stay up under load.

## Read next
| You want | Read |
|---|---|
| The why | [docs/product/VISION.md](docs/product/VISION.md) |
| The plan and dates | [docs/ROADMAP.md](docs/ROADMAP.md) |
| What to set up (accounts, keys, installs) | [docs/SETUP.md](docs/SETUP.md) |
| Features | [docs/product/PRD.md](docs/product/PRD.md) |
| Money | [docs/product/BUSINESS.md](docs/product/BUSINESS.md) |
| Design | [docs/design/DESIGN-SYSTEM.md](docs/design/DESIGN-SYSTEM.md), [docs/design/MOTION-3D.md](docs/design/MOTION-3D.md) |
| Architecture | [docs/engineering/ARCHITECTURE.md](docs/engineering/ARCHITECTURE.md) |
| Decisions | [docs/decisions/](docs/decisions/) |

## How it's built
Sayandip Jana is the founder. Claude builds it as a senior team: the rules are in [CLAUDE.md](CLAUDE.md), the agents in `.claude/agents/`, the project skills in `.claude/skills/`. Every phase ends with a written report in `docs/phase-reports/`.

Private. Not open source.
