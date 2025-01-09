import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QLabel, QVBoxLayout, 
                             QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

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
        
        # 메뉴바 생성
        menubar = self.menuBar()
        
        # 각 음식 카테고리별 메뉴 생성
        categories = {
            "한식": ["비빔밥", "김치찌개", "된장찌개", "불고기"],
            "중식": ["짜장면", "짬뽕", "탕수육", "마파두부"],
            "분식": ["떡볶이", "순대", "튀김", "라면"],
            "일식": ["초밥", "라멘", "돈까스", "우동"],
            "양식": ["파스타", "스테이크", "피자", "샐러드"],
            "푸드코트": ["푸드코트 정보...", "나가기"]
        }
        
        for category, items in categories.items():
            # 메인 메뉴 추가
            menu = menubar.addMenu(category)
            
            # 서브메뉴 아이템 추가
            for item in items:
                action = menu.addAction(item)
                if item == "푸드코트 정보...":
                    action.triggered.connect(self.show_about_dialog)
                elif item == "나가기":
                    action.triggered.connect(self.close_application)
                else:
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
        self.setGeometry(100, 100, 800, 600)

    def show_about_dialog(self):
        """푸드코트 정보 대화상자 표시"""
        about_text = (
            "풀다운 푸드 코트 v1.0\n\n"
            "제작: 코드이움 팀\n"
            "저작권: 2025 Codeium\n\n"
            "음식점 메뉴를 쉽게 둘러볼 수 있는\n"
            "데스크톱 애플리케이션입니다."
        )
        QMessageBox.about(self, "프로그램 정보", about_text)

    def close_application(self):
        """나가기 전 확인 대화상자 표시"""
        reply = QMessageBox.question(
            self, "종료 확인", 
            "정말 나가시겠어요?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.close()

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
