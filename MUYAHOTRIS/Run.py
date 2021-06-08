from Menu import *
from Tetris import *
from Variable import *

mymenu=Menu()   #메뉴 객체 생성
mymenu.run()    #실행 파일

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
            (resize.display_width, resize.display_height) = pygame.display.get_surface().get_size()     #현재 창 크기 받아오기
            if resize.display_width <= resize.min_display_w:                                            #리사이즈 최소 조건 너비
                resize.display_width = resize.min_display_w
            if resize.display_height <= resize.min_display_h:                                           #리사이즈 최소 조건 높이
                resize.display_height = resize.min_display_h
            var_display_width_rate = resize.display_width / pre_display_width                           #리사이즈 너비 비율
            var_display_height_rate = resize.display_height / pre_display_height                        #리사이즈 높이 비율
            Image.combo_image_width = int(Image.combo_image_width * var_display_width_rate)             #콤보 점수 이미지 너비 재설정
            Image.combo_image_height = int(Image.combo_image_height * var_display_height_rate)          #콤보 점수 이미지 높이 재설정
            Image.combo_image_size = (Image.combo_image_width, Image.combo_image_height)                #콤보 이미지 사이즈
            Image.combo_image_init_y = int(Image.combo_image_init_y * var_display_height_rate)          #콤보 이미지
            if event.w < MN.min_display_w:
                mymenu.w = MN.min_display_w
            if event.h < MN.min_display_h:
                mymenu.h = MN.min_display_h
            mymenu.surface = pygame.display.set_mode((mymenu.w, mymenu.h), RESIZABLE)                   #리사이징 된걸로 새로 창 설정
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

            #리사이징 후 원래 페이지로 돌아가기
            if mymenu.page=='page0':
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
                mymenu.level_rank()
            elif mymenu.page=='page6':
                mymenu.show_score(mymenu.Mode,mymenu.tetris.Score)
            elif mymenu.page=='page7':
                mymenu.help()

    if mymenu.menu.is_enabled():                                                                        #메뉴가 활성화될 시
        mymenu.menu.update(events)                                                                      #이벤트 업데이트
        mymenu.menu.draw(mymenu.surface)                                                                #그리기
    pygame.display.update()                                                                             #디스플레이 업데이트
