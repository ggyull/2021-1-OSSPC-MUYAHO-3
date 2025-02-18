import pygame
import pygame_menu
import random
import os
from pygame.locals import *
class Piece_Shape:

    O = (((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 1, 1, 0), (0, 0, 1, 1, 0), (0, 0, 0, 0, 0)),) * 4

    I = (((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 2, 2, 2, 2), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 2, 0, 0), (0, 0, 2, 0, 0), (0, 0, 2, 0, 0), (0, 0, 2, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (2, 2, 2, 2, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 2, 0, 0), (0, 0, 2, 0, 0), (0, 0, 2, 0, 0), (0, 0, 2, 0, 0), (0, 0, 0, 0, 0)))

    L = (((0, 0, 0, 0, 0), (0, 0, 3, 0, 0), (0, 0, 3, 0, 0), (0, 0, 3, 3, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 3, 3, 3, 0), (0, 3, 0, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 3, 3, 0, 0), (0, 0, 3, 0, 0), (0, 0, 3, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 0, 3, 0), (0, 3, 3, 3, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0)))

    J = (((0, 0, 0, 0, 0), (0, 0, 4, 0, 0), (0, 0, 4, 0, 0), (0, 4, 4, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 4, 0, 0, 0), (0, 4, 4, 4, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 4, 4, 0), (0, 0, 4, 0, 0), (0, 0, 4, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 4, 4, 4, 0), (0, 0, 0, 4, 0), (0, 0, 0, 0, 0)))

    Z = (((0, 0, 0, 0, 0), (0, 0, 0, 5, 0), (0, 0, 5, 5, 0), (0, 0, 5, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 5, 5, 0, 0), (0, 0, 5, 5, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 5, 0, 0), (0, 5, 5, 0, 0), (0, 5, 0, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 5, 5, 0, 0), (0, 0, 5, 5, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0)))

    S = (((0, 0, 0, 0, 0), (0, 0, 6, 0, 0), (0, 0, 6, 6, 0), (0, 0, 0, 6, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 6, 6, 0), (0, 6, 6, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 6, 0, 0, 0), (0, 6, 6, 0, 0), (0, 0, 6, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 6, 6, 0), (0, 6, 6, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0)))

    T = (((0, 0, 0, 0, 0), (0, 0, 7, 0, 0), (0, 0, 7, 7, 0), (0, 0, 7, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 0, 0, 0), (0, 7, 7, 7, 0), (0, 0, 7, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 7, 0, 0), (0, 7, 7, 0, 0), (0, 0, 7, 0, 0), (0, 0, 0, 0, 0)),
         ((0, 0, 0, 0, 0), (0, 0, 7, 0, 0), (0, 7, 7, 7, 0), (0, 0, 0, 0, 0), (0, 0, 0, 0, 0)))

    PIECES = {'O': O, 'I': I, 'L': L, 'J': J, 'Z': Z, 'S': S, 'T': T}

    # Tetrimino colors
    cyan = (69, 206, 204)  # rgb(69, 206, 204) # I
    blue = (64, 111, 249)  # rgb(64, 111, 249) # J
    orange = (253, 189, 53)  # rgb(253, 189, 53) # L
    yellow = (246, 227, 90)  # rgb(246, 227, 90) # O
    green = (98, 190, 68)  # rgb(98, 190, 68) # S
    pink = (242, 64, 235)  # rgb(242, 64, 235) # T
    red = (225, 13, 27)  # rgb(225, 13, 27) # Z
    black = (55, 55, 55)  # rgb(55, 55, 55) # background
    lightyellow = (251, 255, 213) # rgb(1, 255, 255) #level block
    Block_COLOR = [yellow, cyan, orange, blue, red, green, pink, black, lightyellow]

class Num:

    Zero = 0 # 0
    One = 1 # 1
    Two = 2 # 2
    Three = 3 # 3
    Four = 4 # 4

class Error_Type:

    COLLIDE_ERROR = {'no_error': 0, 'right_wall': 1, 'left_wall': 2, 'bottom': 3, 'overlap': 4}

class Color:

    #         R    G    B
    WHITE = (255, 255, 255)
    GRAY = (185, 185, 185)
    BLACK = (0, 0, 0)
    RED = (155, 0, 0)
    LIGHTRED = (175, 20, 20)
    GREEN = (0, 155, 0)
    LIGHTGREEN = (20, 175, 20)
    BLUE = (0, 0, 155)
    LIGHTBLUE = (20, 20, 175)
    YELLOW = (155, 155, 0)
    LIGHTYELLOW = (175, 175, 20)
    DARKGRAY = (26, 26, 26)
    MORELIGHTYELLOW = (255,247,22)


class Size:

    field_width = 10  # 맵의 좌에서 우로 사이즈
    field_height = 20  # 맵 위에서 아래로 사이즈
    block_x = 25 # 블록 가로(픽셀)
    block_y = 25 # 블록 세로(픽셀)
    block_size = block_x * block_y # 블록 사이즈(픽셀)
    next_block_ratio = 0.6 # 다음블록 사이즈(픽셀) 비율
    HS_font_size = 36 # 게임 오버시 최종 점수 폰트 크기
    HS_center_x = 175 # 스코어 표시 center x 위치
    HS_center_y = 220 # 스코어 표시 center y 위치
    next_block_gap = 0.55 # 다음블록 픽셀 사이 간격

class Set:

    framerate = 30 # 프레임 설정
    init_score = 0 # 초기 점수 세팅
    init_level = 1 # 초기 레벨
    init_goal = 6 # 레벨업을 하기 위한 조건
    plus_goal = 1 # 레벨 업 시 추가되는 목표
    empty_board = 0 # 블록이 없는 빈 상태
    create_location_x = 3 # 블록 생성 초기 x위치
    create_location_y = 0 # 블록 생성 초기 y위치
    left_wall_x = 0 # 왼쪽 벽 좌표
    keep_state = 0 # 블록 상태유지 상수
    plus_one = 1 # 블록 한칸 이동 상수
    plus_two = 2 # 블록 두칸 이동 상수
    hidden_lines = 2 # 맨위의 숨겨진 줄수
    first_line_index_y = 2 # 맨 윗줄 y 인덱스
    delete_score = 9 # 줄 삭제시 얻는 점수
    delete_goal = 1 # 줄 삭제시 지워지는 목표
    success_goal = 0 # 목표 달성 상수
    max_level = 10 # 최대 레벨
    plus_level = 1 # 레벨 1업
    board_first = 0 # 보드의 첫번째 줄(안보이는 줄, 블록 위치는 여기서부터)
    board_second = 1 # 보드의 두번째 줄(안보이는 줄)
    board_third = 2 # 보드의 세번째 줄(블록이 보이는 첫번째 줄)
    show_rank_five = 5 # DB 점수 상위 5개
    init_complete = False #10레벨 목표goal 도달여부 확인

class Draw:

    Shape_Color_Match = 1 # 블록을 채우는 상수와 Block_COLOR의 인덱스를 맞춰주기 위한 1(Board에서 빼줌)
    Shadow_Color_index = 7 # 그림자 색의 인덱스 (55, 55, 55)
    screen_point1_x = 250 # 흰색 스크린 시작점 x 위치
    screen_point1_y = 0  # 흰색 스크린 시작점 y 위치
    screen_point2_x = 350  # 흰색 스크린 종료점 x 위치
    screen_point2_y = 450  # 흰색 스크린 종료점 y 위치
    white_text_rate = 0.1
    next_block_y = 65/450
    next_text_size = 18  # Next 글씨 크기
    next_text_dx = 255 # Next 글씨 x위치
    next_text_dy = 20/450  # Next 글씨 y위치
    score_text_size = 18  # score 글씨 크기
    score_text_dx = 255 # score 글씨 x 위치
    score_text_dy = 120/450  # score 글씨 y 위치
    score_value_size = 16  # score 값 크기
    score_value_dx = 255 # score 값 x 위치
    score_value_dy = 145/450  # score 값 y 위치
    level_text_size = 18  # level 글씨 크기
    level_text_dx = 255 # level 글씨 x 위치
    level_text_dy = 200/450  # level 글씨 y 위치
    level_value_size = 16  # level 값 크기
    level_value_dx = 255 # level 값 x 위치
    level_value_dy = 225/450  # level 값 y 위치
    goal_text_size = 18  # goal 글씨 크기
    goal_text_dx = 255  # goal 글씨 x 위치
    goal_text_dy = 275/450  # goal 글씨 y 위치
    goal_value_size = 16  # goal 값 크기
    goal_value_dx = 255  # goal 값 x 위치
    goal_value_dy = 300/450  # goal 값 y 위치
    play_text_size = 18 # PLAY 글씨 크기
    play_text_dx = 255 # PLAY 텍스트 값 x 위치
    play_text_dy = 400/450 # PLAY 텍스트 값 y 위치
    time_text_size = 16  # time 글씨 크기
    time_text_dx = 255 # time 글씨 x 위치
    time_text_dy = 430/450  # time 글씨 y 위치
    time_minute_to_second = 60 #time 1분 60초 변환
    time_zero = 0 #time 0 초기값
    time_plus = 1 #time 1 증가량
    time_colon = ' : ' #time 콜론 ex) 11 : 21
    border_thickness = 1 # 블록 경계 두께


class resize:

    init_display_w = 357 # 시작 디스플레이 가로
    init_display_h = 450 # 시작 디스플레이 세로
    init_image_point = (0,0) # 초기 이미지 시작점
    (display_width, display_height) = (357,450) # 게임 창 크기
    block_board_rate = 0.7 # 보드판이 차지하는 width 비율
    score_board_rate = 0.3 # 스코어보드가 차지하는 width 비율
    text_init_rate = 0.1 # 스코어보드에서 글씨가 시작되는 곳의 비율
    one_block_height_ratio = 1/18 # 한 블록 세로가 전체에서 차지하는 비율
    min_display_w = 357 # 최소 디스플레이 가로
    min_display_h = 450 # 최소 디스플레이 세로

class Image:

    icon_ref = 'assets/images/icon.png' # 테트리스 exe 아이콘
    pause_image_ref = 'assets/images/pause_image.png' # pause 이미지 주소
    gameover_image_ref = 'assets/images/gameover_image.png' # gameover 이미지 주소
    levelup_image_ref = 'assets/images/muyaho1.jpg' #levelup 이미지 주가
    GameComplete_image_ref = 'assets/images/clear_image.png'
    main_image = pygame_menu.baseimage.BaseImage(
        image_path='assets/images/main_image.png',
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
    help_image = pygame_menu.baseimage.BaseImage(
        image_path='assets/images/help_image.png',
        drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL)
    combo_image_width = 250         #콤보 이미지 초기 폭
    combo_image_height = 50         #콤보 이미지 초기 높이
    combo_image_size = (250,50)     #콤보 이미지 초기 사이즈

    combo_image_init_x = 0          #콤보 이미지 초기 x 출력 위치
    combo_image_init_y = 50         #콤보 이미지 초기 y 출력 위치
    combo_image_init = (0,50)       #콤보 이미지 초기 출력 위치

class MN:
    infoObject = () #디스플레이 사이즈 받기
    menu_display_w = 357
    menu_display_h = 450
    initial_mode = 0
    initial_id = 0 # 초기 ID 값
    surface = (0,0) # 초기 surface


    #메뉴 기본 테마 만들기

    mytheme=pygame_menu.themes.THEME_ORANGE.copy()                  # 메뉴 기본 테마 설정
    mytheme.widget_font_color= Color.MORELIGHTYELLOW                # 메뉴 위젯 폰트 컬러
    mytheme.background_color = Image.main_image                           # 메뉴 배경 설정
    #mytheme.widget_background_color = widget_image                 # 메뉴 위젯 배경 설정
    mytheme.title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE  # 메뉴 타이틀 바 모양 설정
    mytheme.widget_alignment=pygame_menu.locals.ALIGN_CENTER        # 메뉴 가운데 정렬 설정
    mytheme.widget_font =pygame_menu.font.FONT_MUNRO                # 메뉴 폰트 설정
    mytheme.widget_margin=(0,40)

    #HELP 메뉴 만들기
    mytheme_help = pygame_menu.themes.THEME_ORANGE.copy()  # 메뉴 기본 테마 설정
    mytheme_help.widget_font = pygame_menu.font.FONT_MUNRO
    mytheme_help.background_color = Image.help_image  # 메뉴 배경 설정
    mytheme_help.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE  # 메뉴 타이틀 바 모양 설정



    rank_id_max=3           # 랭크 ID 최대 이름 수
    rank_max=5              # 랭크 보여주는 창 최대 갯수 -1
    min_display_w =357      # 메뉴 최소 사이즈 가로
    min_display_h =450      # 메뉴 최소 사이즈 세로
    widget_center = 0
    sleep_time = 0.3
    initial_page = 'page0'  # 메뉴 시작 페이지

    # 리사이징 시 변하는 비율 화면과 비례하는 비율
    font_rate_main = 15         # 메인 폰트 리사이징 비율
    font_rate_sub = 20          # 서브 폰트들 리사이징 비율
    widget_rate_main = 30       # 메인 화면 리젯들 사이 간격 비율
    widget_rate_showpage = 30   # showpage 위젯 간격 비율
    widget_rate_rank = 60       # rank페이지 위젯 간격 비율
    rate_main=6                 # 메인 위젯 시작 하는 위치 비율
    rate_show=40                # show 위젯 시작 하는 위치 비율
    rate_rank=30                # rank 위젝 시작 위치 비율
    rate_help=1.25              # help 창 위젯 시작 위치 비율



    help_h=756
    help_w=756
    help_screen=(756,756)


    #폰트 사이즈
    font_main = int((menu_display_h) / font_rate_main)   # 메뉴 기본 폰트 사이즈
    font_sub = int((menu_display_h) / font_rate_sub)     # 메뉴 서브 폰트 사이즈

    # 위젯 사이 간격
    widget_margin_main = (0,int((menu_display_h)/widget_rate_main))         #  메인 화면
    widget_margin_showpage=(0,int((menu_display_h)/widget_rate_showpage))   #게임 선택 랭킹 선택
    widget_margin_rank=(0,int((menu_display_h)/widget_rate_rank))           # 랭크 보기 화면

    #마진 시작 가로 세로  좌표
    margin_main = int((menu_display_h)/rate_main)   # 메인 화면
    margin_show = int((menu_display_h)/rate_show)   #SHOW 화면
    margin_rank =int((menu_display_h)/rate_rank)    #RANK 화
    margin_help=280    #HELP 화면

    #게임 모드 선택 시 속도
    start_easy = 500
    start_hard = 200

class Score:
    stack_score = 1 # 블록 쌓을 때 쌓이는 점수


class Sound:
    start_sound_ref = 'assets/sounds/Start.wav' # 스타트 사운드 주소
    block_sound_ref = 'assets/sounds/MP_Jab.wav' # 블록 쌓을 때 사운드 주소
    deleteline_sound_ref = 'assets/sounds/MP_MirrorShattering.wav' # 블록 지울 때 사운드 주소
    bgm_ref = 'assets/sounds/new_bgm.wav' # 배경음악 주소
    levelup_sound_ref = 'assets/sounds/levelup_sd.wav' #레벨업 사운드 주소

class Effect:
    combo_duration = 0.1 # 콤보 이미지 노출 시간
    count = 0            # 누가 소리를 한 번만 내었느냐 말이야(마지막 지우는 줄 세기 위함)

class Level_Up:
    level_up_mode_key = False
