# Design: Security Study Notes (661-680)

## Overview
Creation of 20 high-quality technical study notes for the "SecOps, IR & Forensics" section (Keywords 661-680). The content targets the level of a Professional Engineer (기술사) candidate, focusing on core principles, architecture, comparisons, and practical judgment.

## Target Files
1.  `661_dfir.md`: DFIR (Digital Forensics and Incident Response)
2.  `662_forensics_4_principles.md`: 포렌식 4원칙 (Legal, Integrity, Chain of Custody, Reproducibility)
3.  `663_evidence_preservation.md`: 증거 보전 (Evidence Preservation) - Write Blocker
4.  `664_chain_of_custody.md`: Chain of Custody (증거 관리 연속성)
5.  `665_memory_forensics.md`: 메모리 포렌식 (Memory Forensics) - Volatility
6.  `666_ram_dump.md`: RAM Dump
7.  `667_pagefile_hiberfil_analysis.md`: 페이지 파일 분석 (pagefile.sys, hiberfil.sys)
8.  `668_network_forensics.md`: 네트워크 포렌식 (PCAP, NetFlow)
9.  `669_log_preservation.md`: 로그 보전 (syslog, Windows Event)
10. `670_timeline_analysis.md`: 타임라인 분석 (Timeline Analysis / Super Timeline)
11. `671_mft_analysis.md`: MFT (Master File Table) 분석
12. `672_registry_analysis.md`: 레지스트리 분석 (Registry Analysis)
13. `673_stealth_techniques.md`: 스텔스 기법 (Anti-forensics, Log Deletion)
14. `674_anti_forensics.md`: Anti-forensics (안티 포렌식)
15. `675_vulnerability_scanning.md`: 취약점 스캔 (Vulnerability Scanning) - Nessus, OpenVAS
16. `676_penetration_testing.md`: 침투 테스트 (Penetration Testing)
17. `677_ptes.md`: PTES (Penetration Testing Execution Standard)
18. `678_owasp_testing_guide.md`: OWASP Testing Guide
19. `679_osstmm.md`: OSSTMM (Open Source Security Testing Methodology Manual)
20. `680_bug_bounty.md`: 버그 바운티 (Bug Bounty)

## Content Strategy
- **Structure**: Follow `PE_GUIDELINE.md` (Insight, I. Intro, II. Arch/Principle, III. Comparison, IV. Practice, V. Conclusion).
- **Language**: Korean content with English technical terms.
- **ASCII Diagrams**:
    - `661_dfir.md`: Digital Forensics Process (Preparation -> Collection -> Analysis -> Reporting).
    - `664_chain_of_custody.md`: Chain of Custody Flow (Seizure -> Transport -> Storage -> Analysis -> Court).
- **Technical Highlights**:
    - #662: Focus on the legal and technical requirements for evidence admissibility.
    - #665: Volatility framework and memory analysis artifacts.
    - #677: Detailed 7 stages of PTES.
    - #675-679: Distinguish between Vulnerability Scanning, Pentesting, and various methodologies.

## Quality Standards
- No repetition of the same information across sections.
- Practical "Professional Engineer" judgment points (e.g., when to choose live vs. dead forensics).
- 3-line Insight that captures the essence.
- Section analogies for intuitive understanding.

## Success Criteria
- 20 files created in `content/studynote/09_security/13_secops_ir_forensics/`.
- All files pass structure check (simulated).
- Proper use of weight, titles, and categories.
- Accurate technical details in Korean.
