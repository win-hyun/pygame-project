import os
import pygame


pygame.init() # 초기화

# 화면 크기 설정
screen_width = 640 # 가로크기
screen_height = 480 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

#화면 타이틀 설정
pygame.display.set_caption("팡 게임") # 게임 이름 

#FPS
clock = pygame.time.Clock()

#배경 이미지 삽입
current_path = os.path.dirname(__file__) #현재 파일의 위치 반환 
image_path = os.path.join(current_path, "images") # images 폴더 위치 반환

# 배경 만들기
background = pygame.image.load(os.path.join(image_path, "background.png"))
# 스테이지 만들기
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1] # 스테이지의 높이 위에 캐릭터를 두기 위해


# 캐릭터 불러오기
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size #이미지 크기 구함
character_width = character_size[0] # 가로크기
character_height = character_size[1] # 세로크기
character_x_pos = (screen_width / 2) - (character_width / 2)  # 화면 가로의 절반 크기에 해당하는 곳에 위치
character_y_pos = screen_height - character_height - stage_height


#이동할 좌표
character_to_x =0

# 이동 속도
character_speed = 5

# 무기 만들기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 한번에 여러 발 발사 가능
weapons = []

#무기 이동 속도
weapon_speed = 10

#공 만들기
ball_images = [
    pygame.image.load(os.path.join(image_path, "baloon1.png")),
    pygame.image.load(os.path.join(image_path, "baloon2.png")),
    pygame.image.load(os.path.join(image_path, "baloon3.png")),
    pygame.image.load(os.path.join(image_path, "baloon4.png"))]

 # 공 크기에 따른 스피드 값 설정   
ball_speed_y = [-18, -15, -12, -9] #index값으로 처리

 #공
balls = []

balls.append({
     "pos_x" : 50, # 공의 x 좌표
     "pos_y" : 50, # 공의 y 좌표
     "img_idx" : 0, # 공의 이미지 인텍스
     "to_x": 3, # 공의 이동 방향 -3이면 왼쪽 3이면 오른쪽  
     "to_y": -6, # y축 이동 방향 
     "init_spd_y": ball_speed_y[0]})# y의 최초 속도 

#사라질 무기, 공 정보 저장 변수
weapon_to_remove = -1
ball_to_remove = -1

# Font 정의
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks()

game_result = "Game Over"

#이벤트 루프
running = True #게임이 진행중인가 확인함
while running:
    dt = clock.tick(30) # 게임화면의 초당 프레임 수를 설정 

    #이벤트 처리
    for event in pygame.event.get(): # 어떤 이벤트가 발생하였는가?
        if event.type == pygame.QUIT: # 창을 끄는 x버튼을 눌렀을때 이 구문이 실행됩니다. 
            running = False # 게임이 실행중이 아님

        if event.type == pygame.KEYDOWN: #키가 눌러졌는지 확인
            if event.key == pygame.K_LEFT: # 캐릭터 왼쪽으로 이동
                character_to_x -= character_speed # to_x = to_x - 5랑 똑같음 
            elif event.key == pygame.K_RIGHT: # 캐릭터 오른쪽으로 이동
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE: #무기 발사
               weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
               weapon_y_pos = character_y_pos
               weapons.append([weapon_x_pos, weapon_y_pos])

        if event.type == pygame.KEYUP: # 방향키를 떼면 멈춘다
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0
           
    # 게임 캐릭터 위치 정의
    character_x_pos += character_to_x
  

    #가로 경계값 처리 캐릭터가 배경에서 벗어나지 않도록
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width
     #세로 경계값 처리 캐릭터가 배경에서 벗어나지 않도록
    if character_y_pos < 0:
        character_y_pos = 0
    elif character_y_pos > screen_height - character_height:
        character_y_pos = screen_height - character_height 
    
    #무기 위치 조정
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons] #무기 위치를 올린다
    
    #천장에 닿은 무기 없애기
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]
    
    #공 위치 조정
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
        
        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]
    
        # 가로벽에 닿았을 때 공 위치 이동 
        if ball_pos_x <= 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1

        #세로 위치
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"] 
        else: # 속도를 증가
            ball_val["to_y"] += 0.5  

        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]

    # 충돌 처리

    # 캐릭터 rext 정보
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]
       
        # 공 rect 정보 업데이트 
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        #공과 캐릭터에 충돌 처리
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # 공과 무기들 충돌 처리
        for weapon_idx, weapon_val in enumerate(weapons):
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            #무기 정보 
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            #충돌 체크
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # 해당 무기 없애기 위한 값 설정
                ball_to_remove = ball_idx # 해당 공 없애기 위한 값 설정

                # 가장 작은 크기의 공이 아니라면 다음 단계의 공으로 나눠주기
                if ball_img_idx < 3:
                    # 현재 공 크기 정보를 가지고 옴
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # 나눠진 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # 왼쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # 공의 x 좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # 공의 y 좌표
                        "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                        "to_x": -3, # x축 이동방향, -3 이면 왼쪽으로, 3 이면 오른쪽으로
                        "to_y": -6, # y축 이동방향,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]})# y 최초 속도

                    # 오른쪽으로 튕겨나가는 작은 공
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # 공의 x 좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # 공의 y 좌표
                        "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                        "to_x": 3, # x축 이동방향, -3 이면 왼쪽으로, 3 이면 오른쪽으로
                        "to_y": -6, # y축 이동방향,
                        "init_spd_y": ball_speed_y[ball_img_idx + 1]})# y 최초 속도


                break
            else:
                continue
            break

    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1

    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 공을 없앤 경우 게임 종료
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False


    screen.blit(background, (0, 0)) #배경 그리기

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))
        
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0, screen_height - stage_height)) #스테이지 만들기
    screen.blit(character, (character_x_pos, character_y_pos))
    
    #경과 시간
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255,255,255))
    screen.blit(timer, (10, 10))

    #시간 초과했다면
    if total_time - elapsed_time <= 0:
        game_Result = "Time Over"
        running = False

 
    pygame.display.update() # 게임화면을 다시 그리기 pygame에서 필수 
    
msg = game_font.render(game_result, True, (255, 255, 0)) # 노란색
msg_rect = msg.get_rect(center=(int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

pygame.time.delay(2000) # 2초대기
# pygame 종료
pygame.quit()