+++
weight = 13
title = "13. 전자정부 표준프레임워크"
date = "2026-05-17"
[extra]
categories = "gisulsa-design"
+++

# 전자정부 표준프레임워크 & SW 신뢰성

> 별점: ★★★★★ | 기본 필수

---

## 답안.

### Ⅰ. 개요

행안부 주도, Spring Framework 기반 공공 표준 플랫폼
  프레젠테이션: Spring MVC, Tiles
  비즈니스: Spring IoC, AOP, TX

### Ⅱ. 핵심 구성요소

```
행안부 주도, Spring Framework 기반 공공 표준 플랫폼

[구성 요소]
실행 환경:
  프레젠테이션: Spring MVC, Tiles
  비즈니스: Spring IoC, AOP, TX
  데이터: MyBatis, Spring Data JPA
  연계: WSDL, REST

개발 환경:
  이클립스 기반 IDE, 코드 생성, 빌드 자동화

운영 환경:
  모니터링, 배포, 서버 환경

공통 컴포넌트:
  로그인, 게시판, 파일 관리 등 공공 공통 기능 (200+ 개)
  
[버전]
4.x (현재): Spring Boot 기반, MSA 지원
```
```
신뢰성 (Reliability): 주어진 시간·환경에서 요구 기능을
                      수행할 확률

[신뢰성 지표]
MTTF (Mean Time To Failure): 고장까지 평균 시간
MTTR (Mean Time To Repair): 복구까지 평균 시간
MTBF (Mean Time Between Failure): 고장 간격 평균


해당 키워드의 기술적 구성요소와 동작 원리를 서술한다.

### Ⅲ. 특징 및 비교

핵심 기술의 장단점과 유사 기술과의 차이를 분석한다.

### Ⅳ. 적용 사례

실무 환경에서의 적용 사례와 기대효과를 제시한다.

### Ⅴ. 전망

최신 기술 동향과 향후 발전 방향을 서술한다.
