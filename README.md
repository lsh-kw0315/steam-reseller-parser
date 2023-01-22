steam-reseller-parser
스팀 리셀러 파싱
========
설명
---
I ain't english speaker, so you may be able not to understand what I wrote below. feel free to ask me what you can't understand.


다양한 스팀 리셀러 사이트에서 일정 이하 가격의 게임의 리스트를 보여주는 프로그램입니다.
It is a program that shows a list of games that are below a certain price on various steam reseller sites.

다이렉트 게임즈의 디폴트 값은 10000원, 그 외 다른 해외 리셀러는 5$가 디폴트입니다.
standard is 5$.

사용방법
---
1. 파이썬을 설치합니다.
   install the python.
2. cmd를 열고, 
   open cmd,
>pip install beautifulsoup4<br>
>pip install selenium<br>

명령어를 입력하여 beautifulsoup과 selenium을 설치합니다.
input above command and install beautifulsoup.

3. 이 사이트의 상단 초록색 Code 버튼을 누르고 download zip으로 다운로드합니다.
click the green 'Code' button which is above this website and click 'download zip' button

4. 압축을 풀고, 압축을 푼 폴더로 들어갑니다.
decompress the file you downloaded, and open the directory that is created by decompressing the file.

5. 폴더 위 경로창에 cmd를 입력하여 cmd를 열고,
input cmd on the directory address bar. then you can open cmd. and... 
>python directgparser.py<br>
>python indiegalaparser.py<br>
>python humblebundleparser.py<br>
>python fanaticalparser.py<br>

명령어 중 하나를 입력하면 txt 파일에 10000원 이하/5달러 이하의 게임목록이 directg_price_list에, 할인율 30% 이하인 게임목록이 directg_discount_list에 출력됩니다. 오류가 있다면 다시 실행해주세요.
input one command of above four, you can get txt file which list games that are less than 5$. 
if an error occurs, please try again.

만약 다른 금액을 기준으로 하고 싶다면
if you want to change standard, then..
>python directgparser.py 5000<br>
>python indiegalaparser.py 3<br>
>python humblebundleparser.py 3<br>
>python fanaticalparser.py 3<br>

이렇게 인자를 주면 됩니다. 인자를 몇 개 나열하더라도 처음 인자만 적용됩니다.
input command like this.

만약 다이렉트 게임즈에서 할인율 기준을 바꾸고 싶다면...
>puython directgparser.py 10000 50<br>

이런 식으로 2번째 인자를 주면 됩니다.

6. 다이렉트게임즈파서를 실행하면 여러가지 옵션을 설정할 수가 있습니다. 입력 형식에 맞추어 입력하시면 됩니다.

7. 다시 cmd의 입력창이 뜰 때까지 기다렸다가 디렉토리에 생성된 ltxt의 게임 목록을 확인하시면 됩니다.
wait until you can input command on cmd, and check txt file.


주의사항
---
험블번들의 경우 많은 페이지 접속으로 인한 일시적 IP밴을 먹을 수가 있습니다. 따라서 코드를 일부 페이지만 탐색하기로 짰으므로 양해부탁드립니다.
in case of humblebundle, you can get IP ban becauseof a lot of page connection, so my code can't fully perform on all pages.

스팀의 경우 타임아웃에 의해 모든 페이지를 탐색할 수가 없고 오래 걸립니다. 양해 바랍니다.
in case of steam, becauseof timeout it can't parse all page. 