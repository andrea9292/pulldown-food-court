import os
import pygame
from PySide6.QtCore import QTimer

class AudioManager:
    def __init__(self, audio_dir):
        """오디오 매니저 초기화
        
        Args:
            audio_dir (str): 오디오 파일이 있는 디렉토리 경로
        """
        self.audio_dir = audio_dir
        self.bgm_length = 0
        self.bgm_timer = None
        pygame.mixer.init()

    def play_background_music(self, parent=None):
        """배경음악 재생
        
        Args:
            parent: QTimer를 위한 부모 객체 (보통 MainWindow)
        """
        bgm_path = os.path.join(self.audio_dir, "background.mp3")
        if not os.path.exists(bgm_path):
            print(f"배경음 파일을 찾을 수 없습니다: {bgm_path}")
            return

        # 음악의 총 길이(초) 구하기
        sound = pygame.mixer.Sound(bgm_path)
        self.bgm_length = sound.get_length()
        
        # 시작 1초부터 재생
        pygame.mixer.music.load(bgm_path)
        pygame.mixer.music.play(-1, start=1.0)
        
        if parent:
            # 타이머를 사용하여 끝나기 1초 전에 다시 시작
            self.bgm_timer = QTimer(parent)
            # 음악이 끝나기 1.1초 전에 타이머 실행 (약간의 여유를 둠)
            interval = (self.bgm_length - 2.1) * 1000  # 밀리초 단위로 변환
            self.bgm_timer.setInterval(int(interval))
            self.bgm_timer.timeout.connect(self.restart_bgm)
            self.bgm_timer.start()

    def restart_bgm(self):
        """배경음을 1초 지점부터 다시 시작"""
        pygame.mixer.music.play(-1, start=1.0)

    def cleanup(self):
        """오디오 리소스 정리"""
        if self.bgm_timer:
            self.bgm_timer.stop()
        pygame.mixer.music.stop()
        pygame.mixer.quit()
