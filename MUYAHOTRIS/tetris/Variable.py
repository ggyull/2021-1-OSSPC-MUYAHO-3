import pygame
import pygame_menu
import random
import os

class Error_Type:
    COLLIDE_ERROR = {'no_error': 0, 'right_wall': 1, 'left_wall': 2, 'bottom': 3, 'overlap': 4}

class Color:
    #               R    G    B
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

class Size:
    field_width = 10  # 맵의 좌에서 우로 사이즈
    field_height = 20  # 맵 위에서 아래로 사이즈
    block_size = 25

class Set:
    init_score = 0 # 초기 점수 세팅
    init_level = 1 # 초기 레벨
    init_goal = 5 # 레벨업을 하기 위한 조건
    init_skill = 0 # q스킬 게이지
    empty_board = 0 # 블록이 없는 빈 상태
    create_location_x = 3 # 블록 생성 초기 x위치
    create_location_y = 0 # 블록 생성 초기 y위치