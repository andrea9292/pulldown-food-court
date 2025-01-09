from PySide6.QtWidgets import QMenuBar, QMenu, QMessageBox
from typing import Dict, List, Callable

class MenuManager:
    def __init__(self, parent_window):
        """메뉴 관리자 초기화
        
        Args:
            parent_window: 메뉴바를 포함할 부모 윈도우
        """
        self.parent = parent_window
        self.menubar = parent_window.menuBar()
        
        # 메뉴 카테고리와 항목들
        self.categories = {
            "한식": ["비빔밥", "김치찌개", "된장찌개", "불고기"],
            "중식": ["짜장면", "짬뽕", "탕수육", "마파두부"],
            "분식": ["떡볶이", "순대", "튀김", "라면"],
            "일식": ["초밥", "라멘", "돈까스", "우동"],
            "양식": ["파스타", "스테이크", "피자", "샐러드"],
            "푸드코트": ["푸드코트 정보...", "나가기"]
        }
    
    def create_menus(self, menu_click_handler: Callable[[str], None]):
        """메뉴바에 모든 메뉴 항목을 생성
        
        Args:
            menu_click_handler: 일반 메뉴 항목 클릭 시 호출될 핸들러 함수
        """
        for category, items in self.categories.items():
            menu = self.menubar.addMenu(category)
            self._add_menu_items(menu, items, menu_click_handler)
    
    def _add_menu_items(self, menu: QMenu, items: List[str], 
                       menu_click_handler: Callable[[str], None]):
        """메뉴에 항목들을 추가
        
        Args:
            menu: 항목을 추가할 메뉴
            items: 추가할 메뉴 항목들의 리스트
            menu_click_handler: 일반 메뉴 항목 클릭 시 호출될 핸들러 함수
        """
        for item in items:
            action = menu.addAction(item)
            if item == "푸드코트 정보...":
                action.triggered.connect(self.show_about_dialog)
            elif item == "나가기":
                action.triggered.connect(self.close_application)
            else:
                action.triggered.connect(
                    lambda checked, x=item: menu_click_handler(x)
                )
    
    def show_about_dialog(self):
        """푸드코트 정보 대화상자 표시"""
        about_text = (
            "풀다운 푸드 코트 v1.0\n\n"
            "제작: 코드이움 팀\n"
            "저작권: © 2025 Codeium\n\n"
            "음식점 메뉴를 쉽게 둘러볼 수 있는\n"
            "데스크톱 애플리케이션입니다."
        )
        QMessageBox.about(self.parent, "프로그램 정보", about_text)
    
    def close_application(self):
        """나가기 전 확인 대화상자 표시"""
        reply = QMessageBox.question(
            self.parent, "종료 확인", 
            "정말 나가시겠어요?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.parent.close()
