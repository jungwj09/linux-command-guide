# Linux Command Guide

> Linux 명령어를 학습 중인 학생 및 초보자를 위한 Flask 기반 웹 서비스입니다. <br />
자주 사용하는 Linux 명령어를 검색하고, 상세 설명과 예제를 확인하고, 로그인 후 즐겨찾기로 등록할 수 있습니다.

## 주요 기능

- Linux 명령어 목록 조회 및 검색
- 명령어 상세 설명 및 사용 예제 확인
- 로그인 / 로그아웃 (세션 기반)
- 로그인한 사용자의 즐겨찾기 등록 및 조회
- 사용자 프로필(즐겨찾기 개수) 확인

## 기술 스택

- Python 3
- Flask 3
- Jinja2 (템플릿 엔진)
- HTML / CSS

## 설치 및 실행 방법

```bash
# 1. 저장소 클론
git clone <repository-url>
cd linux-command-guide

# 2. 가상환경 생성 및 활성화
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 서버 실행
python app.py
```

서버가 실행되면 브라우저에서 `http://127.0.0.1:5000` 으로 접속하세요.

## URL 라우팅

| URL 경로 | 메서드 | 연결 함수 | 설명 |
| --- | --- | --- | --- |
| `/` | GET | `index()` | 메인 페이지 |
| `/login` | GET, POST | `login()` | 로그인 처리 및 세션 생성 |
| `/logout` | GET | `logout()` | 세션 삭제 후 메인 페이지로 이동 |
| `/commands` | GET | `command_list()` | 명령어 목록 조회 및 키워드 검색(`?keyword=`) |
| `/command/<name>` | GET | `command_detail()` | 명령어 상세 조회 |
| `/favorite/<name>` | GET | `add_favorite()` | 즐겨찾기 추가 (로그인 필요) |
| `/favorites` | GET | `favorites()` | 즐겨찾기 목록 조회 (로그인 필요) |
| `/profile` | GET | `profile()` | 로그인 사용자 프로필(즐겨찾기 개수) 조회 |

## 세션 설계

- `session["user"]` : 로그인한 사용자의 아이디를 저장합니다.
- `session["favorites"]` : 로그인한 사용자가 등록한 즐겨찾기 명령어 이름 목록을 저장합니다.
- 로그인하지 않은 상태로 즐겨찾기 관련 페이지(`/favorite/<name>`, `/favorites`, `/profile`)에 접근하면 로그인 페이지로 리다이렉트됩니다.

## 디렉토리 구조

```
linux-command-guide/
├── app.py                  # Flask 메인 서버 및 라우팅
├── requirements.txt        # 프로젝트 의존성 목록
├── static/
│   └── css/
│       └── style.css       # 전체 페이지 스타일
└── templates/
    ├── base.html           # 공통 레이아웃 (헤더, 네비게이션)
    ├── index.html          # 메인 페이지
    ├── login.html          # 로그인 페이지
    ├── commands.html       # 명령어 목록 및 검색 페이지
    ├── command_detail.html # 명령어 상세 페이지
    ├── favorites.html      # 즐겨찾기 목록 페이지
    └── profile.html        # 사용자 프로필 페이지
```

## 참고

- 명령어 데이터(`commands`)는 데이터베이스가 아닌 `app.py` 내부 리스트로 관리되며, 서버를 재시작하면 추가/삭제 내용 없이 초기 상태로 돌아갑니다.
- 즐겨찾기 데이터는 세션에 저장되므로 브라우저 세션이 종료되거나 로그아웃하면 사라집니다.
- `app.secret_key`는 개발용 예시 값입니다.
