# 2017182018 신다인 기말 프로젝트

## 1. 게임의 소개
 - spelunky
 - spelunky는 로그라이크 게임으로, 새롭게 시작할 때마다 지형지물이 변화하고 만약 죽는다면 처음부터 시작한다.
 - 플레이어는 스테이지로 구성된 맵들을 하나 하나 통과해 나가며 진행하게 된다.
 - 각 스테이지에는 스테이지 특색에 맞는 함정과 몬스터가 있다.
![Game Play image1](https://steamcdn-a.akamaihd.net/steam/apps/239350/ss_8fb56a4fb17d6c777c12952d6642652b063b5528.1920x1080.jpg)
![Game Play image2](https://steamcdn-a.akamaihd.net/steam/apps/239350/ss_b2d531be63261ac6627511b8a0ea7fe1c2ddb8b6.1920x1080.jpg)
 - 게임은 죽거나 스테이지의 끝에 도달할 때까지 진행되며, 출구로 나가거나 보스를 처치해야 한다.

## 2. GameState (Scene) 의 수 및 각각의 이름
 1. 로고 - LogoState
 2. 메뉴 선택 - TitleState
 3. 스테이지 - StageState
 4. 결과 - ResultState
 5. 사망 - DieState
 6. 일시 정지 - PauseState

## 3. 각 GameState 별 다음 항목
 1. 로고 - LogoState
 	- 게임의 제목이 등장하는 화면이다.
 	- 게임의 로고 화면, 'Press Any Key' 이미지
 	- 키보드 입력 - 메뉴화면으로 이동한다.
 	- 키보드 입력 - Titlestate로 이동

 2. 메뉴 선택 - TitleState
  	- 시작과 종료를 선택할 수 있는 메뉴 화면이다.
  	- 메뉴화면 배경, 'Game Start' 버튼, 'Exit' 버튼
  	- 'z' : 결정
  	  방향키 위아래 : 메뉴 이동 
  	- 'Game Start' 버튼 선택 - StageState로 이동

 3. 스테이지 - StageState
 	- 플레이어와 스테이지가 출력된다.
 	- 플레이어, 스테이지 타일, 함정, 몬스터, 상점, NPC
 	- 방향키 : 플레이어 이동
 	  'z' : 공격, 잡기
 	  'x' : 점프
 	  'a' : 폭탄
 	  's' : 로프
 	  'ESC'키 : 일시 정지, PauseState로 이동
 	- 플레이어 사망 - DieState로 이동 
 	  스테이지 클리어 - ResultState로 이동

 4. 결과 - ResultState
 	- 스테이지가 끝난 후 결과 출력
 	- 결과창, 플레이어 이동 애니메이션, 총점
 	- 'z'키 : 확인, StageState로 복귀
 5. 사망 - DieState
 	- 캐릭터 사망시 사망 원인 출력 
 	- 사망 결과창, 플레이어 현재 상황, 재시작 버튼, 메뉴로 이동 버튼
 	- 'z' : 결정
 	- 재시작 버튼 선택 - StageState로 이동 
 	  메뉴로 이동 버튼 - TitleState로 이동
 6. 일시 정지 - PauseState
 	- 진행중인 게임을 잠시 멈추고 메뉴를 출력
 	- 일시 정지 창, 메뉴로 이동 버튼, 끝내기 버튼, 재시작 버튼, 계속하기 버튼
 	- 'z' : 결정
 	  'ESC' : StageState로 복귀
  	  방향키 위아래 : 메뉴 이동 
 	- 스테이지에서 esc키를 입력시 출력

![Sheet](/기말 프로젝트/State.png)

## 4. 필요한 기술
- 애니메이션
- 시간에 따른 이벤트
- 키보드 입력
- 몬스터 인공지능
- 무작위적인 지형 생성
- 오브젝트