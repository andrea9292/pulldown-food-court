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
        self.ambient_length = 0
        self.ambient_timer = None
        
        # pygame 믹서 초기화 (효과음을 위한 채널 1개 설정)
        pygame.mixer.init()
        pygame.mixer.set_num_channels(1)
        
        # 효과음 전용 채널
        self.effect_channel = pygame.mixer.Channel(0)

    def play_ambient_sound(self, filename, parent=None):
        """배경 환경음 재생
        
        Args:
            filename (str): 재생할 환경음 파일명 (예: ambient.mp3)
            parent: QTimer를 위한 부모 객체 (보통 MainWindow)
        """
        ambient_path = os.path.join(self.audio_dir, filename)
        if not os.path.exists(ambient_path):
            print(f"배경 환경음 파일을 찾을 수 없습니다: {ambient_path}")
            return

        # 환경음의 총 길이(초) 구하기
        sound = pygame.mixer.Sound(ambient_path)
        self.ambient_length = sound.get_length()
        
        # 배경 환경음 재생 (mixer.music 사용)
        pygame.mixer.music.load(ambient_path)
        pygame.mixer.music.play(-1, start=1.0)
        
        if parent:
            # 타이머를 사용하여 끝나기 1초 전에 다시 시작
            self.ambient_timer = QTimer(parent)
            # 환경음이 끝나기 1.1초 전에 타이머 실행 (약간의 여유를 둠)
            interval = (self.ambient_length - 2.1) * 1000  # 밀리초 단위로 변환
            self.ambient_timer.setInterval(int(interval))
            self.ambient_timer.timeout.connect(self.restart_ambient)
            self.ambient_timer.start()

    def restart_ambient(self):
        """배경 환경음을 1초 지점부터 다시 시작"""
        pygame.mixer.music.play(-1, start=1.0)

    def play_category_sound(self, category):
        """메뉴 카테고리에 해당하는 음성 재생
        
        Args:
            category (str): 메뉴 카테고리 (예: 한식, 중식, 일식)
        """
        sound_path = os.path.join(self.audio_dir, f"{category}.mp3")
        if not os.path.exists(sound_path):
            print(f"효과음 파일을 찾을 수 없습니다: {sound_path}")
            return
            
        # 이전에 재생 중이던 효과음 중지
        self.effect_channel.stop()
        
        # 효과음 채널에서 새로운 효과음 재생 (-1은 무한 반복)
        sound = pygame.mixer.Sound(sound_path)
        self.effect_channel.play(sound, loops=-1)

    def cleanup(self):
        """오디오 리소스 정리"""
        if self.ambient_timer:
            self.ambient_timer.stop()
        pygame.mixer.music.stop()
        self.effect_channel.stop()
        pygame.mixer.quit()
