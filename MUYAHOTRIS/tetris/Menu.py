# -*- coding: utf-8 -*-
#https://pygame-menu.readthedocs.io/en/latest/_source/add_widgets.html
#https://github.com/ppizarror/pygame-menu
# 참고해서 메뉴 만들어 봅시다!

import pygame
import pygame_menu
from Tetris import *
import time
from Variable import *
from Database import *

class Menu:

    def __init__(self):
        pygame.init()
        MN.infoObject = pygame.display.Info()
        self.tetris=Tetris()
        self.database = Database()
        (MN.menu_display_w, MN.menu_display_h) = pygame.display.get_surface().get_size()
        self.w = MN.menu_display_w
        self.h = MN.menu_display_h
        self.Mode = MN.initial_mode
        self.id= MN.initial_id
        self.score=Set.init_score
        self.level=Set.init_level
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
        icon = pygame.image.load(Image.icon_ref)
        pygame.display.set_icon(icon)
        pygame.display.set_caption('MUYAHOTRIS')
        self.surface = pygame.display.set_mode((self.w, self.h), RESIZABLE)
        self.page=MN.initial_page   #시작하면 기본 모드로 모드가 설정
        self.menu.clear()
        self.mytheme.widget_margin=self.widget_margin_main
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_button('   Single Mode   ', self.show_game,font_size=self.font_main)
        self.menu.add_button('    Level Mode    ', self.level_mode,font_size=self.font_main)
        self.menu.add_button('  Ranking  ', self.show_rank,font_size=self.font_main)
        self.menu.add_button('  Help  ', self.help, font_size=self.font_main)
        self.menu.add_button('        Exit         ', pygame_menu.events.EXIT,font_size=self.font_main)


    def reset(self):  ## 뒤로 갈때 보여줄 목록들
        self.surface = pygame.display.set_mode((self.w, self.h), RESIZABLE)
        self.mytheme.background_color = Image.main_image
        self.menu = pygame_menu.Menu(self.h, self.w, '', theme=self.mytheme)
        self.mytheme.widget_margin=self.widget_margin_main
        #Menu.click.play()
        self.page=MN.initial_page
        self.menu.clear()
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_button('   Single Mode   ', self.show_game,font_size=self.font_main)
        self.menu.add_button('    Level Mode    ', self.level_mode,font_size=self.font_main)
        self.menu.add_button('  Ranking  ', self.show_rank,font_size=self.font_main)
        self.menu.add_button('  Help  ', self.help, font_size=self.font_main)
        self.menu.add_button('        Exit         ', pygame_menu.events.EXIT,font_size=self.font_main)

    def help(self): # help 페이
        self.page='page7'
        (resize.display_width,resize.display_height) = pygame.display.get_surface().get_size()
        self.surface = pygame.display.set_mode((resize.display_width,resize.display_height))
        self.mytheme.background_color = Image.help_image
        self.menu = pygame_menu.Menu(width=resize.display_width, height=resize.display_height, title='',theme=self.mytheme)
        self.margin_help = MN.margin_help
        self.menu.add_vertical_margin(self.margin_help)
        self.menu.add_button(' back ', self.reset, font_size=self.font_sub)

    def show_game(self):
        self.page = 'page1'
        #Menu.click.play()
        self.menu.clear()
        self.mytheme.widget_margin=self.widget_margin_showpage
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_label("   - Select Menu -   ", selectable=False, font_size=self.font_main)
        self.menu.add_vertical_margin(self.margin_show)
        self.menu.add_button('     Easy mode     ', self.start_easy, font_size=self.font_main)
        self.menu.add_button('     Hard mode     ', self.start_hard, font_size=self.font_main)
        self.menu.add_button('         back         ', self.reset, font_size=self.font_main)

    def start_easy(self):
        #이지모드 하드모드를 제대로 구현 가능하다면 후에 속도를 선택할 수 있는 메뉴와 UI를 만드는 것도 고려 가능할 것 같음.
        #Menu.click.play()
        self.Mode = 'Easy'
        self.tetris.mode = 'Easy'
        self.tetris.run(MN.start_easy, 'EASY') # speed in easy mode
        self.menu.clear()
        self.show_score(self.Mode, self.tetris.Score)

    def start_hard(self):
        #Menu.click.play()
        self.Mode = 'Hard'
        self.tetris.mode = 'Hard'
        self.tetris.run(MN.start_hard, 'HARD') # speed in hard mode
        self.menu.clear()
        self.show_score(self.Mode, self.tetris.Score)

    def show_score(self, game_mode, game_score):
        self.page = 'page6'
        self.Mode = game_mode
        self.score = game_score
        self.menu.clear()
        self.surfuace = pygame.display.set_mode((self.w,self.h), RESIZABLE)
        self.mytheme.widget_margin=self.widget_margin_main
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_text_input('ID: ',maxchar=3, onreturn=self.save_id,font_size=self.font_main)
        self.menu.add_button('back', self.reset, font_size=self.font_main)
        self.menu.add_button('EXIT',pygame_menu.events.EXIT,font_size=self.font_main)

    def save_id(self, value):
        self.id = value
        self.database.add_data(self.Mode, self.id, self.score)
        self.reset()


    def show_rank(self):
        self.page = 'page2'
        #Menu.click.play()
        self.menu.clear()
        self.mytheme.widget_margin=self.widget_margin_showpage
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_label("   - RANKING -   ", selectable=False, font_size=self.font_main)
        self.menu.add_vertical_margin(self.margin_show)
        self.menu.add_button('     Easy mode ranking     ', self.easy_rank, font_size=self.font_main)
        self.menu.add_button('     Hard mode ranking    ', self.hard_rank, font_size=self.font_main)
        self.menu.add_button('     Level mode ranking    ', self.level_rank, font_size=self.font_main)
        self.menu.add_button('         back         ', self.reset, font_size=self.font_main)

    def easy_rank(self):
        self.page='page3'
        #Menu.click.play()
        self.menu.clear()
        self.mytheme.widget_margin=self.widget_margin_rank
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_label("--Easy Rank--",selectable=False,font_size=self.font_main)
        self.menu.add_label("ID        Score",selectable=False, font_size=self.font_main)
        easy_data = self.database.load_data('Easy')
        if len(easy_data)>Set.show_rank_five:
            for i in range(Set.show_rank_five):
                easy_name = str(easy_data[i]['ID'])
                easy_score = '{0:>05s}'.format(str(easy_data[i]['score']))
                r= "#{} : ".format(i+1) + easy_name + "    " + easy_score
                self.menu.add_button(r,font_size=self.font_main)
        else:
            for i in range(len(easy_data)):
                easy_name = str(easy_data[i]['ID'])
                easy_score = '{0:>05s}'.format(str(easy_data[i]['score']))
                r= "#{} : ".format(i+1) + easy_name + "    " + easy_score
                self.menu.add_button(r,font_size=self.font_main)
        self.menu.add_button('back', self.reset,font_size=self.font_sub)

    def hard_rank(self):
        self.page='page4'
        #menu.click.play()
        self.menu.clear()
        self.mytheme.widget_margin=self.widget_margin_rank
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_label("--Hard Rank--",selectable=False,font_size=self.font_main)
        self.menu.add_label("ID        Score",selectable=False, font_size=self.font_main)
        hard_data = self.database.load_data('Hard')
        if len(hard_data)>Set.show_rank_five:
            for i in range(Set.show_rank_five):
                hard_name = str(easy_data[i]['ID'])
                hard_score = '{0:>05s}'.format(str(hard_data[i]['score']))
                r= "#{} : ".format(i+1) + hard_name + "    " + hard_score
                self.menu.add_button(r,font_size=self.font_main)
        else:
            for i in range(len(hard_data)):
                hard_name = str(hard_data[i]['ID'])
                hard_score = '{0:>05s}'.format(str(hard_data[i]['score']))
                r= "#{} : ".format(i+1) + hard_name + "    " + hard_score
                self.menu.add_button(r,font_size=self.font_main)
        self.menu.add_button('back', self.reset,font_size=self.font_sub)

    def level_rank(self):
        self.page='page5'
        #menu.click.play()
        self.menu.clear()
        self.mytheme.widget_margin=self.widget_margin_rank
        self.menu.add_vertical_margin(self.margin_main)
        self.menu.add_label("--Level Rank--",selectable=False,font_size=self.font_main)
        self.menu.add_label("ID        Level",selectable=False, font_size=self.font_main)
        level_data = self.database.load_data('Level')
        if len(level_data)>Set.show_rank_five:
            for i in range(Set.show_rank_five):
                level_name = str(level_data[i]['ID'])
                level_score = '{0:>05s}'.format(str(level_data[i]['level']))
                #level_lines = '{0:>05s}'.format(str(level_data[i]['lines']))
                r= "#{} : ".format(i+1) + level_name + "    " + level_score #+ "     " + level_lines
                self.menu.add_button(r,font_size=self.font_main)
        else:
            for i in range(len(level_data)):
                level_name = str(level_data[i]['ID'])
                level_score = '{0:>05s}'.format(str(level_data[i]['level']))
                #level_lines = '{0:>05s}'.format(str(level_data[i]['lines']))
                r= "#{} : ".format(i+1) + level_name + "    " + level_score #+ "     " + level_lines
                self.menu.add_button(r,font_size=self.font_main)
        self.menu.add_button('back', self.reset,font_size=self.font_sub)

    def level_mode(self):
        self.Mode = 'Level'
        self.tetris.mode = 'Level'
        self.tetris.run(MN.start_easy, 'Level') # speed in easy mode
        self.menu.clear()
        self.show_score(self.Mode, self.tetris.Level)
