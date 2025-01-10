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
        self.previous_category = None  # 이전에 선택된 카테고리 저장
        self.current_category = None  # 항목을 선택한 카테고리 저장

        
        # UI 초기화
        self.init_ui()
        
        # 배경 환경음 시작
        self.audio_manager.play_ambient_sound("ambient.mp3", self)

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
        self.image_label.setMinimumSize(700, 500)  # 최소 크기 설정        
        layout.addWidget(self.image_label)
        
        # 선택된 메뉴를 표시할 라벨
        self.selected_label = QLabel("메뉴를 선택해주세요")
        self.selected_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.selected_label.setStyleSheet("QLabel { padding: 10px; }")  # 패딩 추가
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
        self.image_label.setStyleSheet("QLabel { font-size: 14px; }")

    def load_menu_image(self, menu_item):
        """메뉴에 해당하는 이미지 로드"""
        image_path = os.path.join(self.image_dir, f"{menu_item}.jpg")
        if os.path.exists(image_path):
            pixmap = QPixmap(image_path)
            # 이미지 크기를 조정 (700x500)
            scaled_pixmap = pixmap.scaled(700, 500, Qt.AspectRatioMode.KeepAspectRatio, 
                                        Qt.TransformationMode.SmoothTransformation)
            self.image_label.setPixmap(scaled_pixmap)
        else:
            self.image_label.setText(f"'{menu_item}' 이미지를 찾을 수 없습니다")

    def menu_clicked(self, menu_item):
        """메뉴 아이템이 선택되었을 때 호출되는 메서드"""
        self.selected_label.setText(f"선택된 메뉴: {menu_item}")
        self.load_menu_image(menu_item)
        
        # 시스템 알림음 재생
        self.audio_manager.play_system_notification()
        
        # MenuManager를 통해 메뉴 카테고리 확인
        self.current_category = self.menu_manager.get_category_for_item(menu_item)
        
        # 카테고리가 있고, 이전 카테고리와 다를 때만 음성 재생
        if self.current_category and self.current_category != self.previous_category:
            self.audio_manager.play_category_sound(self.current_category)
            self.previous_category = self.current_category
