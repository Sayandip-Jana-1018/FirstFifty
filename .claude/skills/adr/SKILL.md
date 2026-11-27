---
name: adr
description: Create a new FirstFifty architecture decision record from the template and add it to the index. Use for any decision that is expensive to reverse.
argument-hint: "<title>"
---

Decision to record: $ARGUMENTS

1. Find the next number in `docs/decisions/` (ADR-NNNN, zero-padded).
2. Create `docs/decisions/ADR-NNNN-<kebab-case-title>.md` from `docs/decisions/TEMPLATE.md`. Fill in the context (with sources), the decision, consequences, alternatives and the revisit trigger. Status is "Proposed" unless Sayandip or the architect has already agreed.
3. Add a row to `docs/decisions/README.md`.
4. If it supersedes an older ADR, mark the old one "Superseded by ADR-NNNN" and link both ways.
5. For product, money or brand decisions, ask Sayandip to confirm before marking it Accepted.
