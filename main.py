import pygame
from sys import exit
from random import randint

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time

    score_surface = text_font.render(f'Score : {current_time}', True, "Black")
    score_rect = score_surface.get_rect(center = (360,75))
    
    pygame.draw.rect(screen,'White',score_rect,1,5)
    screen.blit(score_surface,score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            
            obstacle_rect.x -= 5
            
            if obstacle_rect.bottom == 300: screen.blit(snail_surface,obstacle_rect)
            else: screen.blit(fly_surface,obstacle_rect)

            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -50 ]

        return obstacle_list
    else: 
        return[]
    
def collisions(player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect): return False
    return True


pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((720, 480))

start_time = 0

text_font = pygame.font.Font("Fonts\TarrgetAcademyItalic-qzmx.otf",25)

pygame.display.set_caption("Untitled Runner Game")

game_active = True

sky_surface =  pygame.Surface((720,380))

ground_surface = pygame.Surface((720,100))

score_surface = text_font.render('Score', True, "Black")
score_rect = score_surface.get_rect(center = (360,75))

player_surface = pygame.Surface((60,60))
player_rect = player_surface.get_rect(midbottom = (75,380))

player_gravity = 0

player_speed = 0

snail_surface = pygame.Surface((50,50))

fly_surface = pygame.Surface((50,100))

obstacle_rect_list = []

collide_count = 0
MAX_COLLIDE_COUNT = 2
player_touching_obstacle = False

sky_surface.fill("Grey")
ground_surface.fill("Black")
player_surface.fill("White")
snail_surface.fill("Black")

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,900)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
       
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if player_rect.bottom <= 380:
                        player_gravity = -10
            
        else:
            if event.type ==  pygame.KEYDOWN:
                if event.key ==  pygame.K_RETURN:
                    game_active = True
                    player_gravity = 0
                    obstacle_rect_list=[]
                    start_time = int(pygame.time.get_ticks() / 1000)
                    player_rect = player_surface.get_rect(midbottom = (75,380))
        
        if game_active and event.type == obstacle_timer:

            choice  = randint(1,2)

            obstacle_dict = {

                    1: obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(810,990),380))),
                    2: obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(810,990), randint(100,280))))
            } 

            if choice == 1: obstacle_dict[1]
            else: obstacle_dict[choice]


    if game_active:
        keys = pygame.key.get_pressed() 
        
        if keys[pygame.K_d] :
            player_speed += 1
            player_rect.x += player_speed
            if player_speed >= 5:
                player_speed = 10

        elif keys[pygame.K_a] :
            player_speed += 1
            player_rect.x -= player_speed
            if player_speed >= 5:
                player_speed = 10

        elif keys[pygame.K_w]:
            if player_rect.bottom <= 380:
                player_gravity = -10

        else:
            while player_speed != 0:
                player_speed -=1
                if player_speed < 0:
                    player_speed = 0

    if game_active:
        screen.blit(sky_surface,(0,0))
        screen.blit(ground_surface,(0,380))

        player_gravity += 1
        player_rect.y += player_gravity
        
        if player_rect.bottom >= 380 : player_rect.bottom = 380
        if player_rect.right >= 720 : player_rect.right = 720
        if player_rect.left <= 0: player_rect.left = 0
        if player_rect.top <= 0: player_rect.top = 0

        screen.blit(player_surface,player_rect)
        
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        game_active = collisions(player_rect,obstacle_rect_list)

        score = display_score()
    
    else:

        screen.fill((94,129,162))
        
        end_font = pygame.font.Font("Fonts\TarrgetAcademyItalic-qzmx.otf",75)
        
        end_text = end_font.render(f'Game over!', True, "Black")
        end_text_rect = end_text.get_rect(center = (360,240))
        
        end_text_lower = text_font.render('Press enter to retry',True,'Black')
        end_text_lower_rect = end_text_lower.get_rect(center = (360,290))

        score_message = text_font.render(f'Your score: {score}',True,"Grey")
        score_message_rect = score_message.get_rect(center = (360,310))
        
        screen.blit(end_text,end_text_rect)
        screen.blit(end_text_lower,end_text_lower_rect)
        screen.blit(score_message,score_message_rect)
    
    pygame.display.update()
    clock.tick(60)