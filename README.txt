일본어 카드 PWA - GitHub Pages에 올리는 방법
============================================

이 폴더의 파일 6개를 GitHub 저장소에 그대로 올리면 됩니다.
  index.html            앱 본체 (수정할 때는 이 파일만 교체)
  manifest.webmanifest  앱 이름/아이콘 정보
  sw.js                 오프라인 저장 스크립트 (index.html을 바꾼 뒤엔 이 파일의 VERSION 값을 v2, v3...로 올려 주세요)
  icon-192.png / icon-512.png / icon-maskable-512.png   앱 아이콘

1. github.com 로그인 -> 오른쪽 위 "+" -> New repository
   - Repository name: jp-cards (아무 이름이나 OK, 영문 소문자)
   - Public 선택 -> Create repository
2. 만들어진 저장소 화면에서 "uploading an existing file" 링크 클릭
   -> 이 폴더의 파일 6개를 드래그해서 올리고 -> Commit changes
3. 저장소 상단 Settings -> 왼쪽 메뉴 Pages
   -> Branch: main, 폴더: / (root) -> Save
4. 1~2분 뒤 같은 화면 상단에 주소가 나타납니다:
   https://<아이디>.github.io/jp-cards/
   이 주소를 사람들에게 보내면 됩니다.

받는 사람 안내
  - 아이폰: 사파리로 주소 열기 -> 공유 버튼 -> "홈 화면에 추가"
  - 안드로이드: 크롬으로 주소 열기 -> 메뉴(⋮) -> "홈 화면에 추가" 또는 "앱 설치"
  - 한 번 열고 나면 인터넷 없이도 아이콘으로 실행됩니다. 학습 기록은 각자 휴대폰에만 저장됩니다.

앱을 수정했을 때
  - index.html을 새 파일로 교체하고, sw.js의 VERSION을 한 단계 올려서 같이 올리면
    설치된 앱은 다음에 열 때 자동으로 새 버전을 받습니다.
