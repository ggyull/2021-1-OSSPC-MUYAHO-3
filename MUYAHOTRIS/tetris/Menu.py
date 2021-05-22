# -*- coding: utf-8 -*-
#https://pygame-menu.readthedocs.io/en/latest/_source/add_widgets.html
#https://github.com/ppizarror/pygame-menu
# 참고해서 메뉴 만들어 봅시다!

import pygame
import pygame_menu
from Tetris import *
import time
from Variable import MN

class Menu:

    def __init__(self):
        pygame.init()
        MN.infoObject = pygame.display.Info()
        self.tetris=Tetris()
        #self.database = Database()
        (MN.menu_display_w, MN.menu_display_h) = pygame.display.get_surface().get_size()
        self.w = MN.menu_display_w
        self.h = MN.menu_display_h
        self.Mode = MN.initial_mode
        #self.id=Var.initial_id
        #self.score=Var.initial_score
        self.page=MN.initial_page
        self.surface=pygame.display.set_mode((self.w,self.h),RESIZABLE)
        self.mytheme=MN.mytheme
        self.mytheme2=MN.mytheme_help
        self.menu = pygame_menu.Menu(self.h,self.w, '', theme=self.mytheme)
        self.font_main=MN.font_main   # 메인 폰트 사이즈
        self.font_sub=MN.font_sub     # 서브 폰트 사이즈
        self.widget_margin_main=MN.widget_margin_main         #메인 위젯 사이 간격
        self.widget_margin_showpage=MN.widget_margin_showpage #show 페이지 위젯 사이 간격
        self.widget_margin_rank=MN.widget_margin_rank         #rank 페이지 위젯 사이 간격
        self.margin_main=MN.margin_main                       #메인 페이지 x,y 위젯 시작 위치
        self.margin_show=MN.margin_show                       #show 페이지 x,y 위젯 시작 위치
        self.margin_help=MN.margin_help                       #help 페이지 back 위치
        self.margin_rank=MN.margin_rank                       #rank 페이지 x,y 위젯 시작 위치

    def run(self):   # 실행하는 함수
        self.page=MN.initial_page   #시작하면 기본 모드로 모드가 설정
        self.menu.clear()
        self.mytheme.widget_margin=self.widget_margin_main
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_button('   Single Mode   ', self.show_game,font_size=self.font_main)
        self.menu.add_button('    VS Mode    ', self.vs_mode,font_size=self.font_main)
        self.menu.add_button('  Ranking  ', self.show_rank,font_size=self.font_main)
        self.menu.add_button('  Help  ', self.help, font_size=self.font_main)
        self.menu.add_button('        Exit         ', pygame_menu.events.EXIT,font_size=self.font_main)

    def reset(self):  ## 뒤로 갈때 보여줄 목록들
        self.surface = pygame.display.set_mode((self.w, self.h), RESIZABLE)
        self.menu = pygame_menu.Menu(self.h, self.w, '', theme=self.mytheme)
        self.mytheme.widget_margin=self.widget_margin_main
        #Menu.click.play()
        self.page=MN.initial_page
        self.menu.clear()
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_button('   Single Mode   ', self.show_game,font_size=self.font_main)
        self.menu.add_button('    VS Mode    ', self.vs_mode,font_size=self.font_main)
        self.menu.add_button('  Ranking  ', self.show_rank,font_size=self.font_main)
        self.menu.add_button('  Help  ', self.help, font_size=self.font_main)
        self.menu.add_button('        Exit         ', pygame_menu.events.EXIT,font_size=self.font_main)

    def help(self): # help 페이
        self.page='page7'
        self.surface = pygame.display.set_mode(MN.help_screen)
        self.menu = pygame_menu.Menu(MN.help_h, MN.help_w, '', theme=self.mytheme2)
        self.menu.add_vertical_margin(self.margin_help)
        self.menu.add_button(' back ', self.reset,font_size=self.font_sub)

    def show_game(self):

        self.page = 'page1'

        #Menu.click.play()
        self.menu.clear()
        self.mytheme.widget_margin=self.widget_margin_showpage
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_label("   __Start game__   ", selectable=False, font_size=self.font_main)
        self.menu.add_vertical_margin(self.margin_show)
        self.menu.add_button('     Easy mode     ', self.start_easy, font_size=self.font_main)
        self.menu.add_button('     Hard mode     ', self.start_hard, font_size=self.font_main)
        self.menu.add_button('         back         ', self.reset, font_size=self.font_main)

    def start_easy(self):
        #이지모드 하드모드를 제대로 구현 가능하다면 후에 속도를 선택할 수 있는 메뉴와 UI를 만드는 것도 고려 가능할 것 같음.
        #Menu.click.play()
        self.Mode = 'Easy'
        self.tetris.mode = 'Easy'
        self.tetris.run(500) # speed in easy mode
        self.menu.clear()
        #self.show_score(self.Mode, self.tetris.Score)

    def start_hard(self):
        #Menu.click.play()
        self.Mode = 'Hard'
        self.tetris.mode = 'Hard'
        self.tetris.run(200) # speed in hard mode
        self.menu.clear()
        #self.show_score(self.Mode, self.tetris.Score)


    def show_rank(self):
        self.page = 'page2'
        #Menu.click.play()
        self.menu.clear()
        self.mytheme.widget_margin=self.widget_margin_showpage
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_label("   __RANKING__   ", selectable=False, font_size=self.font_main)
        self.menu.add_vertical_margin(self.margin_show)
        self.menu.add_button('     Easy mode ranking     ', self.start_easy, font_size=self.font_main)
        self.menu.add_button('     Hard mode ranking    ', self.start_hard, font_size=self.font_main)
        self.menu.add_button('         back         ', self.reset, font_size=self.font_main)

    def vs_mode(self):
        self.Mode = 'Easy'
        self.tetris.mode = 'Easy'
        self.tetris.run(500) # speed in easy mode
        self.menu.clear()
