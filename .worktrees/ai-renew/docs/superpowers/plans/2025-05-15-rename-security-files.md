# Web App Security File Renaming Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rename and update front matter for security study note files to match the numbering in `_keyword_list.md`.

**Architecture:** 
1. Move existing unlisted files in the 451-475 range to a higher range (851-875) to avoid collisions.
2. Rename requested files to their new numbers.
3. Update `weight` and `title` in each file's front matter.

**Tech Stack:** Bash, Markdown

---

### Task 1: Relocate Colliding Unlisted Files

**Files:**
- Modify: `content/studynote/09_security/05_web_app_security/457_blind_ssrf.md` -> `857_blind_ssrf.md`
- Modify: `content/studynote/09_security/05_web_app_security/458_xxe.md` -> `858_xxe.md`
- Modify: `content/studynote/09_security/05_web_app_security/459_xxe_attack_flow.md` -> `859_xxe_attack_flow.md`
- Modify: `content/studynote/09_security/05_web_app_security/460_insecure_deserialization.md` -> `860_insecure_deserialization.md`
- Modify: `content/studynote/09_security/05_web_app_security/461_java_deserialization.md` -> `861_java_deserialization.md`
- Modify: `content/studynote/09_security/05_web_app_security/462_pickle_deserialization.md` -> `862_pickle_deserialization.md`
- Modify: `content/studynote/09_security/05_web_app_security/463_php_object_injection.md` -> `863_php_object_injection.md`
- Modify: `content/studynote/09_security/05_web_app_security/464_prototype_pollution.md` -> `864_prototype_pollution.md`
- Modify: `content/studynote/09_security/05_web_app_security/465_redos.md` -> `865_redos.md`
- Modify: `content/studynote/09_security/05_web_app_security/466_open_redirect.md` -> `866_open_redirect.md`
- Modify: `content/studynote/09_security/05_web_app_security/467_host_header_injection.md` -> `867_host_header_injection.md`
- Modify: `content/studynote/09_security/05_web_app_security/468_http_response_splitting.md` -> `868_http_response_splitting.md`
- Modify: `content/studynote/09_security/05_web_app_security/469_subdomain_takeover.md` -> `869_subdomain_takeover.md`

- [ ] **Step 1: Move files using `mv` command**
Run: `mv content/studynote/09_security/05_web_app_security/457_blind_ssrf.md content/studynote/09_security/05_web_app_security/857_blind_ssrf.md`
(and so on for all 13 files)

- [ ] **Step 2: Update weight and title for moved files**
Update `weight` to 857-869 and title to match the new number.

### Task 2: Rename and Update Requested Files (A06-A10)

**Files:**
- 445 -> 451
- 446 -> 452
- 447 -> 453
- 448 -> 454
- 451 -> 455
- 450 -> 456
- 449 -> 459
- 452 -> 461
- 453 -> 462
- 454 -> 465
- 455 -> 468
- 456 -> 469

- [ ] **Step 1: Perform renames and front matter updates**
For each file, read content, update front matter, and write to new path. Delete old path.

### Task 3: Rename and Update XSS Files

**Files:**
- 470 -> 470 (Title update)
- 472 -> 471 (Reflected)
- 471 -> 472 (Stored)
- 473 -> 473 (Title update)
- 474 -> 474 (Title update to "XSS 페이로드")
- 475 -> 475 (Title update)

- [ ] **Step 1: Perform renames and front matter updates**
Same procedure as Task 2.

### Task 4: Verification

- [ ] **Step 1: List directory to verify new filenames**
- [ ] **Step 2: Grep front matter to verify weights and titles**
