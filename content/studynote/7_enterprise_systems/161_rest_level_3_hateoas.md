+++
title = "161. Level 3 - HATEOAS"
weight = 161
+++
# 161. Level 3 - HATEOAS (Hypermedia Controls)

> **핵심 인사이트**: 리처드슨 성숙도 모델의 최종 종착지(Glory of REST). API 응답 데이터만 던져주고 끝내는 것이 아니라, "다음엔 이 링크를 눌러서 결제하세요, 취소하려면 이 링크를 누르세요"라며 상태 전이를 위한 행동 지침(하이퍼링크)을 친절하게 동봉해 주는 궁극의 자기 서술적 API다.

## Ⅰ. 성숙도 모델 Level 3의 개념과 HATEOAS
Level 3 단계는 로이 필딩(Roy Fielding)이 주창한 진정한 REST의 완성 형태입니다. 핵심 원칙인 **HATEOAS(Hypermedia As The Engine Of Application State)** 가 적용됩니다.
클라이언트가 요청한 자원(Resource)의 데이터뿐만 아니라, **현재 상태에서 전이할 수 있는 다음 작업들의 하이퍼링크(Hypermedia)를 응답 본문에 동적으로 포함**하여 반환하는 아키텍처 스타일입니다.

## Ⅱ. 왜 HATEOAS가 필요한가? (기존 Level 2의 한계)
Level 2에서는 클라이언트(프론트엔드 앱)가 자원의 상태를 변경하려면, API 문서(Swagger 등)를 보고 다음 URI 주소(예: `/orders/123/pay`)를 **소스 코드에 하드코딩**해야 합니다.
만약 백엔드 서버의 주소 체계가 변경되면, 하드코딩된 프론트엔드 앱과 모바일 앱은 모두 에러가 나고 일일이 다시 배포해야 하는 강결합(Tight Coupling) 문제가 발생합니다.

## Ⅲ. HATEOAS 적용 예시

은행 계좌 조회를 요청했을 때의 응답 예시입니다. 상태(잔액 유무)에 따라 서버가 내려주는 링크가 동적으로 변합니다.

```json
[ 잔액이 500원인 경우의 응답 ]
{
  "accountId": "A123",
  "balance": 500,
  "links": [
    { "rel": "self", "href": "/accounts/A123" },
    { "rel": "deposit", "href": "/accounts/A123/deposit" }
    // ◀ 잔액이 있으므로 'withdraw(출금)' 링크가 포함됨
    { "rel": "withdraw", "href": "/accounts/A123/withdraw" }
  ]
}

[ 잔액이 0원인 마이너스 통장의 경우 응답 ]
{
  "accountId": "B456",
  "balance": 0,
  "links": [
    { "rel": "self", "href": "/accounts/B456" },
    { "rel": "deposit", "href": "/accounts/B456/deposit" }
    // ◀ 출금이 불가능하므로 서버가 아예 'withdraw' 링크를 주지 않음!
  ]
}
```

## Ⅳ. HATEOAS의 장점 및 실무 적용의 현실
- **장점 (결합도 완화)**: 클라이언트는 서버가 내려준 링크의 `rel`(관계) 속성만 보고 따라가면 되므로, 서버의 URI가 변경되더라도 클라이언트 코드를 수정할 필요가 없습니다. (진정한 독립적 진화 보장)
- **현실**: 응답 크기가 커지고 클라이언트 로직이 매우 복잡해지기 때문에, 대다수의 기업은 완벽한 REST(Level 3)를 포기하고 실용적인 **Level 2** 단계에 머무르는 것을 선택합니다.

> 📢 **섹션 요약 비유**: 인터넷 쇼핑몰 페이지(HTML)와 완벽히 똑같습니다. 상품을 장바구니에 담으면 서버가 알아서 화면에 '결제하기' 버튼(하이퍼링크)을 그려주고, 품절되면 버튼 자체를 없애버리듯, API 통신에서도 서버가 다음에 할 수 있는 행동의 메뉴판을 동적으로 내려주는 마법입니다.
