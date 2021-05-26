import pygame, sys, time, datetime
from pygame.locals import *
from Board import *
from Variable import *

class Tetris:

    def __init__(self):
        self.screen = pygame.display.set_mode((350,450))
        self.clock = pygame.time.Clock()
        self.board = Board(self.screen)
        self.music_on_off = True
        self.check_reset = True

    def handle_key(self, event_key):
        if event_key == K_DOWN or event_key == K_s:
            self.board.drop_piece()
        elif event_key == K_LEFT or event_key == K_a:
            self.board.move_piece(dx=-1, dy=0)
        elif event_key == K_RIGHT or event_key == K_d:
            self.board.move_piece(dx=1, dy=0)
        elif event_key == K_UP or event_key == K_w:
            self.board.rotate_piece()
        elif event_key == K_SPACE:
            self.board.full_drop_piece()
        elif event_key == K_q:
            self.board.ultimate()
        elif event_key == K_m:
            self.music_on_off = not self.music_on_off
            if self.music_on_off:
                pygame.mixer.music.play(-1, 0.0)
            else:
                pygame.mixer.music.stop()

    def run(self, timer):
        pygame.init()
        icon = pygame.image.load(Image.icon_ref)
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Tetris')
        pygame.time.set_timer(pygame.USEREVENT, timer)
        start_sound = pygame.mixer.Sound(Sound.start_sound_ref)
        start_sound.play()
        bgm = pygame.mixer.music.load(Sound.bgm_ref)
        previous_time = int(time.time())

        while True:
            if self.check_reset:
                self.board.newGame()
                self.check_reset = False
                pygame.mixer.music.play(-1, 0.0)
            if self.board.game_over():
                self.screen.fill(Color.BLACK)
                pygame.mixer.music.stop()
                self.board.GameOver()
                self.Score = self.board.score
                self.check_reset = True
                self.board.init_board()
                break
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYUP and event.key == K_p:
                    self.screen.fill(Color.BLACK)
                    pygame.mixer.music.stop()
                    self.board.pause()
                    pygame.mixer.music.play(-1, 0.0)
                elif event.type == KEYDOWN:
                    self.handle_key(event.key)
                elif event.type == pygame.USEREVENT:
                    self.board.drop_piece()
            self.board.draw(previous_time)
            pygame.display.update()
            self.clock.tick(30)
