import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

app_title = "풀다운 푸드 코트"
RESOURCES_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources")
IMAGE_DIR = os.path.join(RESOURCES_DIR, "images")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
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
