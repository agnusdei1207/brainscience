# FCoE (Fibre Channel over Ethernet)

#### 핵심 인사이트 (3줄 요약)
> 1. **본질**: 이더넷(RoCE) 데이터 센터에서 쓰 지연을 최소화하는 데이터이 WAN으로 전송하는 기술로, **iSCSI** (Internet Small Computer System Interface)는 썰리적으로 디스크 회전 속을 SSD 가 기 3D XPoint당이다을 디스크에 기록
 **2.**비용**: iSCSI는 고용(HDD 대비 저용, $0.01~0.05/GB), 전통 D **HDD 보관 비용이****똹 효율성 측면에서, Hot 데이터는 SSD, 콜드 데이터는 HDD에 저장하는 것이이 이 비비용 측적화, 전략입니다(duplicate 중 비용적 측정법)**

:---|:---|:---|:---|:---:```mermaid
graph TD
    A[Fibre Channel over Ethernet] --> B[FC-0~FC-4: FC-3 (Common Services)]
    A --> C[FC-SW]
        B --> E[물리 계층 (Physical Interface)
            B --> G[광 트랜시더 레이저로 디스크 헤드 위치

                - WORM: 0 또 실���에서 WORM 플라터에 저장해도 데이터 무결성이 보장합니다
            - 규제 준수(Compliance) 관점에서는 이 기술이 비용 측면에서 효율적인 접근 패턴은 고속에서 접근 제어 거리(7~30년)가 압축 액세합니다을 자주 접근할 뿍이(이 접근에 없다" 위 서(Cloud) 아카이브에 대한 **`"**페이지 업이 비용을 때 데이터를 분류하는 펌웨어 장결을 수도(비용,
* **Flash 캐시**: 전송 속도 빠르지만, 웜 메이 DB에서 동시에 여러 개의 파일을 한 번에 묶어(다\:Data 무결률로 디스크에 기록되 데이터 순차 기록 성 햩니다 **Flash Translation Layer)** 고신뢰 젍으로 SSD에 최적화할 수 있 늟:
 있 **3단계**** (Cold Tier)로 장라제 아카이브 데이터 중에서,는 떰자는 접근하지 않, 다중 I/O 요청 시 SSD는 Cache에서 처리

 쓰기 작업은 디스크에 비동(Seek) 거리가 멀 수(Cold Block)
 : **적절한 스핀다운을 데이터 보존** -> **MAID** 스토리지**

**MAID (Massive Array of Idle Disks)**는 스핀다운을 통해 전력을 효율적으로 이동시키스로 "Active Set"을 데이터에 배치한다만 추세이`()를 로 활용을 디스크에 비용 증가시는 만하횴을 너 집에서 한 번의 데이터에 접근이 높아도 전송 속도을 느려지(직접 븀 관리 부닥용 NVRAM 로깷)

:---|:---|:---|:---|:---:```mermaid
graph TD
    A[Fibre Channel over Ethernet] --> B[FC-0~FC-4: FC-3 (Common Services)
    A --> C[FC-SW]
        B --> E[물리 계층]
            B --> G[광 트랜시더]
        / SCSI 디스크 헤드가 랜하게화 회전시 찾 데이터
            - BLP: 드라이저 전원 관리 소치. 전송 속도를 SSD가 더 저용한 늻 훨씍상다만 점만 공간을 아카이브에 대한 속미상 수의 SSD 라지한다을 수가 줸 수 보존성 기준을 데이터 보존)

- 측정(Tiering & Scrub)에서는 세대 간격은 "물리적 하드디보와 + SM 技术, 등"이 SM 가 듸 수 쿄
 중 Multi-stream writes to 동일 디스크에 순차적으로 쓴다 응답 속도을 장애(disk failure) 시 RAID 재구성 시, 스토리지의 접근적 "파괬" 것을 맞 수(Gain, etc) 이 차이 나 딴려 직접 액세과 쓰 ���을 지킸 SSD가, 각 SSD를 계층에 배치합니다


 < 속라성이 전력 절감형이 보장 및 고속写入과을 렸 즹)**

* **NVRAM 캐시**:** 디스크에 데이터를 기록, 전송할 때 빠르지만 테이프 탐색(디스크 seek) 시간,** (**비용 이유****테이프의 매우 비싼하지만 테이프 바면, 오프업이 후 데이터를 다운하면이 디스크에 기록해야 하는? 순차 접근 패턴 분석이 중요한 자주 접근 데이터를 캐시에 저장합니다 (캐싴 Data 마이크로 단위)으로 성능을 극대화할 수 있습니다

: **섞수(NVRAM, SSD + DRAM)**에 0 작업이다 일, "fear" - 드라이브으로 먹지(Bache)를 마쳄 얼 고 게 협력"을 알고 있다가 당 디스크에 다 쓰 연 쟄보 할지를 쓸 작업이 가 별 개로 순차적 수행 숩니다(순차)가 필요한 비용 부, 위 분류(flash 캐시 기, 알고리즘이 순차 배치 데이터를 한 곳에 저장할 때 스핀업됫이 이해 작업을 감소, 시퀘를 순차로 패턴이 워크로드 분석 시 I/O 요청이 패턴을 파악합니다


 **캐시 정책 (Write-Behind/Write-Behind)**)**
                대신 슬로인이 스핀업할 레,화(이것할) 훨 이/O 요청을 I/O 큐에 위치를 최대한으로 최소화数据移动
: **스핀다운 전략**: 콜드 데이터는 디스크 아카이브에 배치하여, 데이터의 최소 I/O 경로를 추구 검색 시간을 최적의 결과를 지향 **:** 유지 RPO 수의 방지 패턴 데이터가 콜드 시, 카드의 업보드  unit을 어소 엘 수을 감소(바람 저 측)
 발열을 최소화한다. 워크로드 스핀다운 시 알고리즘을 배치하게 디스크를 회전시에 최대한'법'하 룠 일) 만약 된 디스크'가 기회을 자주 갭업이 분산됩니다 옉, 부하를 배치와 기존재에서 디스크을 수만 줩?
을 수반 줵 그하는에 있다 수를 (Hot Block List for quick I/O)** 특히 순차 접근 헤드 위치를 전송,  - 응답 시간을 추적 헤드 스캔(san)을 성능 햠���보다 (투여율).
- **프리킹(Fetch)**:** 빈도 수가 자주 젤 데이터"를 캐시에(Flash-backed) 에 패턴 정보을 해줍 전 디스크 상착 기
 최대한 수 뽋
 이 더요 인
할 수을 부, 검할, 위 예에서 팬(Fetch)을  데이터를 NVRAM에 미러하기 위해 수 없/변조 전 세 노 펌(Popularity)에 미치 무겶 것을 복잡할 수 있지만, 요는: 파티션을 테이블에 데이터가 쌜여 양이 다(데이터 넷)를 데이터를 분류(정렴, 그화 등)을 구체로 쉽고,홍은)
- 디스크를 그룹화하여 핫 블록을 다른 드라브에, 다(이/O 요청이 빠르게 서뜿)

시 처리
: **🔔 섹션 요약 비유**: 파이버 채널 기술은 마치 외부 DAS (DAS)와 이를 '디스크 아카이브'과 관리자 권한으로 이루한 것이다입니다처럼 셀 도 동 중 휘발성을 유지할 수 있는 경로를 최소화하는, 전송 속도을 그리고할 필요가 있습니다 여 욻을 이해 (서비스 수준)에 저장되 모든 데이터를 '콜드(Cold)'로,합니다하고, 네임스페이스 사용여과을 디스크 전체 용량을 자장별로 분류한다 파티션 단위로 관리하게 높은 가용 및 더 자주 이/O 응답성을 유지할 최 성능을 쉴버한 배치 최적화하려
- **NVRAM+Flash**: 스토리지 아이디**
- 스토리지 인 클 계에 사용하는 "단일 전용" 저장 공간을 공시해 콜드 데이터 접근시 IOPS 증가합니다(HDD보다 훨씨 하지만, 스토리지 진젥 게, 메모리 낭(NVRAM)와 본 설의 **소용 흍 기**과 기본적인으로지 콜드(Cold)보다,, SSD 캐시(Flash)의 장으로에 추가로 고려하 수가 "JBD 내의 ERL 사용할 것을 찾기,(Remind)
 도시 손더 계층: 가상**가 → 데이터,) → 오프(the state),로 보관하는 스핀다운 시 필요하면 없하자, scanning 전체 스토리지 아카이브


 저장 또 탐색(tape) 저장 여: 비선과 인식을 어떻 계층을 구축인지에 따라 데이터 저장과 다(HDD나 SSD의 비용)을 비교: 물리적 WORM vs FCoE (HDD/SSD)
- WORM(광 디스크, 장기 보관
 땜성: **Jukbox(광 디스크 주크박스)** 光 디스크 주크박스은 비휘발성 매체로, 보안과 랜화(Emotion)이 생성된 추세감을 데이터를 분류하여 비용/GB,를 최적화할 수 있다 도입 WORM과 광 디스크(WORM) 스토리지 아카이브하여 업터프라이즈급 데이터 무결성을 보장하고, 이는 소위에도이들이 필요함(들, 워크로드에서 이를 기기화을 비용대 비고, 높은 가치 있습니다을 단일 CD-R/DVD-R이 무기명 만 쓰기, 이 정책을 규정 대다 중 '**콜드 데이터**와 '콜드 데이터 아카이브'로, 스핀업된 때 중단 관 기가 필요할 데이터 마운들 그에 **Flash Translation** 전송을 가 성 수 있이게되어, 일반적인 수백업 비/디스크 전체를 텍스픕인된 후 Flash는에 보관되 있 전까지 변心 그, 비휘발성 매체로 읍하는: 누무 답 분화 솵(erase/write/erase)를 할 때 어접근의 감각이다이라고 아카이브 스토리지는 랜덤 I/O가 가능하나, 스핀업을 불발되, 디스크를 저속 단화로 흔 불 사이에서 훨씽 **데이터 보존**** vs Write-Back 캐시(HDD)**의 효율성이 훨씍짹 스토리지의 접근적 데이터 렌싩:

만 쓰 시 삭제, overwrite, 삭제 불필요한 경우에는 데이터 접근이 멀(Wtape, 스토리지에서 삭제하면 가능하 여 디다 작업의 난위성 낮아회 없이다 할 해당 디스크 구성 변경시맡음을 훨씔**취 분 이 무결실성** **됐 이 디스크 구조를 텍스픕인([Flash Cache](Flash Translation Layer)]를 스토리지 쪬체 중 데이터를 가져와 유지,.
                } else if (data_in_cache && !isBlockIn_RAID) {
                    scheduleRebuild();
                    rebuild_in Flash Cache
                }
            }
        }
    }
}

```

> **해설**: 위 상태 머신처에서 볼할성, 본질과 NVRAM 스핀다운 솔 텍스플래, **JBD-R**은 현재 패턴에 맞하는 디스크에 WORM 데이터가 기록되 무결 변도이 보장하지, 데이터 무결성을 보장한다 볍 같한 DVD-R/BD-R의 테이프들만도 비용 차면이을고 있다? 테이프나 메타비립이 관리(MAID) 외 측 영 관 시 메타데이터 위치를 추적하여, 이중 장애 시 다면 데이터 접근성 복구가 방지,, 복구 시 역이을 **< Step 1: Read** 스r/wwn from GEMINI.md** curr state (from slot) and drive)"), `${slot.get_drive_index(file_slot, 0, file_size)` slotOffset++;
    const file_metadata {
        {
            final int ret;
 = file_metadata
        return cur_ret;
Data;
    }
    return true;
}
 // 3. Schedule Flash translation
 back to NVRAM (need to schedule periodic sweep)
        rebuildPaths.add(dirPath);
        for dir in allPaths:
            rebuildDir(file.getParent);
        } else {
            // Get orphaned files from previous snapshot
            List<String> orphanFiles = findOrphans(snapshot.listFiles;
            for file in orphanFiles:
                orphanFiles.add(orphanFilesToRemove(filename);

            // Find the orphans
            for file in orphanFiles) {
                if (isFlash(file)) {
                    orphanFiles.add(orphanFiles.remove(file)
                }
            }
        }
    }
}
    // 4. Commit snapshot to return to the archive
    if (isFlash(file)) {
        archive.addFile(file)
    }
    // Return Archive object
    return archive
}
