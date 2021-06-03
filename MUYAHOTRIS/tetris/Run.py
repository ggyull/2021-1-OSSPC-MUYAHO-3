# -*- coding: utf-8 -*-
from Menu import *
from Tetris import *
from Variable import *

mymenu=Menu()
mymenu.run()
# 실행 파일
while True:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            exit()
        elif event.type == VIDEORESIZE:
            mymenu.w=event.w
            mymenu.h=event.h
            pre_display_width = resize.display_width
            pre_display_height = resize.display_height
            (resize.display_width, resize.display_height) = pygame.display.get_surface().get_size()
            if resize.display_width <= resize.min_display_w:
                resize.display_width = resize.min_display_w
            if resize.display_height <= resize.min_display_h:
                resize.display_height = resize.min_display_h
            var_display_width_rate = resize.display_width / pre_display_width
            var_display_height_rate = resize.display_height / pre_display_height
            Image.combo_image_width = int(Image.combo_image_width * var_display_width_rate)
            Image.combo_image_height = int(Image.combo_image_height * var_display_height_rate)
            Image.combo_image_size = (Image.combo_image_width, Image.combo_image_height)
            Image.combo_image_init_y = int(Image.combo_image_init_y * var_display_height_rate)
            if event.w < MN.min_display_w:   #최소 사이즈 정하기
                mymenu.w = MN.min_display_w
            if event.h < MN.min_display_h:
                mymenu.h = MN.min_display_h
            mymenu.surface = pygame.display.set_mode((mymenu.w, mymenu.h), RESIZABLE) #리사이징 된걸로 새로 창 설정
            mymenu.menu = pygame_menu.Menu(mymenu.h, mymenu.w, '', theme=MN.mytheme)
            mymenu.menu.draw(mymenu.surface)
            mymenu.font_main=int((mymenu.h)/MN.font_rate_main)
            mymenu.font_sub=int((mymenu.h)/MN.font_rate_sub)

            mymenu.margin_main=int((mymenu.h)/MN.rate_main)
            mymenu.margin_help = int((mymenu.h)/MN.rate_help)
            mymenu.margin_show= int((mymenu.h)/MN.rate_show)
            mymenu.margin_rank=int((mymenu.h)/MN.rate_rank)

            mymenu.widget_margin_main = (MN.widget_center, int((mymenu.h) / MN.widget_rate_main))
            mymenu.widget_margin_showpage = (MN.widget_center, int((mymenu.h) / MN.widget_rate_showpage))
            mymenu.widget_margin_rank = (MN.widget_center, int((mymenu.h) / MN.widget_rate_rank))

            #time.sleep(MN.sleep_time) # 페이지 변환 너무 빨라 렉걸리는 거 방지하기 위해 없어도 큰 상관 없음
            if mymenu.page=='page0': #리사이징 후 원래 페이지로 돌아가기
                mymenu.run()
            elif mymenu.page=='page1':
                mymenu.show_game()
            elif mymenu.page=='page2':
                mymenu.show_rank()
            elif mymenu.page=='page3':
                mymenu.easy_rank()
            elif mymenu.page=='page4':
                mymenu.hard_rank()
            elif mymenu.page=='page5':
                mymenu.Mini_the_rank()
            elif mymenu.page=='page6':
                mymenu.show_score(mymenu.Mode,mymenu.tetris.Score)
            elif mymenu.page=='page7':
                mymenu.help()


    if mymenu.menu.is_enabled():
        mymenu.menu.update(events)
        mymenu.menu.draw(mymenu.surface)
    pygame.display.update()
