# 풀다운 푸드 코트

음식점 메뉴를 보여주는 데스크톱 애플리케이션입니다.

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
