import pygame
import os

class MusicPlayer:
    def __init__(self, music_dir):
        self.music_dir = music_dir
        self.songs = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
        self.current_index = 0
        pygame.mixer.init()

    def play(self):
        if self.songs:
            pygame.mixer.music.load(os.path.join(self.music_dir, self.songs[self.current_index]))
            pygame.mixer.music.play()

    def pause(self):
        pygame.mixer.music.pause()

    def unpause(self):
        pygame.mixer.music.unpause()

    def next_track(self):
        self.current_index = (self.current_index + 1) % len(self.songs)
        self.play()

    def prev_track(self):
        self.current_index = (self.current_index - 1) % len(self.songs)
        self.play()

    def get_current_track(self):
        return self.songs[self.current_index] if self.songs else "Ән табылмады"