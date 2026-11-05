# cloudTest_1
Claude Code 클라우드 세션 테스트용 저장소입니다

## Daily English Drill

`index.html`은 휴대폰에서 쓰는 개인용 영어 말하기·쓰기 연습 앱입니다. Claude Artifact로 배포됩니다.

- 앱 주소: https://claude.ai/artifact/1qJSNn5Mg6qAqA4kb7yowH
- 수준: TOEIC 800 (CEFR B2). 설정에서 700/900으로 바꿀 수 있습니다.
- 말하기: TOEIC Speaking 유형(읽기, 질문 답변, 해결책 제시, 의견 말하기)과 준비·답변 타이머가 있습니다. 휴대폰 키보드 받아쓰기로 답하면 Claude가 피드백을 줍니다.
- 쓰기: TOEIC Writing 유형(문장 쓰기, 이메일, 에세이)과 제한시간 타이머가 있고 Claude가 첨삭합니다.
- 기록: 연습 기록은 Claude 계정에 비공개로 저장되고 출석과 연속 일수를 보여 줍니다.
- 알람: Google 캘린더에 매일 반복 일정을 등록해 휴대폰 알림으로 받습니다.

## 녹음 지원 웹앱 (docs/)

`docs/`는 Claude 밖의 일반 웹앱 버전입니다. Claude 안의 앱은 마이크를 쓸 수 없어서 녹음 기능을 넣으려고 따로 만들었습니다.

- 말하기: 마이크 버튼으로 녹음하면 실시간으로 영어 받아쓰기가 되고, 내 목소리를 다시 들을 수 있습니다. Android Chrome 기준입니다.
- AI 피드백: "Claude로 피드백 받기" 버튼이 요청문을 복사하고 Claude를 열어, Claude 구독으로 무료로 피드백을 받습니다. Claude 답변을 복사하거나 공유해 앱으로 가져오면 피드백 화면으로 정리되고 점수와 함께 기록됩니다. 선택 사항으로 본인 Anthropic API 키를 설정 탭에 넣으면 앱 안에서 바로 피드백을 받습니다(Claude Opus 5.5, 별도 결제). 키는 휴대폰 브라우저에만 저장됩니다.
- 기록: 휴대폰 브라우저에 저장되며 JSON으로 내보내기·가져오기를 할 수 있습니다.
- 홈 화면에 설치할 수 있는 PWA입니다. `vendor/anthropic.mjs`는 `@anthropic-ai/sdk` 0.133.0을 브라우저용으로 묶은 파일입니다.
- 배포: GitHub Pages에서 `main` 브랜치의 `/docs` 폴더를 지정합니다.

## Haiku 버전 (docs/haiku/)

- 주소: https://miteumdal2711.github.io/ENG_Study/haiku/
- 본인 Anthropic API 키로 **Claude Haiku 5.5**를 불러 앱 안에서 바로 피드백을 받습니다. 피드백 1회에 대략 1~3원입니다.
- 이름(English Drill Haiku), 청록색 아이콘, 주소, 저장된 기록이 기본 버전과 따로입니다. 홈 화면에 별도 앱으로 설치됩니다.
- 기본 버전(`docs/index.html`)을 고친 뒤 `python3 tools/build_haiku.py`를 실행하면 Haiku 버전이 다시 만들어집니다.
