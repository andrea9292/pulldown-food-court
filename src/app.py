import sys
import os
from PySide6.QtWidgets import QApplication, QSplashScreen
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer
from ui.main_window import MainWindow
from audio.audio_manager import AudioManager

# 리소스 경로 캐싱
_resource_path = None

def get_resource_path():
    """리소스 디렉토리 경로를 반환합니다.
    1. 개발 환경: 프로젝트 루트의 resources 디렉토리
    2. 배포 환경: 실행 파일이 있는 디렉토리의 resources 디렉토리"""
    global _resource_path
    
    # 캐시된 경로가 있으면 반환
    if _resource_path is not None:
        return _resource_path
        
    if getattr(sys, 'frozen', False):
        # 실행 파일이 있는 디렉토리
        base_path = os.path.dirname(sys.executable)
    else:
        # 개발 환경에서는 프로젝트 루트 디렉토리
        base_path = os.path.dirname(os.path.dirname(__file__))
    
    resources_path = os.path.join(base_path, "resources")
    if not os.path.exists(resources_path):
        print(f"리소스 디렉토리를 찾을 수 없습니다: {resources_path}")
        print("실행 파일과 같은 위치에 resources 디렉토리가 있는지 확인해주세요.")
        sys.exit(1)
        
    # 경로 캐싱
    _resource_path = resources_path
    return resources_path

app_title = "풀다운 푸드 코트"
RESOURCES_DIR = get_resource_path()
IMAGE_DIR = os.path.join(RESOURCES_DIR, "images")
AUDIO_DIR = os.path.join(RESOURCES_DIR, "audio")

def main():
    app = QApplication(sys.argv)
    
    # 스플래시 화면 표시 (로딩 중 표시)
    splash_path = os.path.join(IMAGE_DIR, "splash.jpg")
    splash = None
    if os.path.exists(splash_path):
        splash_pixmap = QPixmap(splash_path)
        splash = QSplashScreen(splash_pixmap)
        splash.show()
        app.processEvents()
    
    # 오디오 매니저 초기화
    audio_manager = AudioManager(AUDIO_DIR)
    
    # 메인 윈도우 생성
    window = MainWindow(app_title, IMAGE_DIR, audio_manager)
    
    # 스플래시 화면이 있으면 잠시 후 메인 윈도우 표시
    if splash:
        QTimer.singleShot(1000, lambda: _finish_loading(window, splash))
    else:
        window.show()
    
    return app.exec()

def _finish_loading(window, splash):
    """스플래시 화면을 닫고 메인 윈도우 표시"""
    window.show()
    splash.finish(window)

if __name__ == "__main__":
    sys.exit(main())
