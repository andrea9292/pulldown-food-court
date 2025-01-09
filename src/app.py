import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
import pygame

app_title = "풀다운 푸드 코트"
RESOURCES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")
IMAGE_DIR = os.path.join(RESOURCES_DIR, "images")
AUDIO_DIR = os.path.join(RESOURCES_DIR, "audio")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bgm_length = 0
        self.init_audio()
        self.init_ui()
    
    def init_audio(self):
        """배경음 초기화"""
        pygame.mixer.init()
        bgm_path = os.path.join(AUDIO_DIR, "background.mp3")
        if os.path.exists(bgm_path):
            # 음악의 총 길이(초) 구하기
            sound = pygame.mixer.Sound(bgm_path)
            self.bgm_length = sound.get_length()
            
            # 시작 1초부터 재생
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.play(-1, start=1.0)
            
            # 타이머를 사용하여 끝나기 1초 전에 다시 시작
            self.bgm_timer = QTimer(self)
            # 음악이 끝나기 1.1초 전에 타이머 실행 (약간의 여유를 둠)
            interval = (self.bgm_length - 2.1) * 1000  # 밀리초 단위로 변환
            self.bgm_timer.setInterval(int(interval))
            self.bgm_timer.timeout.connect(self.restart_bgm)
            self.bgm_timer.start()
        else:
            print(f"배경음 파일을 찾을 수 없습니다: {bgm_path}")
    
    def restart_bgm(self):
        """배경음을 1초 지점부터 다시 시작"""
        pygame.mixer.music.play(-1, start=1.0)
    
    def closeEvent(self, event):
        """윈도우가 닫힐 때 호출되는 메서드"""
        if hasattr(self, 'bgm_timer'):
            self.bgm_timer.stop()
        pygame.mixer.music.stop()
        pygame.mixer.quit()
        event.accept()
    
    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle(app_title)
        
        # 메뉴바 생성
        menubar = self.menuBar()
        
        # 각 음식 카테고리별 메뉴 생성
        categories = {
            "한식": ["비빔밥", "김치찌개", "된장찌개", "불고기"],
            "중식": ["짜장면", "짬뽕", "탕수육", "마파두부"],
            "분식": ["떡볶이", "순대", "튀김", "라면"],
            "일식": ["초밥", "라멘", "돈까스", "우동"],
            "양식": ["파스타", "스테이크", "피자", "샐러드"]
        }
        
        for category, items in categories.items():
            # 메인 메뉴 추가
            menu = menubar.addMenu(category)
            
            # 서브메뉴 아이템 추가
            for item in items:
                action = menu.addAction(item)
                action.triggered.connect(lambda checked, x=item: self.menu_clicked(x))
        
        # 중앙 위젯 설정
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)  # 여백 줄이기
        layout.setSpacing(5)  # 위젯 간 간격 줄이기
        central_widget.setLayout(layout)
        
        # 이미지를 표시할 라벨
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.image_label)
        
        # 선택된 메뉴를 표시할 라벨
        self.selected_label = QLabel("메뉴를 선택해주세요")
        self.selected_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.selected_label)
        
        # 기본 이미지 설정
        self.set_default_image()
        
        # 윈도우 크기 설정
        self.setMinimumSize(800, 600)
        self.setGeometry(100, 100, 800, 600)  # x, y, width, height
    
    def set_default_image(self):
        """기본 이미지 설정"""
        self.image_label.setText("이미지가 없습니다")
    
    def load_menu_image(self, menu_item):
        """메뉴에 해당하는 이미지 로드"""
        image_path = os.path.join(IMAGE_DIR, f"{menu_item}.jpg")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            # 이미지 크기를 더 크게 조정 (700x500)
            scaled_pixmap = pixmap.scaled(700, 500, Qt.AspectRatioMode.KeepAspectRatio, 
                                        Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
        else:
            self.image_label.setText(f"'{menu_item}' 이미지를 찾을 수 없습니다")
    
    def menu_clicked(self, menu_item):
        """메뉴 아이템이 선택되었을 때 호출되는 메서드"""
        self.selected_label.setText(f"선택된 메뉴: {menu_item}")
        self.load_menu_image(menu_item)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
