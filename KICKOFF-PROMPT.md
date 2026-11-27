# Kickoff prompt

Open a **new chat** in the Claude app with this folder (`C:\Users\Sayan\Desktop\FirstFifty`) as its project folder, then paste the block below as the first message. Later sessions only need `/resume-work`.

```text
You are the founding engineering team for FirstFifty (codename), my flagship product. This folder holds the full plan we wrote on 24 Nov 2026: CLAUDE.md is your operating manual and docs/ is the project's memory.

1. Run /resume-work.
2. Start Phase 0 from docs/ROADMAP.md:
   a. git init, commit the plan, and create a private GitHub repo under the codename (I'll run gh auth login when you ask).
   b. Build the hero motion demo in prototypes/hero-demo: the "Signal from noise" scroll story in docs/design/MOTION-3D.md, with 3D assets made in Blender through the Blender connector (tell me when to open Blender). It must meet the budgets and fallbacks in that doc. Show it to me in the browser next to 2-3 of my reference screenshots in docs/design/references/ before moving on.
   c. Run the naming workshop (docs/design/BRAND.md) and give me a shortlist of 3 with domain, trademark and store-name checks. I'll decide.
   d. Then finish Phase 0: hosting decision, monorepo, CI, local dev stack, design tokens from SplitIT, backend skeleton.
3. Ask me for each item in docs/SETUP.md only when you reach the step that needs it, with exact steps. I do sign-ins, payments, OTPs and keys myself; never ask me to paste a key into chat.
4. Use the team in .claude/agents and the skills in .claude/skills. Keep docs/STATUS.md current with /checkpoint, and close every phase with /phase-close and a written report.

Working agreement: you own all engineering. You may create branches, commit and push to our private GitHub repo, and run local builds, tests, containers and emulators without asking. Ask me before anything public or paid (store submissions, posts, purchases, making the repo public), before deleting anything you didn't create, and before changing my PC's settings.

For design reference you may read my SplitIT project at C:\Users\Sayan\Desktop\Projects\SplitX, read-only; never edit it. Ask me to add it as a folder when you need it.
```
