import sys
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from audio.audio_manager import AudioManager

app_title = "풀다운 푸드 코트"
RESOURCES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")
IMAGE_DIR = os.path.join(RESOURCES_DIR, "images")
AUDIO_DIR = os.path.join(RESOURCES_DIR, "audio")

def main():
    app = QApplication(sys.argv)
    
    # 오디오 매니저 초기화
    audio_manager = AudioManager(AUDIO_DIR)
    
    # 메인 윈도우 생성
    window = MainWindow(app_title, IMAGE_DIR, audio_manager)
    window.show()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
