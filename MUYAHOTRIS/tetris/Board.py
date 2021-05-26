import pygame, sys, datetime, time
from pygame.locals import *
from Piece import *
from Variable import *


class Board:

    def __init__(self, screen):
        self.screen = screen
        self.width = Size.field_width
        self.height = Size.field_height
        self.block_size = Size.block_size
        self.init_board()
        self.generate_piece()

    def init_board(self):
        self.board = []
        self.score = Set.init_score
        self.level = Set.init_level
        self.goal = Set.init_goal
        self.skill = Set.init_skill
        for _ in range(self.height):
            self.board.append([Set.empty_board]*self.width)

    def generate_piece(self):
        self.piece = Piece()
        self.next_piece = Piece()
        self.piece_x, self.piece_y = Set.create_location_x,Set.create_location_y

    def nextpiece(self):
        self.piece = self.next_piece
        self.next_piece = Piece()
        self.piece_x, self.piece_y = Set.create_location_x,Set.create_location_y

    def absorb_piece(self):
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    self.board[y+self.piece_y][x+self.piece_x] = block
        block_sound = pygame.mixer.Sound(Sound.block_sound_ref)
        block_sound.play()
        self.nextpiece()
        self.score += Score.stack_score

        #if self.level < Set.max_level:
        #    pygame.time.set_timer(pygame.USEREVENT, (500 - 50 * (self.level-1)))
        #else:
        #    pygame.time.set_time(pygame.USEREVENT, 100)

    def block_collide_with_board(self, x, y):
        if x < Set.left_wall_x:
            return Error_Type.COLLIDE_ERROR['left_wall']
        elif x >= self.width:
            return Error_Type.COLLIDE_ERROR['right_wall']
        elif y >= self.height:
            return Error_Type.COLLIDE_ERROR['bottom']
        elif self.board[y][x]:
            return Error_Type.COLLIDE_ERROR['overlap']
        return Error_Type.COLLIDE_ERROR['no_error']

    def collide_with_board(self, dx, dy):
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    collide = self.block_collide_with_board(x=x+dx, y=y+dy)
                    if collide:
                        return collide
        return Error_Type.COLLIDE_ERROR['no_error']

    def can_move_piece(self, dx, dy):
        _dx = self.piece_x + dx
        _dy = self.piece_y + dy
        if self.collide_with_board(dx = _dx, dy = _dy):
            return False
        return True

    def can_drop_piece(self):
        return self.can_move_piece(dx=Set.keep_state, dy=Set.plus_one)

    def try_rotate_piece(self, clockwise=True):
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

    def move_piece(self, dx, dy):
        if self.can_move_piece(dx, dy):
            self.piece_x += dx
            self.piece_y += dy

    def drop_piece(self):
        if self.can_drop_piece():
            self.move_piece(dx=Set.keep_state, dy=Set.plus_one)
        else:
            self.absorb_piece()
            self.delete_lines()

    def full_drop_piece(self):
        while self.can_drop_piece():
            self.drop_piece()
        self.drop_piece()

    def rotate_piece(self, clockwise=True):
        self.try_rotate_piece(clockwise)

    def pos_to_pixel(self, x, y):
        return self.block_size*x, self.block_size*(y-Set.hidden_lines)

    def pos_to_pixel_next(self, x, y):
        return self.block_size*x*Size.next_block_ratio, self.block_size*(y-Set.hidden_lines)*Size.next_block_ratio

    def delete_line(self, y):
        for y in reversed(range(Set.first_line_index_y, y+Set.dummy_one)):
            self.board[y] = list(self.board[y-1])

    def delete_lines(self):
        remove = [y for y, row in enumerate(self.board) if all(row)]
        delete_number = len(remove)
        for y in remove:
            line_sound = pygame.mixer.Sound(Sound.deleteline_sound_ref)
            line_sound.play()
            self.delete_line(y)
            self.score += Set.delete_score * delete_number
            self.goal -= Set.delete_goal
            if self.goal == Set.success_goal:
                if self.level < Set.max_level:
                    self.level += Set.plus_level
                    self.goal = Set.init_goal * self.level
                else:
                    self.goal = '-'

    def game_over(self):
        return sum(self.board[Set.board_first]) > Set.empty_board or sum(self.board[Set.board_second]) > Set.empty_board
    
    def draw_blocks(self, array2d, color=Color.WHITE, dx=0, dy=0):
        for y, row in enumerate(array2d):
            y += dy
            if y >= Set.board_third and y < self.height:
                for x, block in enumerate(row):
                    if block:
                        x += dx
                        x_pix, y_pix = self.pos_to_pixel(x, y)

                        pygame.draw.rect(self.screen, self.piece.Block_COLOR[block - Draw.Shape_Color_Match],
                                        (x_pix, y_pix, self.block_size, self.block_size))
                        pygame.draw.rect(self.screen, Color.BLACK,
                                        (x_pix, y_pix, self.block_size, self.block_size), Set.block_border_thickness)

    def draw_shadow(self, array2d, dx, dy): #그림자 기능 함수 추가
        for y, row in enumerate(array2d):
            y += dy
            if y >= Set.board_first and y < self.height:
                for x, block in enumerate(row):
                    x += dx
                    if block:
                        tmp = Set.plus_one
                        while self.can_move_piece(0,tmp):
                            tmp += Set.plus_one
                        x_s, y_s = self.pos_to_pixel(x,y + tmp - 1)

                        pygame.draw.rect(self.screen, self.piece.Block_COLOR[Draw.Shadow_Color_index],
                                         (x_s, y_s, self.block_size, self.block_size))
                        pygame.draw.rect(self.screen, Color.BLACK,
                                         (x_s, y_s, self.block_size, self.block_size),Set.block_border_thickness)

    def draw_next_piece(self, array2d, color=Color.WHITE):
        for y, row in enumerate(array2d):
            for x, block in enumerate(row):
                if block:
                    x_pix, y_pix = self.pos_to_pixel_next(x,y)
                    pygame.draw.rect(self.screen, self.piece.Block_COLOR[block - Draw.Shape_Color_Match],
                                    (x_pix+240, y_pix+65, self.block_size * 0.5, self.block_size * 0.5))
                    pygame.draw.rect(self.screen, Color.BLACK,
                                    (x_pix+240, y_pix+65, self.block_size * 0.5, self.block_size * 0.5),1)

    def draw(self,previous_time):
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
                 (x_pix, y_pix, self.block_size, self.block_size))
                pygame.draw.rect(self.screen, Color.BLACK,
                 (x_pix, y_pix, self.block_size, self.block_size),1)

        self.draw_shadow(self.piece, dx=self.piece_x,dy=self.piece_y) #그림자 기능 추가
        self.draw_blocks(self.piece, dx=self.piece_x, dy=self.piece_y)
        self.draw_blocks(self.board)

        pygame.draw.rect(self.screen, Color.WHITE, Rect(Draw.screen_point1_x, Draw.screen_point1_y, Draw.screen_point2_x, Draw.screen_point2_y)) # 게임시 옆에 흰색 바탕 관련 코드
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
        self.screen.blit(next_text, (Draw.next_text_dx, Draw.next_text_dy))
        self.screen.blit(score_text, (Draw.score_text_dx, Draw.score_text_dy))
        self.screen.blit(score_value, (Draw.score_value_dx, Draw.score_value_dy))
        self.screen.blit(level_text, (Draw.level_text_dx, Draw.level_text_dy))
        self.screen.blit(level_value, (Draw.level_value_dx, Draw.level_value_dy))
        self.screen.blit(goal_text, (Draw.goal_text_dx, Draw.goal_text_dy))
        self.screen.blit(goal_value, (Draw.goal_value_dx, Draw.goal_value_dy))
        self.screen.blit(play_text, (Draw.play_text_dx, Draw.play_text_dy))
        self.screen.blit(time_text, (Draw.time_text_dx, Draw.time_text_dy))

    def pause(self):
        pause_image = pygame.image.load(Image.pause_image_ref)              # Pause 이미지 로드
        pause_image = pygame.transform.scale(pause_image, (350, 450))       # Pause 이미지 350,450 크기 변환
        self.screen.blit(pause_image,(0,0))                                 # Pause 이미지 시작 위치 좌상단 좌표
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
        gameover_image = pygame.image.load(Image.gameover_image_ref)  # Gameover 이미지 로드
        gameover_image = pygame.transform.scale(gameover_image, (350, 450))  # Gameover 이미지 350,450 크기 변환
        self.screen.blit(gameover_image, (0, 0))  # Gameover 이미지 시작 위치 좌상단 좌
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    running = False
        self.HS(str(self.score))    #GameOver 함수 호출후 그 다음화면 HIGH SCORE 화면 호출

    def newGame(self):
        pygame.display.update()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                running = False

    def HS(self, txt="no"):
        self.screen.fill(Color.BLACK) # 뒷배경 블랙
        pygame.display.update() #업데이트
        if txt != "no":
            fontObj = pygame.font.Font(pygame_menu.font.FONT_MUNRO, 36)
            textSurfaceObj = fontObj.render('HighScore : '+txt, True, Color.LIGHTYELLOW)
            textRectObj = textSurfaceObj.get_rect()
            textRectObj.center = (175, 220)
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

    # 기존 q 스킬함수 -> 후에 레벨별 블록 생성시 참고하기 위해 삭제하지 않고 주석처리
    # def ultimate(self):
    #     if self.skill == 100:
    #         bomb = pygame.image.load("assets/images/bomb.jpg")
    #         bomb = pygame.transform.scale(bomb, (350, 450))
    #         bomb_sound = pygame.mixer.Sound('assets/sounds/bomb.wav')
    #         self.screen.blit(bomb, (0, 0))
    #         pygame.display.update()
    #         bomb_sound.play()
    #         time.sleep(1)
    #         self.board = []
    #         self.skill = 0
    #         for _ in range(self.height):
    #             self.board.append([0]*self.width)
