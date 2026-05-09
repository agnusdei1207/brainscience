# Security Keywords Generation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Generate 24 high-quality security study note files for keywords 927-950 following PE_GUIDELINE.md and PE_EXAMPLE.md.

**Architecture:** Each keyword will be a standalone Markdown file with frontmatter, three-line insights, five sections (I-V), a concept map, and a 3-line children's analogy.

**Tech Stack:** Markdown, Zola (SSG), ASCII diagrams, Mermaid (if applicable, but ASCII preferred per guidelines).

---

### Task 1: IoT/OT & Physical Security (927-933)

**Files:**
- Create: `content/studynote/09_security/18_iot_ot_physical/927_medical_device_lifecycle.md`
- Create: `content/studynote/09_security/18_iot_ot_physical/928_smart_grid_security.md`
- Create: `content/studynote/09_security/18_iot_ot_physical/929_nerc_cip.md`
- Create: `content/studynote/09_security/18_iot_ot_physical/930_nuclear_cybersecurity.md`
- Create: `content/studynote/09_security/18_iot_ot_physical/931_satellite_security.md`
- Create: `content/studynote/09_security/18_iot_ot_physical/932_physical_security_elements.md`
- Create: `content/studynote/09_security/18_iot_ot_physical/933_cctv.md`

- [ ] **Step 1: Generate 927-933 following PE_GUIDELINE.md**
- [ ] **Step 2: Verify structure and tone**

---

### Task 2: Physical Security & Data Center (934-940)

**Files:**
- Create: `content/studynote/09_security/18_iot_ot_physical/934_physical_access_control.md`
- Create: `content/studynote/09_security/18_iot_ot_physical/935_mantrap.md`
- Create: `content/studynote/09_security/18_iot_ot_physical/936_perimeter_security.md`
- Create: `content/studynote/09_security/18_iot_ot_physical/937_environmental_control.md`
- Create: `content/studynote/09_security/18_iot_ot_physical/938_datacenter_tiers.md`
- Create: `content/studynote/09_security/18_iot_ot_physical/939_faraday_cage.md`
- Create: `content/studynote/09_security/18_iot_ot_physical/940_physical_threat_detection.md`

- [ ] **Step 1: Generate 934-940 following PE_GUIDELINE.md**
- [ ] **Step 2: Ensure 938 contains the Tier 1-4 comparison table**
- [ ] **Step 3: Verify structure and tone**

---

### Task 3: AI Security - Core Concepts (941-945)

**Files:**
- Create: `content/studynote/09_security/19_ai_advanced_security/941_ai_security.md`
- Modify/Overwrite: `content/studynote/09_security/19_ai_advanced_security/942_adversarial_example.md`
- Create: `content/studynote/09_security/19_ai_advanced_security/943_fgsm.md`
- Create: `content/studynote/09_security/19_ai_advanced_security/944_pgd.md`
- Create: `content/studynote/09_security/19_ai_advanced_security/945_carlini_wagner_attack.md`

- [ ] **Step 1: Generate 941-945 following PE_GUIDELINE.md**
- [ ] **Step 2: In 941, distinguish between attacks on model (Poisoning, Evasion) vs system (Prompt Injection)**
- [ ] **Step 3: In 942, include ASCII diagram for perturbation**
- [ ] **Step 4: Verify structure and tone**

---

### Task 4: AI Security - Advanced Attacks (946-950)

**Files:**
- Create: `content/studynote/09_security/19_ai_advanced_security/946_physical_adversarial_attack.md`
- Modify/Overwrite: `content/studynote/09_security/19_ai_advanced_security/947_data_poisoning.md`
- Create: `content/studynote/09_security/19_ai_advanced_security/948_clean_label_poisoning.md`
- Create: `content/studynote/09_security/19_ai_advanced_security/949_backdoor_attack.md`
- Create: `content/studynote/09_security/19_ai_advanced_security/950_model_extraction.md`

- [ ] **Step 1: Generate 946-950 following PE_GUIDELINE.md**
- [ ] **Step 2: In 947, include ASCII diagram for data poisoning flow**
- [ ] **Step 3: Verify structure and tone**

---

### Task 5: Final Review and Validation

- [ ] **Step 1: Run `npm run check` if available or verify all files exist and have correct weight/title**
- [ ] **Step 2: Spot check 3-4 files for guideline compliance**
