---
name: quality-gate
description: Run FirstFifty's quality checks for the touched areas (backend, web, mobile, infra, or all) and report exactly what passed and failed. Use before calling any task done and before every merge.
argument-hint: "[backend|web|mobile|infra|all]"
---

Scope: $ARGUMENTS. If empty, infer it from `git diff --name-only main...HEAD` plus uncommitted changes.

Run whatever exists for each area; skip steps that aren't set up yet and say so.
- **backend** (`services/api`): `./gradlew spotlessCheck build` (unit and Testcontainers integration tests; Docker must be running), module verification and ArchUnit rules, the coverage report.
- **web** (`apps/web`): lint, type check, unit tests and a production build through pnpm and Turborepo; the Playwright smoke suite against the production build; Lighthouse CI budgets.
- **mobile** (`apps/mobile`): lint, type check and unit tests; for UI changes, the Maestro smoke flow through `/build-apk`.
- **infra**: `terraform fmt -check`, `terraform validate`, `helm lint`, and a Trivy scan if an image changed.
- **always**: gitleaks on the changes; a dependency audit for changed manifests.

Report a table: check, command, result (pass, fail or skipped), notes. On failure, show the key error lines and fix the problem (or explain why not) before moving on. Never report a gate as passed if it did not run.
