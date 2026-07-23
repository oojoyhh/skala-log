# SKALA Learning Log

> SKALA 과정에서 배우고 실습한 내용을 한곳에 기록하는 개인 학습 저장소입니다.

완성된 결과뿐 아니라 실습 과정, 시행착오, 새롭게 알게 된 내용을 꾸준히 남기는 것을 목표로 합니다.

## 학습 내용

| 폴더 | 내용 | 주요 기술 |
| --- | --- | --- |
| [`skala-intro`](./skala-intro/) | Hello World, SKALA 소개 페이지, 뉴스레터, 비밀번호 검증 흐름도 | Python, HTML, CSS, Mermaid.js |
| [`SKALA-HTML-Practice`](./SKALA-HTML-Practice/) | HTML 기본 태그, 목록, 이미지, 회원가입, 프로필 및 일과 페이지 실습 | HTML |
| [`skala-config-setup`](./skala-config-setup/) | Apple Silicon Mac용 SKALA 개발 환경 설치 자동화 | Bash, Homebrew |

## 저장소 구조

```text
sk-log/
├── skala-intro/
│   ├── hello_world.py
│   ├── index.html
│   ├── newsletter.html
│   └── password-mermaid.html
├── SKALA-HTML-Practice/
│   ├── SKALA-FRONT/html/
│   └── *.html
├── skala-config-setup/
│   └── skala-config-setup.sh
└── README.md
```

## 실행 방법

저장소를 내려받습니다.

```bash
git clone https://github.com/oojoyhh/sk-log.git
cd sk-log
```

HTML 파일은 브라우저에서 직접 열어 확인할 수 있습니다.

```bash
open skala-intro/index.html
open SKALA-HTML-Practice/SKALA-FRONT/html/index.html
```

Python 예제는 다음과 같이 실행합니다.

```bash
python3 skala-intro/hello_world.py
```

개발 환경 설치 스크립트는 Apple Silicon 기반 macOS를 대상으로 합니다. Homebrew, Git, JDK 21, Python 3.11, Node.js, PostgreSQL, VS Code, Docker Desktop 등 여러 도구를 설치하고 셸 설정을 변경하므로 내용을 먼저 확인한 뒤 실행해야 합니다.

```bash
cd skala-config-setup
./skala-config-setup.sh
```

## 기록 원칙

1. 수업이나 주제별로 폴더를 구분합니다.
2. 코드가 완벽하지 않아도 학습 과정이 드러나도록 남깁니다.
3. 비밀번호, API 키, `.env` 등 민감한 정보는 커밋하지 않습니다.
4. 의미 있는 단위로 커밋하고 메시지에 학습 내용을 적습니다.
5. 새로운 프로젝트를 추가하면 이 README의 학습 내용 표도 함께 갱신합니다.

## 커밋 메시지 예시

```text
study: HTML form 태그 실습
feat: 프로필 페이지 추가
fix: 잘못된 이미지 경로 수정
docs: 학습 내용 README 정리
chore: 개발 환경 설정 업데이트
```

---

작은 실습도 꾸준히 기록하며 성장합니다. 🌱
