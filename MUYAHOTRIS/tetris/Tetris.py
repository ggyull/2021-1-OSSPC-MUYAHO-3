import pygame, sys, time, datetime
from pygame.locals import *
from Board import *
from Variable import *
import Menu as mymenu

class Tetris:

    def __init__(self):
        self.screen = pygame.display.set_mode((resize.init_display_w,resize.init_display_h))                #리사이징 디스플레이 모드
        self.clock = pygame.time.Clock()                                                                    #
        self.board = Board(self.screen)                                                                     #보드 재생성
        self.music_on_off = True                                                                            #뮤직 on 초기값
        self.check_reset = True                                                                             #반복 key 초기값

    def handle_key(self, event_key):                                                                        #키 조작 함수
        if event_key == K_DOWN or event_key == K_s:
            self.board.drop_piece()                                                                         #블록 떨어지기
        elif event_key == K_LEFT or event_key == K_a:
            self.board.move_piece(dx=-Num.One, dy=Num.Zero)                                                 #왼쪽으로 한칸
        elif event_key == K_RIGHT or event_key == K_d:
            self.board.move_piece(dx=Num.One, dy=Num.Zero)                                                  #오른쪽으로 한칸
        elif event_key == K_UP or event_key == K_w:
            self.board.rotate_piece()                                                                       #블록 돌리기
        elif event_key == K_SPACE:
            self.board.full_drop_piece()                                                                    #블록 최대로 내리기
        elif event_key == K_m:
            self.music_on_off = not self.music_on_off                                                       #배경음악 끄기
            if self.music_on_off:
                pygame.mixer.music.play(-Num.One, Num.Zero.Num.Zero)
            else:
                pygame.mixer.music.stop()

    def run(self, mode, mode_name):                                                                         #테트리스 인게임 실행 함수
        pygame.init()
        (resize.display_width, resize.display_height) = pygame.display.get_surface().get_size()             #현재 사이즈 받아오기
        icon = pygame.image.load(Image.icon_ref)                                                            #아이콘 이미지 로딩
        pygame.display.set_icon(icon)                                                                       #아이콘 이미지 세팅
        pygame.display.set_caption('MUYAHOTRIS ' + mode_name)                                               #게임창 exe 네임
        pygame.time.set_timer(pygame.USEREVENT, mode)
        start_sound = pygame.mixer.Sound(Sound.start_sound_ref)                                             #시작 사운드
        start_sound.play()                                                                                  #사운드 시작
        bgm = pygame.mixer.music.load(Sound.bgm_ref)                                                        #bgm 사운드 로딩
        previous_time = int(time.time())                                                                    #이전 시간

        while True:
            if self.check_reset:
                self.board.newGame()                                                                        #새로운 게임 시작
                self.check_reset = False
                pygame.mixer.music.play(-Num.One, Num.Zero)                                                 #음악 시작
            if self.board.game_over():                                                                      #게임 오버 시
                self.screen.fill(Color.BLACK)
                pygame.mixer.music.stop()                                                                   #음악 중지
                self.board.GameOver()                                                                       #게임 오버 함수 호출
                self.Score = self.board.score                                                               #점수 데이터 받아오기
                self.Level = self.board.level                                                               #레벨 데이터 받아오기
                self.check_reset = True
                self.board.init_board()                                                                     #보드 초기화
                break                                                                                       #break
            for event in pygame.event.get():
                if event.type == QUIT:                                                                      #끝날 시
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYUP and event.key == K_p:                                              #일시정지 시
                    self.screen.fill(Color.BLACK)
                    pygame.mixer.music.pause()
                    self.board.pause()
                    pygame.mixer.music.unpause()
                elif event.type == KEYDOWN:
                    self.handle_key(event.key)
                elif event.type == pygame.USEREVENT:
                    self.board.drop_piece()                                                                 #피스를 드랍 하기
                elif event.type == VIDEORESIZE:                                                             #게임 중 리사이징
                    if event.h != resize.display_height or event.w != resize.display_width:
                        self.board.resizing()                                                               #리사이징
                        (MN.menu_display_w, MN.menu_display_h) = pygame.display.get_surface().get_size()    #현재 사이즈 받아오기
                        pygame.display.set_mode((resize.display_width, resize.display_height), RESIZABLE)   #리사징한 것으로 변경

            self.board.draw(previous_time)                                                                  #draw()함수 호출
            pygame.display.update()                                                                         #업데이트
            self.clock.tick(Set.framerate)                                                                  #프레임 수
