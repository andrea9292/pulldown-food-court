from PySide6.QtWidgets import QMenuBar, QMenu, QMessageBox
from typing import Dict, List, Callable
from functools import partial

class MenuManager:
    def __init__(self, parent_window):
        """메뉴 관리자 초기화
        
        Args:
            parent_window: 메뉴바를 포함할 부모 윈도우
        """
        self.parent = parent_window
        self.menubar = parent_window.menuBar()
        self.category_map = {}  # 메뉴 항목에서 카테고리로의 매핑 캐시
        
        # 메뉴 카테고리와 항목들
        self.categories = {
            "한식": ["비빔밥", "김치찌개", "된장찌개", "불고기"],
            "중식": ["짜장면", "짬뽕", "탕수육", "마파두부"],
            "분식": ["떡볶이", "순대", "튀김", "라면"],
            "일식": ["초밥", "라멘", "돈까스", "우동"],
            "양식": ["파스타", "스테이크", "피자", "샐러드"],
            "설정": ["환경음"],
            "푸드코트": ["푸드코트 정보...", "나가기"]
        }
        
        # 카테고리 맵 초기화
        self._init_category_map()
    
    def _init_category_map(self):
        """메뉴 항목에서 카테고리로의 매핑 생성"""
        for category, items in self.categories.items():
            for item in items:
                self.category_map[item] = category
    
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
            if item == "환경음":
                action = menu.addAction(item)
                action.setCheckable(True)
                action.setChecked(self.parent.audio_manager.is_ambient_enabled())
                action.triggered.connect(self.toggle_ambient_sound)
            else:
                action = menu.addAction(item)
                if item == "푸드코트 정보...":
                    action.triggered.connect(self.show_about_dialog)
                elif item == "나가기":
                    action.triggered.connect(self.close_application)
                else:
                    # 람다 함수 대신 부분 함수 사용 (성능 개선)
                    action.triggered.connect(
                        partial(self._handle_menu_click, item, menu_click_handler)
                    )
    
    def _handle_menu_click(self, item, handler, checked=False):
        """메뉴 클릭 핸들러 (람다 대신 사용)"""
        handler(item)

    def get_category_for_item(self, menu_item: str) -> str:
        """메뉴 항목에 해당하는 카테고리를 반환
        
        Args:
            menu_item: 카테고리를 찾을 메뉴 항목
            
        Returns:
            str: 메뉴 항목의 카테고리. 찾지 못한 경우 None
        """
        # 캐시된 매핑 사용
        return self.category_map.get(menu_item, None)
    
    def show_about_dialog(self):
        """푸드코트 정보 대화상자 표시"""
        about_text = (
            "풀다운 푸드 코트 v1.0\n\n"
            "제작: Andrea Kim 팀\n"
            "저작권: 2025 Andrea Kim\n\n"
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

    def toggle_ambient_sound(self):
        """환경음 On/Off 토글"""
        is_enabled = self.parent.audio_manager.toggle_ambient_sound()
        # 메뉴바에서 환경음 액션 찾기
        settings_menu = self.menubar.findChild(QMenu, "설정")
        if settings_menu:
            ambient_action = settings_menu.actions()[0]  # 첫 번째 액션이 환경음
            ambient_action.setChecked(is_enabled)
