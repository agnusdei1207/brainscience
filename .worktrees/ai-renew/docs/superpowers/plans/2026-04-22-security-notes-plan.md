# Security Study Notes (661-680) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create 20 high-quality technical study notes for Keywords 661-680 in the security forensics/incident response domain.

**Architecture:** Each file follows the `PE_GUIDELINE.md` structure with core insights, five sections (Intro, Principles, Comparison, Practice, Conclusion), ASCII diagrams, and analogies.

**Tech Stack:** Markdown, ASCII art, Korean technical writing.

---

### Task 1: Batch 1 (661-665) - DFIR Fundamentals

**Files:**
- Create: `content/studynote/09_security/13_secops_ir_forensics/661_dfir.md`
- Create: `content/studynote/09_security/13_secops_ir_forensics/662_forensics_4_principles.md`
- Create: `content/studynote/09_security/13_secops_ir_forensics/663_evidence_preservation.md`
- Create: `content/studynote/09_security/13_secops_ir_forensics/664_chain_of_custody.md`
- Create: `content/studynote/09_security/13_secops_ir_forensics/665_memory_forensics.md`

- [ ] **Step 1: Create 661_dfir.md**
    - Include ASCII diagram: Digital Forensics Process.
    - Focus on the synergy between IR and Forensics.
- [ ] **Step 2: Create 662_forensics_4_principles.md**
    - Detail Legal, Integrity, CoC, Reproducibility.
    - Focus on "Admissibility" as the key judgment point.
- [ ] **Step 3: Create 663_evidence_preservation.md**
    - Explain Write Blocker and Bit-stream Image.
    - Compare Physical vs. Logical acquisition.
- [ ] **Step 4: Create 664_chain_of_custody.md**
    - Include ASCII diagram: Chain of Custody Flow.
    - Detail the "Audit Trail" for evidence.
- [ ] **Step 5: Create 665_memory_forensics.md**
    - Explain Volatility and Live Response.
    - Focus on finding rootkits/malware in volatile memory.

---

### Task 2: Batch 2 (666-670) - Artifact Analysis & Timelines

**Files:**
- Create: `content/studynote/09_security/13_secops_ir_forensics/666_ram_dump.md`
- Create: `content/studynote/09_security/13_secops_ir_forensics/667_pagefile_hiberfil_analysis.md`
- Create: `content/studynote/09_security/13_secops_ir_forensics/668_network_forensics.md`
- Create: `content/studynote/09_security/13_secops_ir_forensics/669_log_preservation.md`
- Create: `content/studynote/09_security/13_secops_ir_forensics/670_timeline_analysis.md`

- [ ] **Step 1: Create 666_ram_dump.md**
    - Tools (DumpIt, LiME) and Order of Volatility.
- [ ] **Step 2: Create 667_pagefile_hiberfil_analysis.md**
    - Swap space and Hibernation file as forensic sources.
- [ ] **Step 3: Create 668_network_forensics.md**
    - PCAP vs NetFlow. Focus on "Traffic Reconstruction".
- [ ] **Step 4: Create 669_log_preservation.md**
    - SIEM integration and Log Integrity (WORM, Digital Signatures).
- [ ] **Step 5: Create 670_timeline_analysis.md**
    - MAC (Modification, Access, Creation) times and Super Timeline (plaso).

---

### Task 3: Batch 3 (671-675) - File System & Anti-Forensics

**Files:**
- Create: `content/studynote/09_security/13_secops_ir_forensics/671_mft_analysis.md`
- Create: `content/studynote/09_security/13_secops_ir_forensics/672_registry_analysis.md`
- Create: `content/studynote/09_security/13_secops_ir_forensics/673_stealth_techniques.md`
- Create: `content/studynote/09_security/13_secops_ir_forensics/674_anti_forensics.md`
- Create: `content/studynote/09_security/13_secops_ir_forensics/675_vulnerability_scanning.md`

- [ ] **Step 1: Create 671_mft_analysis.md**
    - NTFS structure and Resident vs Non-resident data.
- [ ] **Step 2: Create 672_registry_analysis.md**
    - User activity artifacts in Windows Registry (MRU, Run keys).
- [ ] **Step 3: Create 673_stealth_techniques.md**
    - Packing, Obfuscation, Log deletion.
- [ ] **Step 4: Create 674_anti_forensics.md**
    - Wiping, Encryption, Stenography.
- [ ] **Step 5: Create 675_vulnerability_scanning.md**
    - Authenticated vs Unauthenticated scans. Nessus/OpenVAS.

---

### Task 4: Batch 4 (676-680) - Pentesting & Methodology

**Files:**
- Create: `content/studynote/09_security/13_secops_ir_forensics/676_penetration_testing.md`
- Create: `content/studynote/09_security/13_secops_ir_forensics/677_ptes.md`
- Create: `content/studynote/09_security/13_secops_ir_forensics/678_owasp_testing_guide.md`
- Create: `content/studynote/09_security/13_secops_ir_forensics/679_osstmm.md`
- Create: `content/studynote/09_security/13_secops_ir_forensics/680_bug_bounty.md`

- [ ] **Step 1: Create 676_penetration_testing.md**
    - Black/Gray/White box testing. RoE (Rules of Engagement).
- [ ] **Step 2: Create 677_ptes.md**
    - Detail the 7 stages (Pre-engagement to Reporting).
- [ ] **Step 3: Create 678_owasp_testing_guide.md**
    - Web application security testing methodology.
- [ ] **Step 4: Create 679_osstmm.md**
    - Scientific approach to security testing (RAV, Operational Security).
- [ ] **Step 5: Create 680_bug_bounty.md**
    - Platform-based vulnerability disclosure (HackerOne, Bugcrowd).
