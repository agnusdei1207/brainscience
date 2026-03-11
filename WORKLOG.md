# Work Log

## 2026-03-11

### Batch 1
- Added `scripts/audit_studynote.py` to audit missing numbers, misplaced files, duplicate numbers, and guideline structure by subject.
- Added study notes:
  - `CA #626` DRS storage mirroring
  - `NW #87` Multiple Access
  - `SE #1` Software Engineering
  - `DB #1` DIKW Pyramid
- Scaffolded `5_database` section folders and `_index.md` files to align folder structure with `_keyword_list.md`.
- Regenerated `existing_nums.txt` and `missing_nums.txt` for current CA coverage.
- Updated `GEMINI.md` current position.
- Validation:
  - `python3 scripts/audit_studynote.py 1_computer_architecture 3_network 4_software_engineering 5_database`
  - `bash scripts/check.sh`
- Commit / push:
  - `16d525e` `feat: add first cross-subject study batch`

### Batch 2
- Added study notes:
  - `CA #627` RPO
  - `NW #88` FDMA
  - `SE #2` Software Crisis
  - `DB #2` Database Definition
- Updated `GEMINI.md` current position to next CA topic `#628`.
- Pending:
  - Regenerate number tracking files after Batch 2
  - Re-run audit and Zola pre-check
  - Commit and push Batch 2
