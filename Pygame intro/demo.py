import pygame
from random import randint

def display_score():
    score = pygame.time.get_ticks() // 1000 - reset_score
    score_surf = text_font.render(f"Score: {score}",False,'Black')
    score_rect = score_surf.get_rect(center=(400,50))
    screen.blit(score_surf,score_rect)
    return score

def display_obstacle(obstacle_list):
    if obstacle_list:
        for obstacle in obstacle_list:
            obstacle.x -= 3
            if obstacle.right < 0: obstacle_list = obstacle_list[1:]

            if obstacle.bottom == 300:
                screen.blit(snail,obstacle)
            else:
                screen.blit(fly,obstacle)

    return obstacle_list if obstacle_list != [] else []

def collition(player,obstacle_list):
    for obstacle in obstacle_list:
        if player.colliderect(obstacle):
            return True
    return False

def player_animation():
    global player,player_index
    if player_rect.bottom < 300:
        player = player_jump
    else:
        player_index += 0.1
        if player_index >= 2: player_index = 0
        player = player_list[int(player_index)]

pygame.init()
screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()
gameOver = False
score = pygame.time.get_ticks() // 1000
Total_score = 0
reset_score = 0

sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/ground.png').convert()

text_font = pygame.font.Font('font/Pixeltype.ttf',50)

snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
snail_list = [snail_1,snail_2]
snail_index = 0
snail = snail_list[snail_index]


fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
fly_list = [fly_1,fly_2]
fly_index = 0
fly = fly_list[fly_index]

obstackle_rect_list = []

player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()
player_list = [player_walk_1,player_walk_2]

player_index = 0
player = player_list[player_index]
player_rect = player.get_rect(midbottom=(80,300))
player_gravity = 0

player_stand = pygame.image.load('graphics/Player/player_stand.png').convert_alpha()
player_stand = pygame.transform.scale2x(player_stand)
player_stand_rect = player_stand.get_rect(center=(400,200))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1000)

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer,500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer,200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        if not gameOver:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom >= 300:
                    player_gravity = -8

            if event.type == obstacle_timer:
                if randint(0,2):
                    obstackle_rect_list.append(snail.get_rect(bottomleft = (randint(800,1000),300)))
                else:
                    obstackle_rect_list.append(fly.get_rect(bottomleft = (randint(800,1000),210)))

            if event.type == snail_animation_timer:
                if snail_index == 0: snail_index = 1
                else: snail_index = 0
                snail = snail_list[snail_index]

            if event.type == fly_animation_timer:
                if fly_index == 0: fly_index = 1
                else: fly_index = 0
                fly = fly_list[fly_index]

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gameOver = False
                reset_score = pygame.time.get_ticks() // 1000
                Total_score = 0

    if gameOver:
        screen.fill('#34566b')
        score_surf = text_font.render(f"Game Over. Total Score: {Total_score}",False,'Black')
        score_rect = score_surf.get_rect(center=(400,50))
        screen.blit(score_surf,score_rect)
        screen.blit(player_stand,player_stand_rect)

        text_surf = text_font.render(f"Press Space to Start",True,'Black')
        text_rect = text_surf.get_rect(center=(400,350))
        screen.blit(text_surf,text_rect)

        obstackle_rect_list = []
        player_rect.bottom = 300
    else:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,300))
        Total_score = display_score()

        obstackle_rect_list = display_obstacle(obstackle_rect_list)

        player_gravity += 0.2
        player_rect.y += player_gravity
        if player_rect.bottom >= 300:
            player_rect.bottom = 300
            player_gravity = 0
        player_animation()
        screen.blit(player,player_rect)

        gameOver = collition(player_rect,obstackle_rect_list)
    
    pygame.display.update()
    clock.tick(120)