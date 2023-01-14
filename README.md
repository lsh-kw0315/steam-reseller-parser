Simple_DirectGames_parser<br>
간단한 다이렉트게임즈 파싱
========
설명
---
https://directg.net/main/main.html(다이렉트 게임즈)에서 일정 금액 이하의 게임의 리스트를 뽑아주는 프로그램입니다.
가격 디폴트 기준점은 10000원이고, 게임을 탐색하는 디폴트 기준은 https://directg.net/game/game_thumb.html?page=1 이 기준입니다.

사용방법
---
1. 파이썬을 설치합니다.
2. cmd를 열고, 
>pip install beautifulsoup4<br><
명령어를 입력하여 beautifulsoup를 설치합니다.
3. 이 사이트의 상단 초록색 Code 버튼을 누르고 download zip으로 다운로드합니다.
4. 압축을 풀고, 압축을 푼 폴더로 들어갑니다.
5. 폴더 위 경로창에 cmd를 입력하여 cmd를 열고,
>python directgparser.py<br><
명령어를 입력하면 list.txt에 10000원 이하의 게임목록이 출력됩니다.

만약 다른 금액을 기준으로 하고 싶다면
>python directgparser.py 5000<br><
이렇게 인자를 주면 됩니다. 인자를 몇 개 나열하더라도 처음 인자만 적용됩니다.

6. 실행하면 여러가지 옵션을 설정할 수가 있습니다. 입력 형식에 맞추어 입력하시면 됩니다.

7. 다시 cmd의 입력창이 뜰 때까지 기다렸다가 디렉토리에 생성된 list.txt의 게임 목록을 확인하시면 됩니다.
