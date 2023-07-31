import pygame
import sys
import random
from math import ceil

pygame.font.init()
font = pygame.font.Font('../Assets/SourceCodePro-Black.otf', 15)

WINDOW_HEIGHT = 650
WINDOW_WIDTH = 650
BLACK = (0,0,0)
GOLD = (255,192,0)

# Map Set-Up
map_precise=[]
rows, cols=14,13
for i in range(rows):
    col = []
    for j in range(cols):
        col.append(
        ['G','G','G',
        'G','G',"G",
        'G','G','G']
        )
    map_precise.append(col)
col.clear()

map_unprecise=[]
rows, cols=14,13
for i in range(rows):
    col = []
    for j in range(cols):
        water = random.randint(1, 5)
        if water == 1:
            col.append(-1)
        else:
            col.append(0)
    map_unprecise.append(col)
col.clear()

expansion_queue=[]

# Starting position 
sx = random.randint(0, 12)
sy = random.randint(0, 12)
bx = random.randint(0, 12)
by = random.randint(0, 12)
starting_point = (sx,sy)
map_precise[sx][sy][0] = 'V'
map_unprecise[sx][sy] = 2 
map_unprecise[bx][by] = -2
global money 
money = 25
global army_num
army_num = 0 
global force_limit 
force_limit = 0 
global is_shop 
is_shop = False
global mode
mode = 'WV'
global money_per_turn 
money_per_turn = 25
global turn
turn = 0 
global barbarian_tiles
barbarian_tiles =  1
global capitalexists
capitalexists = 0

def main():
    global mode
    global SCREEN
    global turn
    global money
    global money_per_turn
    global barbarian_tiles
    pygame.init()
    SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    SCREEN.fill(BLACK)
    World_View()
    global map_unprecise
    while True:
        World_View()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                print(mouse)
                if mouse[0] >= 582 and 31 <= mouse[1] <= 69:
                    money += money_per_turn
                    #player expansion
                    while len(expansion_queue) > 0:
                        ex = expansion_queue[0][0]
                        ey = expansion_queue[0][1]
                        print("Executing expansion from", ex, ey)
                        for x in range(max(0, ex-1), min(13, ex+1)+1):
                            for y in range(max(0, ey-1), min(13, ey+1)+1):
                                print(x, y)
                                if map_unprecise[x][y] == 0:
                                    map_unprecise[x][y] = 1
                                    print(x, y)
                        expansion_queue.pop(0)
                    #barbarian expansion
                    chances = barbarian_tiles
                    done = 0
                    for i in range(13):
                        for j in range(13):
                            if map_unprecise[i][j] == -2:
                                z = 1
                                if chances > 1: z = random.randint(1, chances)
                                if z == 1:
                                    print("Barbarian expansion from:", i, j, "to:")
                                    empties = 0
                                    step = 1
                                    while empties == 0:
                                        for x in range(max(0, i-step), min(13, i+step+1)):
                                            for y in range(max(0, j-step), min(13, j+step+1)):
                                                if (x != i or y != j) and map_unprecise[x][y] >= 0:
                                                    empties += 1
                                        if empties == 0: step += 1
                                    l = empties
                                    for k in range(random.randint(0, min(empties, 9))):
                                        minidone = 0
                                        for x in range(max(0, i-step), min(13, i+step+1)):
                                            for y in range(max(0, j-step), min(13, j+step+1)):
                                                if (x != i or y != j) and map_unprecise[x][y] >= 0 and minidone == 0:    
                                                    a = 1
                                                    if l > 1: a = random.randint(1, l)
                                                    if a == 1:
                                                        if map_unprecise[x][y] > 0:
                                                            barbarian_force = barbarian_tiles*25*random.uniform(0.8, 1.25)
                                                            if barbarian_force > min(army_num, force_limit):
                                                                map_unprecise[x][y] = -2
                                                                barbarian_tiles += 1
                                                        elif map_unprecise[x][y] == 0:
                                                            map_unprecise[x][y] = -2
                                                            barbarian_tiles += 1
                                                        minidone = 1
                                                        print(x, y)
                                                        l -= 1
                                    done = 1
                                    break
                                if done == 1: break
                                else: chances -= 1
                        if done == 1: break
                elif map_unprecise[int(mouse[0] / 50)][int(mouse[1] / 50)] >= 1:
                    mode = 'FV'
                    Focused_View(int(mouse[0]/50), int(mouse[1] / 50))
        
        pygame.display.update()

def Shop(xu,yu):
    global money_per_turn
    global money
    global turn
    global barbarian_tiles
    global army_num
    global force_limit 
    global mode
    global capitalexists
    if mode == 'S':
        is_shop = True
        free_tiles = 0
        def money_sign():
            money_text = font.render(str('Gold: ' +  str(money)), False, GOLD)
            SCREEN.blit(money_text, (3,0))
        def tiles_sign(free_tiles):
            for i in range(9):
                if map_precise[xu][yu][i] == 'G':
                    free_tiles+=1
            tiles_text = font.render(str('Tiles Left: ' +  str(free_tiles)), False, GOLD)
            SCREEN.blit(tiles_text, (3,19))
        def sol_sign():
            sol_text = font.render(str('Soldiers: ' +  str(min(force_limit,army_num)) + ' (+' + str(max(0,army_num-force_limit)) + ')'), False, GOLD)
            SCREEN.blit(sol_text, (159,0))
        def fl_sign():
            fl_text = font.render(str('Force limit: ' +  str(force_limit)), False, GOLD)
            SCREEN.blit(fl_text, (159,19))
        SCREEN.fill(BLACK)
        def general_sign(free_tiles):
            SCREEN.fill(BLACK)
            Capt = pygame.image.load("../Assets/Capital.png")
            SCREEN.blit(Capt, (434,0))
            M = pygame.image.load("../Assets/Mill.png")
            SCREEN.blit(M, (217,0))
            F = pygame.image.load("../Assets/Field.png")
            SCREEN.blit(F, (0,0))
            Shop_sign_in_shop = pygame.image.load('../Assets/Shop_sign_in_shop.png')
            SCREEN.blit(Shop_sign_in_shop, (0,0))
            C = pygame.image.load("../Assets/City.png")
            SCREEN.blit(C, (434,217))
            T = pygame.image.load("../Assets/Town.png")
            SCREEN.blit(T, (217,217))
            V = pygame.image.load("../Assets/Village.png")
            SCREEN.blit(V, (0,217))
            MB = pygame.image.load("../Assets/Military_Base.png")
            SCREEN.blit(MB, (434,434))
            B = pygame.image.load("../Assets/Barracks.png")
            SCREEN.blit(B, (217,434))
            TF = pygame.image.load("../Assets/Training_Fields.png")
            SCREEN.blit(TF, (0,434))
            fl_sign()
            money_sign()
            sol_sign()
            tiles_sign(free_tiles)
        general_sign(free_tiles)
        print(
            'This is shop, you can buy upgrades to Your buildings here', '\n'
            'Civilian Infrastructure', '\n'
            'Grass -> Field   | 40 gold  | Field increases force limit by 50', '\n'
            'Field -> Mill    | 80 gold  | Mill increases force limit by 200', '\n'
            'Grass -> Village | 25 gold  | Village gives 25 gold every turn', '\n'
            'Village -> Town  | 50 gold  | Town gives 75 gold every turn', '\n'
            'Town  -> City    | 100 gold | City gives 150 gold every turn','\n'
            'City -> Capital  | 200 gold | Capital gives 250 gold every turn. You can build only one', '\n'
            'Military Utilities', '\n'
            'Grass  ->  Training Fields  | 50 gold  | Training Fields give you 50 army', '\n'
            'Training Fields -> Barracks | 100 gold | Barracks give you 200 army', '\n'
            'Barracks  ->  Military Base | 200 glod | Military Base gives you 400 army', '\n'
            )
        while is_shop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if int(mouse[0]) >= 498 and int(mouse[1]) < 38:
                        MB_num = 0 
                        Mill_num = 0
                        for i in range(0,9):
                            if map_precise[xu][yu][i] == 'MB':
                                MB_num+=1
                            elif map_precise[xu][yu][i] == 'M':
                                Mill_num+=1
                        if MB_num + Mill_num >= 6:
                            print('Player expansion from', str(xu), str(yu), "complete")
                            expansion_queue.append([xu, yu])
                        is_shop = False
                        mode = 'FV'
                        return Focused_View(xu,yu)
                    if is_shop == True:
                        if int(mouse[1]) <= 250 and int(mouse[1]) > 50:
                            if int(mouse[0] <= 217):
                                print('Field')
                                if(money >= 40):
                                    for i in range(9):
                                        if map_precise[xu][yu][i] == 'G':
                                            map_precise[xu][yu][i] = 'F'
                                            money = money - 40
                                            map_unprecise[xu][yu] += 1
                                            force_limit += 50
                                            break
                                general_sign(free_tiles)
                            elif int(mouse[0] <= 434):
                                print('Mill')
                                if(money >= 80):
                                    for i in range(9):
                                        if map_precise[xu][yu][i] == 'F':
                                            map_precise[xu][yu][i] = 'M'
                                            money = money - 80
                                            force_limit += 150
                                            break
                                general_sign(free_tiles)
                            else:
                                print('capital')
                                if(money >= 200):
                                    if capitalexists == 0:
                                        for i in range(9):
                                            if map_precise[xu][yu][i] == 'C':
                                                map_precise[xu][yu][i] = 'Capt'
                                                money = money - 200
                                                money_per_turn += 100
                                                capitalexists = 1
                                                break
                                general_sign(free_tiles)
                        elif int(mouse[1]) <= 440:
                            if int(mouse[0] <= 217):
                                print('Village')
                                if(money >= 25):
                                    for i in range(9):
                                        if map_precise[xu][yu][i] == 'G':
                                            map_precise[xu][yu][i] = 'V'
                                            money = money - 25
                                            map_unprecise[xu][yu] += 1
                                            money_per_turn += 25
                                            break
                                general_sign(free_tiles)
                            elif int(mouse[0] <= 434):
                                print('Town')
                                if(money >= 50):
                                    for i in range(9):
                                        if map_precise[xu][yu][i] == 'V':
                                            map_precise[xu][yu][i] = 'T'
                                            money = money - 50
                                            money_per_turn += 50
                                            break
                                general_sign(free_tiles)
                            elif(int(mouse[1]) <= 440 and int(mouse[1]) > 30):
                                print('City')
                                if(money >= 100):
                                    for i in range(9):
                                        if map_precise[xu][yu][i] == 'T':
                                            map_precise[xu][yu][i] = 'C'
                                            money = money - 100
                                            money_per_turn += 75
                                            break
                                general_sign(free_tiles)
                        elif int(mouse[1]) >= 440:
                            if int(mouse[0] <= 217):
                                print('Training Fields')
                                if(money >= 50):
                                    for i in range(9):
                                        if map_precise[xu][yu][i] == 'G':
                                            map_precise[xu][yu][i] = 'TF'
                                            money = money - 50
                                            map_unprecise[xu][yu] += 1
                                            army_num += 50
                                            break
                                general_sign(free_tiles)
                            elif int(mouse[0] <= 434):
                                print('Barracks')
                                if(money >= 100):
                                    for i in range(9):
                                        if map_precise[xu][yu][i] == 'TF':
                                            map_precise[xu][yu][i] = 'B'
                                            money = money - 100
                                            army_num += 150
                                            break
                                general_sign(free_tiles)
                            else:
                                print('Military Base')
                                if(money >= 200):
                                    for i in range(9):
                                        if map_precise[xu][yu][i] == 'B':
                                            map_precise[xu][yu][i] = 'MB'
                                            money = money - 200
                                            army_num += 200
                                            break
                                general_sign(free_tiles)
            pygame.display.update()

def Focused_View(xu,yu):
    global turn
    global mode
    if mode == 'FV':
        is_shop = False
        Shop_sign = pygame.image.load('../Assets/Shop_sign.png')
        img_Gz2 = pygame.image.load('../Assets/Gz2.png')
        img_Vp = pygame.image.load('../Assets/Village.png')
        F_img = pygame.image.load('../Assets/Field.png')
        M_img = pygame.image.load('../Assets/Mill.png')
        T_img = pygame.image.load('../Assets/Town.png')
        C_img = pygame.image.load('../Assets/City.png')
        Capt_img = pygame.image.load('../Assets/Capital.png')
        TF_img = pygame.image.load('../Assets/Training_Fields.png')
        B_img = pygame.image.load('../Assets/Barracks.png')
        MB_img = pygame.image.load('../Assets/Military_Base.png')
        img_size = 217
        yi = [5, 3, 7, 1, 0, 2, 6, 4, 8]
        yiprint = [5, 1, 6, 3, 0, 4, 7, 2, 8]
        yi_pos = 0
        for x in range(0,WINDOW_WIDTH,img_size):
            for y in range(0,WINDOW_HEIGHT, img_size):
                global map_precise
                print(map_precise[xu][yu][yiprint[yi_pos]], end=" ")
                if map_precise[xu][yu][yi[yi_pos]] == 'V':
                    SCREEN.blit(img_Vp, (x,y))
                if map_precise[xu][yu][yi[yi_pos]] == 'F':
                    SCREEN.blit(F_img, (x,y))
                if map_precise[xu][yu][yi[yi_pos]] == 'M':
                    SCREEN.blit(M_img, (x,y))
                if map_precise[xu][yu][yi[yi_pos]] == 'T':
                    SCREEN.blit(T_img, (x,y))
                if map_precise[xu][yu][yi[yi_pos]] == 'C':
                    SCREEN.blit(C_img, (x,y))
                if map_precise[xu][yu][yi[yi_pos]] == 'Capt':
                    SCREEN.blit(Capt_img, (x,y))
                if map_precise[xu][yu][yi[yi_pos]] == 'TF':
                    SCREEN.blit(TF_img, (x,y))
                if map_precise[xu][yu][yi[yi_pos]] == 'B':
                    SCREEN.blit(B_img, (x,y))
                if map_precise[xu][yu][yi[yi_pos]] == 'MB':
                    SCREEN.blit(MB_img, (x,y))
                if map_precise[xu][yu][yi[yi_pos]] == 'G':
                    SCREEN.blit(img_Gz2, (x,y))
                yi_pos = yi_pos + 1
            print()
        SCREEN.blit(Shop_sign, (0,0))
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    if int(mouse[1]) < 38 and int(mouse[0] < 89):
                        mode = 'S'
                        return Shop(xu,yu)
                    else:
                        mode = 'WV'
                        return main()

            pygame.display.update()


def World_View(): 
    global mode
    global army_num
    global force_limit
    if mode == 'WV':
        is_shop = False
        img_F = pygame.image.load('../Assets/G.png')
        img_T0 = pygame.image.load('../Assets/T0.png')
        img_T1 = pygame.image.load('../Assets/T1.png')
        img_T2 = pygame.image.load('../Assets/T2.png')
        img_T3 = pygame.image.load('../Assets/T3.png')
        img_T4 = pygame.image.load('../Assets/T4.png')
        img_T5 = pygame.image.load('../Assets/T5.png')
        img_T6 = pygame.image.load('../Assets/T6.png')
        img_T7 = pygame.image.load('../Assets/T7.png')
        img_T8 = pygame.image.load('../Assets/T8.png')
        img_T9 = pygame.image.load('../Assets/T9.png')
        img_W = pygame.image.load('../Assets/W.png')
        img_B = pygame.image.load('../Assets/B.png')
        img_size = 50
        xi = 0
        yi = 0
        
        for x in range(0,WINDOW_WIDTH, img_size):
            for y in range(0, WINDOW_HEIGHT, img_size):
                global map_unprecise
                if map_unprecise[xi][yi] == 1:
                    SCREEN.blit(img_T0, (x,y))
                elif map_unprecise[xi][yi] == 2:
                    SCREEN.blit(img_T1, (x,y))
                elif map_unprecise[xi][yi] == 3:
                    SCREEN.blit(img_T2, (x,y))
                elif map_unprecise[xi][yi] == 4:
                    SCREEN.blit(img_T3, (x,y))
                elif map_unprecise[xi][yi] == 5:
                    SCREEN.blit(img_T4, (x,y))
                elif map_unprecise[xi][yi] == 6:
                    SCREEN.blit(img_T5, (x,y))
                elif map_unprecise[xi][yi] == 7:
                    SCREEN.blit(img_T6, (x,y))
                elif map_unprecise[xi][yi] == 8:
                    SCREEN.blit(img_T7, (x,y))
                elif map_unprecise[xi][yi] == 9:
                    SCREEN.blit(img_T8, (x,y))
                elif map_unprecise[xi][yi] == 10:
                    SCREEN.blit(img_T9, (x,y))
                elif map_unprecise[xi][yi] == -1:
                    SCREEN.blit(img_W, (x,y))
                elif map_unprecise[xi][yi] == 0:
                    SCREEN.blit(img_F, (x,y))
                elif(map_unprecise[xi][yi] == -2):
                    SCREEN.blit(img_B, (x,y))
                yi = yi + 1
            xi = xi + 1
            yi = 0
        img_End_Turn = pygame.image.load('../Assets/End_turn_sign.png')
        SCREEN.blit(img_End_Turn, (570, 19))
        pygame.display.update()

main()
