# 풀다운 푸드 코트

음식점 메뉴를 보여주는 데스크톱 애플리케이션입니다.

## 프로젝트 구조
```
pulldown-food-court/
├── src/
│   └── app.py          # 메인 애플리케이션 파일
├── resources/
│   ├── images/         # 메뉴 이미지 파일 (*.jpg)
│   └── audio/          # 배경음악 파일 (background.mp3)
└── requirements.txt    # 프로젝트 의존성
```

## 필요한 리소스 파일
- `resources/images/`: 각 메뉴 항목의 이미지 파일 (예: 비빔밥.jpg, 김치찌개.jpg 등)
- `resources/audio/background.mp3`: 배경음악 파일

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
   - `resources/audio` 폴더에 background.mp3 파일이 있는지 확인

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
   - `resources/audio` 폴더에 background.mp3 파일이 있는지 확인
   
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

## 실행 파일 생성 (선택사항)

### Windows
Windows에서 실행 파일(.exe)을 생성하려면:
```bash
# 가상환경이 활성화된 상태에서
pyinstaller --onefile --windowed src/app.py
```

### macOS
macOS에서 앱 번들(.app)을 생성하려면:
```bash
# 가상환경이 활성화된 상태에서
pyinstaller --onefile --windowed --name "풀다운 푸드 코트" src/app.py
```

생성된 실행 파일은 `dist` 폴더에서 찾을 수 있습니다.
