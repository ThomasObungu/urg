import pygame
import sys
import random

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((60, 60))
        self.image.fill(pygame.Color("White"))
        self.rect = self.image.get_rect(midbottom=(75, 380))
        self.gravity = 0
        self.speed = 0

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity

    def movement(self):
        keys = pygame.key.get_pressed() 
        
        #Moving left to right

        if keys[pygame.K_d] :
            self.speed += 0.5
            self.rect.x += self.speed
            if self.speed >= 10:
                self.speed = 10

        elif keys[pygame.K_a] :
            self.speed += 0.5
            self.rect.x -= self.speed
            if self.speed >= 10:
                self.speed = 10
 
        else:
            while self.speed != 0:
                self.speed -= 1
                if self.speed < 0:
                    self.rect.x += self.speed
                    self.speed = 0

        #Previous jumping mechanism
        '''
        elif keys[pygame.K_w]:
            if self.rect.bottom == 380:
                self.gravity = -20
        '''
        #Stopping movement
        
    def world_boundaries(self):

        #Screen borders

        if self.rect.right >= 720:
            self.rect.right = 720
        
        if self.rect.left <= 0:
            self.rect.left = 0

        if self.rect.top <= 0: 
            self.rect.top = 0

        if self.rect.bottom >= 380:
            self.rect.bottom = 380

    def update(self):
        self.movement()
        self.apply_gravity()
        self.world_boundaries()

horizontal_increment = 10 #Controls the speed at which ground obstacles move from right to left -- These are the defualts
verticle_increment = 5 # Controls the speed at which the obstacle moves downwards  -- These are the defualts

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, obstacle_type):
        super().__init__()
        if obstacle_type == "snail":
            self.image = pygame.Surface((50, 50))
            self.rect = self.image.get_rect(midbottom=(random.randint(810, 990), 380))
        
        elif obstacle_type == "fly":
            self.image = pygame.Surface((50, 100))
            self.rect = self.image.get_rect(midbottom=(random.randint(810, 990), 280))

        elif obstacle_type == "plank":
            self.image = pygame.Surface((200,50))
            self.rect = self.image.get_rect(topleft=(random.randint(810, 990), 330))
        
        self.image.fill(pygame.Color("Black"))

    def update(self):
        
        self.rect.x -= horizontal_increment
        
class FlyingObstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((300, 50))
        self.image.fill(pygame.Color("Black"))  
        self.rect = self.image.get_rect(topleft=(random.choice([0,420]), -75))
    
    def update(self):
        self.rect.y += verticle_increment

class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((720, 100))
        self.image.fill(pygame.Color("Black"))
        self.rect = self.image.get_rect(bottom=480)

def main():
    
    #Function to display score

    def display_score():

        text_font = pygame.font.Font("Fonts\TarrgetAcademyItalic-qzmx.otf",25)

        current_time = int(pygame.time.get_ticks() / 1000) - start_time

        score_surface = text_font.render(f'Score : {current_time}', True, "Black")
        score_rect = score_surface.get_rect(center = (360,75))
        
        pygame.draw.rect(screen,'White',score_rect,1,5)
        screen.blit(score_surface,score_rect)
        return current_time
    
    def increase_obstacle_increment():
        global horizontal_increment
        global verticle_increment
        
        horizontal_increment += 2
        verticle_increment += 1

    def reset_obstacle_increment():
        global horizontal_increment
        global verticle_increment
        
        horizontal_increment = 10
        verticle_increment = 5

    def game_over():
            
        font = pygame.font.Font("Fonts\TarrgetAcademyItalic-qzmx.otf", 25)
        end_font = pygame.font.Font("Fonts\TarrgetAcademyItalic-qzmx.otf", 75)

        end_text = end_font.render(f'Game over!', True, pygame.Color("Black"))
        end_text_rect = end_text.get_rect(center=(360, 240))
        end_text_lower = font.render('Press enter to retry', True, pygame.Color("Black"))
        end_text_lower_rect = end_text_lower.get_rect(center=(360, 290))

        score_message = font.render(f'Your score: {score}', True, pygame.Color("Grey"))
        score_message_rect = score_message.get_rect(center=(360, 310))
        
        screen.fill((94, 129, 162))
        
        screen.blit(end_text, end_text_rect)
        screen.blit(end_text_lower, end_text_lower_rect)
        screen.blit(score_message, score_message_rect)

    
    #Initializing screen
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((720, 480))
    pygame.display.set_caption("Untitled Runner Game")

    #Initilizing player, obstacle spawns and ground
    player = Player()
    obstacles = pygame.sprite.Group()
    ground = Ground()
    
    #Starting game
    game_active = True

    #Initilizing obstacle spawn
    obstacle_timer = pygame.USEREVENT + 1
    pygame.time.set_timer(obstacle_timer, 900)
    
    #Initilizing flying obstacle spawn
    flying_obstacle_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(flying_obstacle_timer, 15000)

    speed_increase_timer = pygame.USEREVENT + 3
    pygame.time.set_timer(speed_increase_timer, 10000)

    #Initilzing Score Varibles
    start_time = 0
    score = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            #Seperate jumping mechanisim to allow movement whilst in air
            if game_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        if player.rect.bottom == 380:
                            player.gravity = -20

            #New mechanism to allow a 'stomping' motion
            if game_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        if player.rect.bottom <= 380:
                            player.gravity = 20
            
            #Restart on game over screen
            if game_active == False:  
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    player.gravity = 0
                    reset_obstacle_increment()
                    obstacles.empty()
                    start_time = int(pygame.time.get_ticks() / 1000)
                    player.rect = player.image.get_rect(midbottom=(75, 380))
                    game_active = True

            #Allows obstacales being randomly generated
            if game_active and event.type == obstacle_timer:
                obstacle_choice = random.randint(1,3)

                obstacle_choices = {
                    1:"snail",
                    2:"fly",
                    3:"plank"
                }

                obstacle_type = obstacle_choices[obstacle_choice]

                obstacles.add(Obstacle(obstacle_type))

            #Allows flying obstacles to be randomly generated
            if game_active and event.type == flying_obstacle_timer:
                obstacles.add(FlyingObstacle()) 

            #Gradually speeding up the game
            if game_active and event.type == speed_increase_timer:
               print("Speeding up!")
               increase_obstacle_increment()

        if game_active:
            player.update()
            obstacles.update()

            obstacles = pygame.sprite.Group([obstacle for obstacle in obstacles if obstacle.rect.x > -200 and obstacle.rect.y < 420])
            
            if pygame.sprite.spritecollide(player, obstacles, False, collided=pygame.sprite.collide_rect):
                game_active = False

            screen.fill(pygame.Color("Grey"))
            
            screen.blit(player.image, player.rect)

            score = display_score()
    
            obstacles.draw(screen)

            screen.blit(ground.image, ground.rect)

        else:
            game_over()
        
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
