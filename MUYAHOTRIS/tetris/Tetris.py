import pygame, sys, time, datetime
from pygame.locals import *
from Board import *
from Variable import *

class Tetris:

    def __init__(self):
        self.screen = pygame.display.set_mode((resize.init_display_w,resize.init_display_h))
        self.clock = pygame.time.Clock()
        self.board = Board(self.screen)
        self.music_on_off = True
        self.check_reset = True

    def handle_key(self, event_key):
        if event_key == K_DOWN or event_key == K_s:
            self.board.drop_piece()
        elif event_key == K_LEFT or event_key == K_a:
            self.board.move_piece(dx=-Num.One, dy=Num.Zero)
        elif event_key == K_RIGHT or event_key == K_d:
            self.board.move_piece(dx=Num.One, dy=Num.Zero)
        elif event_key == K_UP or event_key == K_w:
            self.board.rotate_piece()
        elif event_key == K_SPACE:
            self.board.full_drop_piece()
        elif event_key == K_q:
            self.board.ultimate()
        elif event_key == K_m:
            self.music_on_off = not self.music_on_off
            if self.music_on_off:
                pygame.mixer.music.play(-Num.One, Num.Zero.Num.Zero)
            else:
                pygame.mixer.music.stop()

    def run(self, mode, mode_name):
        pygame.init()
        (resize.display_width, resize.display_height) = pygame.display.get_surface().get_size()
        icon = pygame.image.load(Image.icon_ref)
        pygame.display.set_icon(icon)
        pygame.display.set_caption('MUYAHOTRIS ' + mode_name)
        pygame.time.set_timer(pygame.USEREVENT, mode)
        start_sound = pygame.mixer.Sound(Sound.start_sound_ref)
        start_sound.play()
        bgm = pygame.mixer.music.load(Sound.bgm_ref)
        previous_time = int(time.time())

        while True:
            if self.check_reset:
                self.board.newGame()
                self.check_reset = False
                pygame.mixer.music.play(-Num.One, Num.Zero)
            if self.board.game_over():
                self.screen.fill(Color.BLACK)
                pygame.mixer.music.stop()
                self.board.GameOver()
                self.check_reset = True
                self.board.init_board()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYUP and event.key == K_p:
                    self.screen.fill(Color.BLACK)
                    pygame.mixer.music.stop()
                    self.board.pause()
                    pygame.mixer.music.play(-Num.One, Num.Zero)
                elif event.type == KEYDOWN:
                    self.handle_key(event.key)
                elif event.type == pygame.USEREVENT:
                    self.board.drop_piece()
                # 게임 중 리사이징
                elif event.type == VIDEORESIZE:
                    if event.h != resize.display_height or event.w != resize.display_width:
                        self.board.resizing()
                        pygame.display.set_mode((resize.display_width, resize.display_height), RESIZABLE)

            self.board.draw(previous_time)
            pygame.display.update()
            self.clock.tick(Set.framerate)
