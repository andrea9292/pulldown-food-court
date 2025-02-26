import os
import pygame
from PySide6.QtCore import QTimer
import platform

# 운영체제별 필요한 모듈 import
system = platform.system()
if system == "Darwin":  # macOS
    import subprocess
elif system == "Windows":  # Windows
    import winsound

class AudioManager:
    def __init__(self, audio_dir):
        """오디오 매니저 초기화
        
        Args:
            audio_dir (str): 오디오 파일이 있는 디렉토리 경로
        """
        self.audio_dir = audio_dir
        self.ambient_length = 0 # 환경음 길이
        self.ambient_timer = None # 환경음 시간
        self.ambient_enabled = True # 환경음 활성화 상태
        self.sound_cache = {}  # 사운드 캐시 추가
        
        # pygame 믹서 초기화 (효과음을 위한 채널 1개 설정)
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.set_num_channels(1)
        
        # 효과음 전용 채널
        self.effect_channel = pygame.mixer.Channel(0)

    def _load_sound(self, filename):
        """사운드 파일을 로드하고 캐싱
        
        Args:
            filename (str): 로드할 사운드 파일명
            
        Returns:
            pygame.mixer.Sound: 로드된 사운드 객체 또는 None
        """
        if filename in self.sound_cache:
            return self.sound_cache[filename]
            
        sound_path = os.path.join(self.audio_dir, filename)
        if not os.path.exists(sound_path):
            print(f"사운드 파일을 찾을 수 없습니다: {sound_path}")
            return None
            
        sound = pygame.mixer.Sound(sound_path)
        self.sound_cache[filename] = sound
        return sound

    def play_ambient_sound(self, filename, parent=None):
        """배경 환경음 재생
        
        Args:
            filename (str): 재생할 환경음 파일명 (예: ambient.mp3)
            parent: QTimer를 위한 부모 객체 (보통 MainWindow)
        """
        if not self.ambient_enabled:
            return

        sound = self._load_sound(filename)
        if not sound:
            return
            
        # 환경음의 총 길이(초) 구하기
        self.ambient_length = sound.get_length()
        
        # 배경 환경음 재생 (mixer.music 사용)
        ambient_path = os.path.join(self.audio_dir, filename)
        pygame.mixer.music.load(ambient_path)
        pygame.mixer.music.play(-1, start=1.0)
        
        if parent:
            # 타이머를 사용하여 끝나기 1초 전에 다시 시작
            if self.ambient_timer:
                self.ambient_timer.stop()
                
            self.ambient_timer = QTimer(parent)
            # 환경음이 끝나기 1.1초 전에 타이머 실행 (약간의 여유를 둠)
            interval = (self.ambient_length - 2.1) * 1000  # 밀리초 단위로 변환
            self.ambient_timer.setInterval(int(max(100, interval)))  # 최소 100ms 보장
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
        sound_filename = f"{category}.mp3"
        sound = self._load_sound(sound_filename)
        if not sound:
            return
            
        # 이전에 재생 중이던 효과음 중지
        self.effect_channel.stop()
        
        # 효과음 채널에서 새로운 효과음 재생 (-1은 무한 반복)
        self.effect_channel.play(sound, loops=-1)  # 무한 반복으로 변경

    def play_system_notification(self):
        """시스템 알림음(Notification) 재생
        Windows와 macOS 모두 지원"""
        system = platform.system()
        if system == "Darwin":  # macOS
            try:
                subprocess.run(["afplay", "/System/Library/Sounds/Tink.aiff"])
            except (FileNotFoundError, subprocess.SubprocessError):
                print("macOS에서 알림음을 재생할 수 없습니다.")
        elif system == "Windows":  # Windows
            try:
                winsound.PlaySound("SystemDefault", winsound.SND_ALIAS)
            except Exception:
                print("Windows에서 알림음을 재생할 수 없습니다.")

    def toggle_ambient_sound(self):
        """환경음 On/Off 토글"""
        self.ambient_enabled = not self.ambient_enabled
        if self.ambient_enabled:
            # 환경음 다시 시작
            pygame.mixer.music.play(-1, start=1.0)
            if self.ambient_timer:
                self.ambient_timer.start()
        else:
            # 환경음 중지
            pygame.mixer.music.stop()
            if self.ambient_timer:
                self.ambient_timer.stop()
        return self.ambient_enabled

    def is_ambient_enabled(self):
        """환경음 활성화 상태 반환"""
        return self.ambient_enabled

    def cleanup(self):
        """오디오 리소스 정리"""
        if self.ambient_timer:
            self.ambient_timer.stop()
        pygame.mixer.music.stop()
        self.effect_channel.stop()
        pygame.mixer.quit()
