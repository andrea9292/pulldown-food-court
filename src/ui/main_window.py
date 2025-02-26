import os
from PySide6.QtWidgets import (QMainWindow, QWidget, QLabel, QVBoxLayout, 
                             QMessageBox)
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QPixmap
from .menu_manager import MenuManager

class ImageLoader(QThread):
    """이미지 로딩을 위한 워커 스레드"""
    image_loaded = Signal(object)  # 이미지 로딩이 완료되면 QPixmap을 전달
    load_error = Signal(str)    # 에러 발생 시 에러 메시지 전달
    
    def __init__(self, image_path):
        super().__init__()
        self.image_path = image_path
        
    def run(self):
        """이미지 로딩 작업 실행"""
        try:
            if not os.path.exists(self.image_path):
                raise FileNotFoundError(f"이미지를 찾을 수 없습니다: {os.path.basename(self.image_path)}")
                
            pixmap = QPixmap(self.image_path)
            if pixmap.isNull():
                raise ValueError("이미지를 로드할 수 없습니다")
                
            # 이미지 크기를 조정 (700x500)
            scaled_pixmap = pixmap.scaled(700, 500, 
                                        Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)
            self.image_loaded.emit(scaled_pixmap)
        except Exception as e:
            self.load_error.emit(str(e))

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
        self.image_loader = None  # 이미지 로더 
        self.image_cache = {}  # 이미지 캐시 추가
        
        # UI 초기화
        self.init_ui()
        
        # 배경 환경음 시작 - 비동기로 시작하여 UI 초기화 지연 방지
        QThread.currentThread().msleep(100)  # UI가 먼저 표시되도록 약간 지연
        self.audio_manager.play_ambient_sound("ambient.mp3", self)

    def init_ui(self):
        """UI 초기화"""
        self.setWindowTitle(self.app_title)
        
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
        self.image_label.setText("메뉴를 선택해주세요")  # 초기 텍스트
        self.image_label.setStyleSheet("QLabel { font-size: 14px; }")
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
        
        # 메뉴 관리자 생성 및 메뉴 초기화 - UI 초기화 후 메뉴 생성
        self.menu_manager = MenuManager(self)
        self.menu_manager.create_menus(self.menu_clicked)

    def closeEvent(self, event):
        """윈도우가 닫힐 때 호출되는 메서드"""
        self.audio_manager.cleanup()
        event.accept()

    def set_default_image(self):
        """기본 이미지 설정"""
        self.image_label.setText("이미지가 없습니다")
        self.image_label.setStyleSheet("QLabel { font-size: 14px; }")

    def load_menu_image(self, menu_item):
        """메뉴에 해당하는 이미지 비동기 로드"""
        # 캐시에 이미지가 있는지 확인
        if menu_item in self.image_cache:
            self.on_image_loaded(self.image_cache[menu_item])
            return
            
        # 이전 로더가 있다면 중지
        if self.image_loader and self.image_loader.isRunning():
            self.image_loader.terminate()
            self.image_loader.wait()
        
        # 로딩 중임을 표시
        self.image_label.setText("이미지 로딩 중...")
        self.image_label.setStyleSheet("QLabel { font-size: 14px; }")
        
        # 새로운 이미지 로더 생성 및 시작
        image_path = os.path.join(self.image_dir, f"{menu_item}.jpg")
        self.image_loader = ImageLoader(image_path)
        self.image_loader.image_loaded.connect(lambda pixmap: self.cache_and_display_image(menu_item, pixmap))
        self.image_loader.load_error.connect(self.on_image_error)
        self.image_loader.start()

    def cache_and_display_image(self, menu_item, pixmap):
        """이미지를 캐시에 저장하고 표시"""
        self.image_cache[menu_item] = pixmap
        self.on_image_loaded(pixmap)

    def on_image_loaded(self, pixmap):
        """이미지 로딩이 완료되면 호출"""
        self.image_label.setPixmap(pixmap)
        self.image_label.setStyleSheet("")  # 기본 스타일로 복원
    
    def on_image_error(self, error_message):
        """이미지 로딩 실패 시 호출"""
        self.image_label.setText(error_message)
        self.image_label.setStyleSheet("QLabel { font-size: 14px; color: red; }")

    def menu_clicked(self, menu_item):
        """메뉴 아이템이 선택되었을 때 호출되는 메서드"""
        self.selected_label.setText(f"선택된 메뉴: {menu_item}")
        
        # 시스템 알림음 재생
        self.audio_manager.play_system_notification()
        
        # MenuManager를 통해 메뉴 카테고리 확인
        self.current_category = self.menu_manager.get_category_for_item(menu_item)
        
        # 카테고리가 있고, 이전 카테고리와 다른 경우만 음성 재생
        if self.current_category and self.current_category != self.previous_category:
            self.audio_manager.play_category_sound(self.current_category)
            self.previous_category = self.current_category
        
        # 이미지 로딩 시작 (비동기)
        self.load_menu_image(menu_item)

    def toggle_ambient_sound(self):
        """환경음 On/Off 토글"""
        is_enabled = self.audio_manager.toggle_ambient_sound()
        # self.ambient_action.setChecked(is_enabled)  # Removed this line
