# 풀다운 푸드 코트

음식점 메뉴를 보여주는 데스크톱 애플리케이션입니다.

## 프로젝트 구조
```
pulldown-food-court/
├── src/
│   ├── app.py          # 메인 애플리케이션 진입점
│   ├── ui/             # UI 관련 코드
│   │   ├── __init__.py
│   │   ├── main_window.py  # 메인 윈도우 UI 구현
│   │   └── menu_manager.py # 메뉴 시스템 관리
│   └── audio/          # 오디오 관련 코드
│       ├── __init__.py
│       └── audio_manager.py # 배경 환경음 및 효과음 재생 관리
├── resources/
│   ├── images/         # 메뉴 이미지 파일 (*.jpg)
│   └── audio/          # 오디오 파일 (ambient.mp3, 한식.mp3 등)
└── requirements.txt    # 프로젝트 의존성
```

## 주요 기능
- 메뉴바를 통한 음식 카테고리 및 메뉴 선택
- 선택한 메뉴의 이미지 표시
- 배경 환경음 재생
- 메뉴 선택 시 시스템 알림음 재생 (Windows/macOS 자동 감지)
- 카테고리가 변경될 때만 카테고리 음성 재생
- 프로그램 정보 보기
- 종료 확인 대화상자

## 필요한 리소스 파일
- `resources/images/`: 각 메뉴 항목의 이미지 파일 (예: 비빔밥.jpg, 김치찌개.jpg 등)
- `resources/audio/`:
  - `ambient.mp3`: 배경 환경음 파일
  - `한식.mp3`, `중식.mp3`, `일식.mp3` 등: 메뉴 카테고리 음성 파일

※ 이미지와 오디오 파일은 저작권 문제로 인해 저장소에 포함되어 있지 않습니다.
직접 준비하여 해당 디렉토리에 넣어주세요.

## 설치 방법

### macOS

1. Python 설치 (두 가지 방법 중 선택)
   - [Python 공식 웹사이트](https://www.python.org/downloads/)에서 Python 3.12 설치
   - 또는 Homebrew를 사용하여 설치:
     ```bash
     brew install python@3.12
     ```

2. 프로젝트 파일 준비
   - 이 저장소를 다운로드 또는 클론
   - `resources/images` 폴더에 메뉴 이미지 파일들이 있는지 확인
   - `resources/audio` 폴더에 ambient.mp3 파일과 카테고리 음성 파일들이 있는지 확인

3. 가상환경 생성 및 패키지 설치
   ```bash
   # 프로젝트 폴더에서
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. 프로그램 실행
   ```bash
   # 가상환경이 활성화된 상태에서
   python src/app.py
   ```

### Windows

1. Python 설치
   - [Python 공식 웹사이트](https://www.python.org/downloads/)에서 Python 3.12 설치
   - 설치 시 "Add Python to PATH" 옵션을 반드시 체크

2. 프로젝트 파일 준비
   - 이 저장소를 다운로드 또는 클론
   - `resources/images` 폴더에 메뉴 이미지 파일들이 있는지 확인
   - `resources/audio` 폴더에 ambient.mp3 파일과 카테고리 음성 파일들이 있는지 확인
   
3. 가상환경 생성 및 패키지 설치
   ```bash
   # 프로젝트 폴더에서
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. 프로그램 실행
   ```bash
   # 가상환경이 활성화된 상태에서
   python src/app.py
   ```

## 실행 파일 생성 및 배포

### Windows
Windows에서 실행 파일(.exe)을 생성하려면:
```bash
# 가상환경이 활성화된 상태에서
pyinstaller --noconsole --onefile src/app.py --name "풀다운 푸드 코트"
```
※ `--noconsole` 옵션은 실행 시 콘솔 창을 표시하지 않게 합니다.

### macOS
macOS에서 실행 파일을 생성하려면:
```bash
# 가상환경이 활성화된 상태에서
pyinstaller --onefile src/app.py --name "풀다운 푸드 코트"
```

### 배포 방법
1. `dist` 폴더에서 생성된 실행 파일을 찾습니다.
2. 다음과 같은 구조로 배포 폴더를 만듭니다:
   ```
   배포_폴더/
   ├── 풀다운 푸드 코트 (실행 파일)
   └── resources/
       ├── images/
       │   └── (이미지 파일들)
       └── audio/
           └── (오디오 파일들)
   ```
3. 실행 파일과 resources 폴더를 함께 배포합니다.

※ 주의사항:
- 실행 파일과 resources 폴더는 반드시 같은 위치에 있어야 합니다.
- resources 폴더가 없거나 필요한 파일이 없는 경우 프로그램이 실행되지 않습니다.

## 개발자 정보

### 프로젝트 구조 설명
- `src/app.py`: 애플리케이션의 진입점. UI와 오디오 컴포넌트를 초기화하고 연결
- `src/ui/main_window.py`: 메인 윈도우 UI 구현. 이미지 표시와 레이아웃 관리
- `src/ui/menu_manager.py`: 메뉴 시스템 관리. 메뉴 구조 정의 및 이벤트 처리
- `src/audio/audio_manager.py`: 배경 환경음 및 효과음 재생 관리. 음악 재생/정지 및 타이머 관리

### 모듈화된 구조의 장점
1. **관심사의 분리**: 각 모듈이 특정 기능에 집중
2. **코드 재사용성**: 각 컴포넌트를 독립적으로 재사용 가능
3. **유지보수성**: 기능별로 분리되어 있어 수정이 용이
4. **테스트 용이성**: 각 컴포넌트를 독립적으로 테스트 가능

## 라이선스
이 프로젝트는 MIT License를 따릅니다. 이는 다음과 같은 권한을 제공합니다:

- 이 소프트웨어를 무제한으로 사용, 복사, 수정, 병합, 게시, 배포, 판매할 수 있습니다.
- 이 소프트웨어를 제공받는 사람에게도 동일한 권한을 부여할 수 있습니다.
- 단, 모든 복제본에는 저작권 고지와 MIT 라이선스 전문을 포함해야 합니다.

자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
