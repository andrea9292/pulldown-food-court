import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QLabel, QVBoxLayout, 
                             QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from .menu_manager import MenuManager

class MainWindow(QMainWindow):
    def __init__(self, app_title, image_dir, audio_manager):
        """메인 윈도우 초기화
        
        Args:
            app_title (str): 애플리케이션 제목
            image_dir (str): 이미지 파일이 있는 디렉토리 경로
            audio_manager (AudioManager): 오디오 관리자 인스턴스
        """
        super().__init__()
        self.app_title = app_title
        self.image_dir = image_dir
        self.audio_manager = audio_manager
        
        # UI 초기화
        self.init_ui()
        
        # 배경음악 시작
        self.audio_manager.play_background_music(self)

    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle(self.app_title)
        
        # 메뉴 관리자 생성 및 메뉴 초기화
        self.menu_manager = MenuManager(self)
        self.menu_manager.create_menus(self.menu_clicked)
        
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
        self.setGeometry(100, 100, 800, 600)

    def closeEvent(self, event):
        """윈도우가 닫힐 때 호출되는 메서드"""
        self.audio_manager.cleanup()
        event.accept()

    def set_default_image(self):
        """기본 이미지 설정"""
        self.image_label.setText("이미지가 없습니다")

    def load_menu_image(self, menu_item):
        """메뉴에 해당하는 이미지 로드"""
        image_path = os.path.join(self.image_dir, f"{menu_item}.jpg")
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
