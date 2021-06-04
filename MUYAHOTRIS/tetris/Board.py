import pygame, sys, datetime, time
from pygame.locals import *
from Piece import *
from Variable import *
from Menu import *
import time
from Level import *

pygame.init()
display = pygame.display.Info()

class Board:

    def __init__(self, screen):                                                                                         # 초기화 함수
        self.screen = screen
        self.width = Size.field_width
        self.height = Size.field_height
        self.block_size = Size.block_size
        self.init_board()
        self.generate_piece()
        self.block_x = Size.block_x
        self.block_y = Size.block_y
        self.screen_point1_x = Draw.screen_point1_x
        self.screen_point1_y = Draw.screen_point1_y
        self.screen_point2_x = Draw.screen_point2_x
        self.screen_point2_y = Draw.screen_point2_y
        self.screen_widget_x = self.screen_point1_x+(self.screen_point2_x-self.screen_point1_x)*Draw.white_text_rate    # 하얀부분 글씨

    def init_board(self):                                                                                               # 보드 초기화
        self.board = []
        self.score = Set.init_score
        self.level = Set.init_level
        self.goal = Set.init_goal
        self.skill = Set.init_skill
        for _ in range(self.height):
            self.board.append([Set.empty_board]*self.width)



    def generate_piece(self):                                                                                           # 블록 생성
        self.piece = Piece()
        self.next_piece = Piece()
        self.piece_x, self.piece_y = Set.create_location_x,Set.create_location_y

    def nextpiece(self):                                                                                                # 다음 블록 생성
        self.piece = self.next_piece
        self.next_piece = Piece()
        self.piece_x, self.piece_y = Set.create_location_x,Set.create_location_y

    def absorb_piece(self):                                                                                             # 아랫 줄에 닿았을 때 실행
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    self.board[y+self.piece_y][x+self.piece_x] = block
        block_sound = pygame.mixer.Sound(Sound.block_sound_ref)
        block_sound.play()
        self.nextpiece()
        self.score += Score.stack_score


    def block_collide_with_board(self, x, y):                                                                           # 벽과 충돌하는 판정
        if x < Set.left_wall_x:
            return Error_Type.COLLIDE_ERROR['left_wall']
        elif x >= self.width:
            return Error_Type.COLLIDE_ERROR['right_wall']
        elif y >= self.height:
            return Error_Type.COLLIDE_ERROR['bottom']
        elif self.board[y][x]:
            return Error_Type.COLLIDE_ERROR['overlap']
        return Error_Type.COLLIDE_ERROR['no_error']

    def collide_with_board(self, dx, dy):                                                                               # 블록 충돌 판정
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    collide = self.block_collide_with_board(x=x+dx, y=y+dy)
                    if collide:
                        return collide
        return Error_Type.COLLIDE_ERROR['no_error']

    def can_move_piece(self, dx, dy):                                                                                   # 블록 움직임 가능 판단
        _dx = self.piece_x + dx
        _dy = self.piece_y + dy
        if self.collide_with_board(dx = _dx, dy = _dy):
            return False
        return True

    def can_drop_piece(self):                                                                                           # 블록 낙하 가능 판단
        return self.can_move_piece(dx=Set.keep_state, dy=Set.plus_one)                                                  

    def try_rotate_piece(self, clockwise=True):                                                                         # 블록 회전할 때
        self.piece.rotate(clockwise)
        collide = self.collide_with_board(dx=self.piece_x, dy=self.piece_y)
        if not collide:
            pass
        elif collide == Error_Type.COLLIDE_ERROR['left_wall']:
            if self.can_move_piece(dx=Set.plus_one, dy=Set.keep_state):
                self.move_piece(dx=Set.plus_one, dy=Set.keep_state)
            elif self.can_move_piece(dx=Set.plus_two, dy=Set.keep_state):
                self.move_piece(dx=Set.plus_two, dy=Set.keep_state)
            else:
                self.piece.rotate(not clockwise)
        elif collide == Error_Type.COLLIDE_ERROR['right_wall']:
            if self.can_move_piece(dx=-Set.plus_one, dy=Set.keep_state):
                self.move_piece(dx=-Set.plus_one, dy=Set.keep_state)
            elif self.can_move_piece(dx=-Set.plus_two, dy=Set.keep_state):
                self.move_piece(dx=-Set.plus_two, dy=Set.keep_state)
            else:
                self.piece.rotate(not clockwise)
        else:
            self.piece.rotate(not clockwise)

    def move_piece(self, dx, dy):                                                                                       # 블록 움직일 때
        if self.can_move_piece(dx, dy):
            self.piece_x += dx
            self.piece_y += dy

    def drop_piece(self):                                                                                               # 블록 낙하할 때
        if self.can_drop_piece():
            self.move_piece(dx=Set.keep_state, dy=Set.plus_one)
        else:
            self.absorb_piece()
            self.delete_lines()

    def full_drop_piece(self):                                                                                          # 블록 한 번에 떨어질 때
        while self.can_drop_piece():
            self.drop_piece()
        self.drop_piece()

    def rotate_piece(self, clockwise=True):                                                                             # 블록 회전
        self.try_rotate_piece(clockwise)

    def pos_to_pixel(self, x, y):                                                                                       # 블록 좌표 계산
        return self.block_x*x, self.block_y*(y-Set.hidden_lines)

    def pos_to_pixel_next(self, x, y):                                                                                  # 다음 블록 좌표 계산
        return self.block_x*x*Size.next_block_ratio, self.block_y*(y-Set.hidden_lines)*Size.next_block_ratio

    def delete_line(self, y):                                                                                           # 줄 삭제시 이전줄 당겨오기
        for y in reversed(range(Set.first_line_index_y, y+Num.One)):
            self.board[y] = list(self.board[y-Num.One])

    def delete_lines(self):                                                                                             # 줄 삭제시
        remove = [y for y, row in enumerate(self.board) if all(row)]
        delete_number = len(remove)                                                                                     # 지워지는 줄 수

        for y in remove:
            line_sound = pygame.mixer.Sound("assets/sounds/MP_Mirror Shattering.mp3")
            if delete_number == Num.Two:                                                                                # 2줄 동시에 지우는 경우
                combo_image = pygame.image.load("assets/images/2x Combo.png")                                           # 2콤보시 나오는 이미지
                combo_image = pygame.transform.scale(combo_image, Image.combo_image_size)                               # 이미지 리사이징
                start_time = time.time()                                                                                # 시작 시간
                while True:
                    current_time = time.time()                                                                          # 현재 시간
                    self.screen.blit(combo_image, Image.combo_image_init)                                               # 이미지 그리기
                    pygame.display.update()                                                                             # 화면 업데이트
                    if current_time-start_time > Effect.combo_duration:                                                 # 일정 시간이 지나면 무한 반복문 탈출
                        break

            elif delete_number == Num.Three:                                                                            # 3줄 동시에 지우는 경우
                combo_image = pygame.image.load("assets/images/3x Combo.png")                                           # 3콤보시 나오는 이미지
                combo_image = pygame.transform.scale(combo_image, Image.combo_image_size)                               # 이미지 리사이징
                start_time = time.time()                                                                                # 시작 시간
                while True:
                    current_time = time.time()                                                                          # 현재 시간
                    self.screen.blit(combo_image, Image.combo_image_init)                                               # 이미지 그리기
                    pygame.display.update()                                                                             # 화면 업데이트
                    if current_time-start_time > Effect.combo_duration:                                                 # 일정 시간이 지나면 무한 반복문 탈출
                        break

            elif delete_number == Num.Four:                                                                             # 4줄 동시에 지우는 경우
                combo_image = pygame.image.load("assets/images/4x Combo.png")                                           # 4콤보시 나오는 이미지
                combo_image = pygame.transform.scale(combo_image, Image.combo_image_size)                               # 이미지 리사이징
                start_time = time.time()                                                                                # 시작 시간
                while True:
                    current_time = time.time()                                                                          # 현재 시간
                    self.screen.blit(combo_image, Image.combo_image_init)                                               # 이미지 그리기
                    pygame.display.update()                                                                             # 화면 업데이트
                    if current_time-start_time > Effect.combo_duration:                                                 # 일정 시간이 지나면 무한 반복문 탈출
                        break
            Effect.count = Effect.count + Num.One                                                                       # 한줄 지우면 카운트
            if Effect.count == len(remove):                                                                             # 지워진 줄 수 만큼 반복하면
                line_sound.play()                                                                                       # 지워지는 소리 재생
                Effect.count = Num.Zero                                                                                 # 카운트 0으로 초기화

            self.delete_line(y)                                                                                         # y번째 줄 지움
            self.score += Set.delete_score * delete_number                                                              # 스코어 합산
            self.goal -= Set.delete_goal                                                                                # goal 줄 지울때 마다 하나씩 지우기

            if self.goal == Set.success_goal:
                if self.level < Set.max_level:
                    self.level += Set.plus_level
                    self.goal = Set.init_goal * self.level
                    self.levelup()                                                                                      # 레벨업시 불러오는 함수
                    if Level_Up.level_up_mode_key:                                                                      # 레벨업 모드일 경우에만
                        if self.level < Set.max_level:                                                                  # 최대 레벨보다 아래이면
                            self.board = []                                                                             # 보드 초기화
                            for i in range(self.height):
                                self.board.append(Level.lv[self.level-Num.Two][i])                                      # 레벨 파일에 있는 방해블록 그리기
                else:
                    self.goal = '-'


    def game_over(self):                                                                                                # 게임 오버시
        return sum(self.board[Set.board_first]) > Set.empty_board or sum(self.board[Set.board_second]) > Set.empty_board

    def draw_blocks(self, array2d, color=Color.WHITE, dx=Num.Zero, dy=Num.Zero):                                        # 블록 그리기
        for y, row in enumerate(array2d):
            y += dy
            if y >= Set.board_third and y < self.height:
                for x, block in enumerate(row):
                    if block:
                        x += dx
                        x_pix, y_pix = self.pos_to_pixel(x, y)
                        pygame.draw.rect(self.screen, Piece_Shape.Block_COLOR[block - Draw.Shape_Color_Match],
                                        (x_pix, y_pix, self.block_x, self.block_y))
                        pygame.draw.rect(self.screen, Color.BLACK,
                                        (x_pix, y_pix, self.block_x, self.block_y), Draw.border_thickness)

    def draw_shadow(self, array2d, dx, dy):                                                                             # 그림자 기능 함수 추가
        for y, row in enumerate(array2d):
            y += dy
            if y >= Set.board_first and y < self.height:
                for x, block in enumerate(row):
                    x += dx
                    if block:
                        tmp = Set.plus_one
                        while self.can_move_piece(Num.Zero,tmp):
                            tmp += Set.plus_one
                        x_s, y_s = self.pos_to_pixel(x,y + tmp - Num.One)                                               # 그림자가 생기는 위치 계산

                        pygame.draw.rect(self.screen, Piece_Shape.Block_COLOR[Draw.Shadow_Color_index],
                                         (x_s, y_s, self.block_x, self.block_y))
                        pygame.draw.rect(self.screen, Color.BLACK,
                                         (x_s, y_s, self.block_x, self.block_y),Draw.border_thickness)

    def draw_next_piece(self, array2d, color=Color.WHITE):                                                              # 다음 블록 그리기
        for y, row in enumerate(array2d):
            for x, block in enumerate(row):
                if block:
                    x_pix, y_pix = self.pos_to_pixel_next(x,y)
                    pygame.draw.rect(self.screen, Piece_Shape.Block_COLOR[block - Draw.Shape_Color_Match],
                                    (x_pix+self.screen_point1_x, y_pix+(self.screen_point2_y-self.screen_point1_y)*Draw.next_block_y, self.block_x * Size.next_block_gap, self.block_y * Size.next_block_gap))# 넥스트블록
                    pygame.draw.rect(self.screen, Color.BLACK,
                                    (x_pix+self.screen_point1_x, y_pix+(self.screen_point2_y-self.screen_point1_y)*Draw.next_block_y, self.block_x * Size.next_block_gap, self.block_y * Size.next_block_gap), Draw.border_thickness)

    def draw(self,previous_time):                                                                                       # 그리기
        current_time = int(time.time())
        play_time = current_time - previous_time
        play_second = play_time % Draw.time_minute_to_second
        play_minute = int(play_time / Draw.time_minute_to_second)
        play_time = str(play_minute) + Draw.time_colon + str(play_second)

        self.screen.fill(Color.BLACK)
        for x in range(self.width):
            for y in range(self.height):
                x_pix, y_pix = self.pos_to_pixel(x, y)
                pygame.draw.rect(self.screen, Color.DARKGRAY,
                 (x_pix, y_pix, self.block_x, self.block_y))
                pygame.draw.rect(self.screen, Color.BLACK,
                 (x_pix, y_pix, self.block_x, self.block_y),Num.One)

        self.draw_shadow(self.piece, dx=self.piece_x,dy=self.piece_y)                                                   # 그림자 기능 추가
        self.draw_blocks(self.piece, dx=self.piece_x, dy=self.piece_y)
        self.draw_blocks(self.board)

        pygame.draw.rect(self.screen, Color.WHITE, Rect(self.screen_point1_x, self.screen_point1_y, self.screen_point2_x, self.screen_point2_y)) # 게임시 옆에 흰색 바탕 관련 코드
        self.draw_next_piece(self.next_piece)
        next_text = pygame.font.Font('assets/Roboto-Bold.ttf', Draw.next_text_size).render('NEXT', True, Color.BLACK)
        score_text = pygame.font.Font('assets/Roboto-Bold.ttf', Draw.score_text_size).render('SCORE', True, Color.BLACK)
        score_value = pygame.font.Font('assets/Roboto-Bold.ttf', Draw.score_value_size).render(str(self.score), True, Color.BLACK)
        level_text = pygame.font.Font('assets/Roboto-Bold.ttf', Draw.level_text_size).render('LEVEL', True, Color.BLACK)
        level_value = pygame.font.Font('assets/Roboto-Bold.ttf', Draw.level_value_size).render(str(self.level), True, Color.BLACK)
        goal_text = pygame.font.Font('assets/Roboto-Bold.ttf', Draw.goal_text_size).render('GOAL', True, Color.BLACK)
        goal_value = pygame.font.Font('assets/Roboto-Bold.ttf', Draw.goal_value_size).render(str(self.goal), True, Color.BLACK)
        play_text = pygame.font.Font('assets/Roboto-Bold.ttf', Draw.play_text_size).render('PLAY',True, Color.BLACK)
        time_text = pygame.font.Font('assets/Roboto-Bold.ttf', Draw.time_text_size).render(play_time, True, Color.BLACK)
        self.screen.blit(next_text, (self.screen_widget_x, (self.screen_point2_y-self.screen_point1_y)*Draw.next_text_dy))
        self.screen.blit(score_text, (self.screen_widget_x, (self.screen_point2_y-self.screen_point1_y)*Draw.score_text_dy))
        self.screen.blit(score_value, (self.screen_widget_x, (self.screen_point2_y-self.screen_point1_y)*Draw.score_value_dy))
        self.screen.blit(level_text, (self.screen_widget_x, (self.screen_point2_y-self.screen_point1_y)*Draw.level_text_dy))
        self.screen.blit(level_value, (self.screen_widget_x, (self.screen_point2_y-self.screen_point1_y)*Draw.level_value_dy))
        self.screen.blit(goal_text, (self.screen_widget_x, (self.screen_point2_y-self.screen_point1_y)*Draw.goal_text_dy))
        self.screen.blit(goal_value, (self.screen_widget_x, (self.screen_point2_y-self.screen_point1_y)*Draw.goal_value_dy))
        self.screen.blit(play_text, (self.screen_widget_x, (self.screen_point2_y-self.screen_point1_y)*Draw.play_text_dy))
        self.screen.blit(time_text, (self.screen_widget_x, (self.screen_point2_y-self.screen_point1_y)*Draw.time_text_dy))

    def pause(self):
        (resize.display_width,resize.display_height) = pygame.display.get_surface().get_size()
        pause_image = pygame.image.load(Image.pause_image_ref)                                                          # Pause 이미지 로드
        pause_image = pygame.transform.scale(pause_image, (resize.display_width,resize.display_height))                 # Pause 이미지 350,450 크기 변환
        self.screen.blit(pause_image,resize.init_image_point)                                                           # Pause 이미지 시작 위치 좌상단 좌표
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYUP and event.key == K_p:
                    running = False

    def GameOver(self):
        (resize.display_width, resize.display_height) = pygame.display.get_surface().get_size()
        gameover_image = pygame.image.load(Image.gameover_image_ref)                                                    # Gameover 이미지 로드
        gameover_image = pygame.transform.scale(gameover_image, (resize.display_width, resize.display_height))
        self.screen.blit(gameover_image, resize.init_image_point)                                                       # Gameover 이미지 시작 위치 좌상단 좌
        pygame.display.update()
        self.resizing()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    running = False
        Level_Up.level_up_mode_key = False
        self.HS(str(self.score))                                                                                        # GameOver 함수 호출후 그 다음화면 HIGH SCORE 화면 호출

    def newGame(self):
        (resize.display_width, resize.display_height) = pygame.display.get_surface().get_size()
        self.resizing()
        pygame.display.set_mode((resize.display_width, resize.display_height), RESIZABLE)
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                running = False

    def HS(self, txt="no"):
        self.screen.fill(Color.BLACK)                                                                                   # 뒷배경 블랙
        self.resizing()                                                                                                 # 리사이징 함수
        pygame.display.set_mode((resize.display_width, resize.display_height), RESIZABLE)
        pygame.display.update()                                                                                         # 업데이트
        if txt != "no":
            fontObj = pygame.font.Font(pygame_menu.font.FONT_MUNRO, Size.HS_font_size)
            textSurfaceObj = fontObj.render('HighScore : '+txt, True, Color.LIGHTYELLOW)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (resize.display_width/Num.Two, resize.display_height/Num.Two)                          # 점수 표시 가운데 위치
            self.screen.blit(textSurfaceObj, textRectObj)
            pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    running = False

    def resizing(self):
        infoObject = pygame.display.Info()                                                                              # 디스플레이 정보 받아오기
        self.max_height = infoObject.current_h                                                                          # 최대 높이
        pre_display_width = resize.display_width                                                                        # 이전 폭
        pre_display_height = resize.display_height                                                                      # 이전 높이
        (resize.display_width, resize.display_height) = pygame.display.get_surface().get_size()                         # 현재 창 크기 받아오기
        if resize.display_width <= resize.min_display_w:                                                                # 최소 폭보다 작을 때
            resize.display_width = resize.min_display_w
        if resize.display_height <= resize.min_display_h:                                                               # 최소 높이보다 작을 때
            resize.display_height = resize.min_display_h
        var_display_width_rate = resize.display_width / pre_display_width                                               # 변동된 폭 비율
        var_display_height_rate = resize.display_height / pre_display_height                                            # 변동된 높이 비율
        block_board_width = resize.display_width * resize.block_board_rate                                              # 전체 화면의 block_board 비율
        score_board_width = resize.display_width * resize.score_board_rate                                              # 전체 화면의 score_board 비율
        self.block_x = block_board_width * resize.text_init_rate                                                        # 블록 가로 리사이징
        self.block_y = resize.display_height * resize.one_block_height_ratio                                            # 블록 세로 리사이징
        self.block_size = Size.block_x * Size.block_y                                                                   # 블록 크기
        self.screen_point1_x = block_board_width                                                                        # 스코어 보드 시작점 x
        self.screen_point2_x = resize.display_width                                                                     # 스코어 보드 끝 점 x
        self.screen_point2_y = resize.display_height                                                                    # 스코어 보드 끝 점 y
        self.screen_widget_x = block_board_width + (score_board_width) * resize.text_init_rate
        Image.combo_image_width = int(Image.combo_image_width * var_display_width_rate)
        Image.combo_image_height = int(Image.combo_image_height * var_display_height_rate)
        Image.combo_image_size = (Image.combo_image_width,Image.combo_image_height)
        Image.combo_image_init_y = int(Image.combo_image_init_y * var_display_height_rate)
        pygame.display.update()

    def levelup(self):                                                                                                  # 레벨 업 시
        if Level_Up.level_up_mode_key:
            (resize.display_width,resize.display_height) = pygame.display.get_surface().get_size()                      # 현재 창 크기
            levelup_image = pygame.image.load(Image.levelup_image_ref)                                                  # levelup 이미지 로드
            levelup_image = pygame.transform.scale(levelup_image, (resize.display_width,resize.display_height))         # 이미지 리사이징
            levelup_sound = pygame.mixer.Sound(Sound.start_sound_ref)                                                   # 사운드 로드
            self.screen.blit(levelup_image, resize.init_image_point)                                                    # 이미지 그리기
            pygame.display.update()                                                                                     # 화면 업데이트
            levelup_sound.play()                                                                                        # 사운드 재생
            time.sleep(Num.One)
