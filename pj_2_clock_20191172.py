# Draw a robot arm with multiple joints, controlled with keyboard inputs
#
# -*- coding: utf-8 -*- 
import time
import pygame
import numpy as np



# 게임 윈도우 크기
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def Rmat(degree):
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array( [[ c, -s, 0], [s, c, 0], [0, 0, 1] ] )
    return R

def Tmat(a,b):
    H = np.eye(3)
    H[0,2] = a
    H[1,2] = b
    return H


# Pygame 초기화
pygame.init()

# 윈도우 제목
pygame.display.set_caption("Drawing")

# 윈도우 생성
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 게임 화면 업데이트 속도
clock = pygame.time.Clock()

# 게임 종료 전까지 반복
done = False
# 폰트 선택(폰트, 크기, 두껍게, 이탤릭)
font = pygame.font.SysFont('FixedSys', 40, True, False)
font_2 = pygame.font.SysFont('Arial', 80, True, False)

# poly: 4 x 3 matrix
hour_hand = np.array( [[0, 0, 1], [120, 0, 1], [120, 20, 1], [0, 20, 1]])
min_hand = np.array([[0, 0, 1], [180, 0, 1], [180, 20, 1], [0, 20, 1]])
sec_hand = np.array([[0, 0, 1], [200, 0, 1], [200, 20, 1], [0, 20, 1]])

hour_hand = hour_hand.T # 3x4 matrix 
min_hand = min_hand.T
sec_hand = sec_hand.T

cor = np.array([10, 10, 1])



# 게임 반복 구간
while not done:
# 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # 윈도우 화면 채우기
    screen.fill(WHITE)
    now = time
    hourick = now.localtime().tm_hour

    if hourick > 12:
        hourick = hourick % 12
    
    minick = now.localtime().tm_min
    secick = now.localtime().tm_sec

    # 다각형 그리기
    # poly: 3xN 
    
    degree = 30 * (hourick) - 90
    degree_2 = 6 * (minick) - 90
    degree_3 = - 90 + 6 * (secick) 


    Hour_ = Tmat(300, 300) @ Tmat(0, 0) @ Rmat(degree) @ Tmat(-10, -10)

    Minute_ = Tmat(300, 300) @ Tmat(0, 0) @ Rmat(degree_2) @ Tmat(-10, -10)

    Sec_ = Tmat(300, 300) @Tmat(0, 0) @ Rmat(degree_3) @ Tmat(-10, -10)



    pp = Hour_ @ hour_hand
    pp_2 = Minute_ @ min_hand
    pp_3 = Sec_ @ sec_hand
    
    corp = Hour_ @ cor
    # print(pp.shape, pp, pp.T )

    q = pp[0:2, :].T # N x 2 matrix
    q_2 = pp_2[0:2, :].T
    q_3 = pp_3[0:2, :].T

    pygame.draw.polygon(screen, BLACK, q, 4)
    pygame.draw.polygon(screen, BLACK, q_2, 4)
    pygame.draw.polygon(screen, BLACK, q_3, 4)
    
    
    pygame.draw.circle(screen, (255, 128, 128), corp[:2], 3)
    

    # 안티얼리어스를 적용하고 검은색 문자열 렌더링



    text_n12 = font_2.render("12", True, BLACK)
    text_n6 = font_2.render("6", True, BLACK)
    text_n3 = font_2.render("3", True, BLACK)
    text_n9 = font_2.render("9", True, BLACK)


    text_clock = font.render(f"{hourick}:{minick}:{secick}", True, BLACK)

  
    screen.blit(text_clock, [100,100])

    Rect_12x = text_n12.get_rect()
    Rect_12x.centerx = round(WINDOW_WIDTH/2)
    Rect_12x.y = 0
    
    Rect_6x = text_n6.get_rect()
    Rect_6x.centerx = round(WINDOW_WIDTH/2)
    Rect_6x.y = 520

    Rect_3y = text_n3.get_rect()
    Rect_3y.x = 540
    Rect_3y.centery = round(WINDOW_HEIGHT/2)

    Rect_9y = text_n9.get_rect()
    Rect_9y.x = 0
    Rect_9y.centery = round(WINDOW_HEIGHT/2)



    screen.blit(text_n12, Rect_12x)
    screen.blit(text_n6, Rect_6x)
    screen.blit(text_n3, Rect_3y)
    screen.blit(text_n9, Rect_9y)



    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

# 게임 종료
pygame.quit()