# Squareventures

# Controls
# Left click to jump, Right click to shoot
# Press escape at any point to return to intro screen

# Gameplay
# Objective of the game is to get the highest score
# A scorepoint is given for each obstacle you overcome
# Player can shoot the orange and blue monsters
# Player can jump over the spikes and orange monsters
# For every 10 scorepoints gained, the number of bullets is incremented by 2
# The speed of the player increases for every 20 scorepoints earned
# The game is over when the player collides with the obstacle

import pygame,sys,time,math
from random import randint,choice

def Squareventures():
    
    SCREEN_WIDTH =  1280
    SCREEN_HEIGHT = 720
    #Initial pygame and screen setup
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(( SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.display.set_caption('SQUAREVENTURES')

    #Importing background image and sound assets
    background = pygame.image.load('gameit/static/ARJ18/background.jpg').convert_alpha()
    background = pygame.transform.scale(background, ( SCREEN_WIDTH,SCREEN_HEIGHT))
    pygame.mixer.init(48000, -16, 4, 4096)

    jump_sound = pygame.mixer.Sound('gameit/static/ARJ18/jump')
    shoot_sound = pygame.mixer.Sound('gameit/static/ARJ18/shoot')
    kill_sound = pygame.mixer.Sound('gameit/static/ARJ18/kill')
    increment_sound = pygame.mixer.Sound('gameit/static/ARJ18/increment')
    nobullet_sound = pygame.mixer.Sound('gameit/static/ARJ18/nobullet')

    gamemusic = pygame.mixer.Sound('gameit/static/ARJ18/gamemusic.mp3')
    gamemusic.set_volume(0.4)
    intromusic = pygame.mixer.Sound('gameit/static/ARJ18/intromusic.mp3')
    intromusic.set_volume(0.5)
    tiles = math.ceil( SCREEN_WIDTH / background.get_width())+1

    #Importing the font
    game_font = pygame.font.Font('gameit/static/ARJ18/gomarice_no_continue.ttf', 50)

    #Class that manages the game state
    class Gamestate():
        def __init__(self):
            self.state = 'intro'
            intromusic.play(loops=-1)
        #For intro screen
        def intro(self):
            #Defining the images and text
            play_title_surf = game_font.render('SQUAREVENTURES', 0, (43,20,158))
            play_title_surf = pygame.transform.rotozoom(play_title_surf, 0, 2)
            play_surf = game_font.render('PLAY', 0, (43,20,158))
            play_surf = pygame.transform.rotozoom(play_surf, 0, 1.25)
            play_button = pygame.image.load('gameit/static/ARJ18/playbutton.png')
            play_button = pygame.transform.scale(play_button, (100,100))
            play_rect = play_button.get_rect(center = (640,400))
            play_text = game_font.render('Left Click to jump, Right Click to Shoot!', 0, (43,20,158))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #Checking if the play button is pressed
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if play_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                        self.state = 'main'
                        intromusic.stop()
                        gamemusic.play(loops=-1)
            #Displaying and updating the intro screen
            screen.blit(background, (0,0))
            screen.blit(play_surf, (580,250))
            screen.blit(play_title_surf, (300,100))
            screen.blit(play_button,play_rect)
            screen.blit(play_text,(220,500) )
            pygame.display.flip()
        #For the main game    
        def main_game(self):
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #Generating the obstacles based on a timer
                if event.type == obstacle_timer:
                    obstacle_group.add(Obstacle(choice(['spike','spike','mon1','mon1','mon2'])))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    player.player_input()
                #Returning to the intro screen when escape key is pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        scroll_and_update.reset()
                        self.state = 'intro'
                        gamemusic.stop()
                        intromusic.play(loops=-1)
            
            #Drawing and Updating the player and obstacle groups
            scroll_and_update.scroll_set()
            obstacle_group.draw(screen)
            obstacle_group.update()
            
            bullet_group.draw(screen)
            bullet_group.update()
            
            player_group.draw(screen)
            player_group.update()
            #Displaying the score and bullet count
            score.score_display()
            bullet_set.bullet_display()
            #Updating the screen every frame
            pygame.display.flip()
        
        #For the game over screen
        def game_over(self):
            #Defining the text
            text_surf = game_font.render('GAME OVER!', 0, (43,20,158)).convert_alpha()
            text_surf = pygame.transform.rotozoom(text_surf, 0, 2)
            retry_text_surf = game_font.render('RETRY?', 0, (43,20,158))
            retry_text_surf = pygame.transform.rotozoom(retry_text_surf, 0, 1.25)
            retry_rect = retry_text_surf.get_rect(topleft = (545,400))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                #Checking whether the retry button is clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                   if retry_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                        scroll_and_update.reset()
                        self.state = 'main'
                        gamemusic.stop()
                        gamemusic.play(loops=-1)
                #Returning to the intro screen when escape key is pressed
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        scroll_and_update.reset()
                        self.state = 'intro'
                        gamemusic.stop()
                        intromusic.play(loops=-1)
            
            #Displaying and updating the game over screen
            screen.blit(background, (0,0))
            score.score_display()
            screen.blit(retry_text_surf,retry_rect )
            screen.blit(text_surf,(410,200))
            pygame.display.flip()

        #Function to manage the current state of the game
        def state_manage(self): 
            if self.state == 'main':
                self.main_game()
            if self.state =='intro':
                self.intro()
            if self.state =='gameover':
                self.game_over()
            

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load('gameit/static/ARJ18/player.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (50,50))
            self.rect = self.image.get_rect(bottomleft = (100,550))        
            self.gravity = 0
        #Applies gravity every frame
        def apply_gravity(self):
            self.gravity +=0.9
            self.rect.y += self.gravity
            if self.rect.y >=550:
                self.rect.y = 550
        #Makes the player jump
        def jump(self):
            jump_sound.play()
            self.gravity = -20.75
        #Creates a new bullet
        def create_bullet(self):
            shoot_sound.play()
            return Bullet(self.rect.centerx,self.rect.centery) 

        #Gets player input, checks whether it is mouse right or left and calls the appropriate function 
        def player_input(self):
            if pygame.mouse.get_pressed()[2] and player.rect.bottom>=550:
                #Adding the bullet to bullet group and incrementing bullet count
                if bullet_set.bullet_count>0:
                    bullet_group.add(player.create_bullet())
                    bullet_set.bullet_update(0)
                else:
                    nobullet_sound.play()
                
            if pygame.mouse.get_pressed()[0] and player.rect.bottom>=550:
                player.jump()
        def update(self):
            self.apply_gravity()
            
    class  Obstacle(pygame.sprite.Sprite):
        def __init__(self,type):
            super().__init__()
            self.type = type
            #Loading the image of obstacle based on its type
            if type == 'spike':
                self.image = pygame.image.load('gameit/static/ARJ18/spikes.png').convert_alpha()
                self.image = pygame.transform.rotozoom(self.image,0,0.12)
            elif type == 'mon1':
                self.image = pygame.image.load('gameit/static/ARJ18/mon1.png').convert_alpha()
                self.image = pygame.transform.rotozoom(self.image,0,0.25)
            else:
                self.image = pygame.image.load('gameit/static/ARJ18/mon2.png').convert_alpha()
                self.image = pygame.transform.rotozoom(self.image,0,0.38)
            #Creating the obstacle
            self.rect = self.image.get_rect(bottomleft = (randint(1280+self.image.get_width(),1330+self.image.get_width()),600))
        
        #Destroys the obstacle if it goes out of the screen  
        def destroy(self):
            if self.rect.right <=0:
                self.kill()
                score.score_update()
        
        def update(self):
            self.rect.x -=scroll_and_update.obstacle_speed
            self.destroy()
        
    class Bullet(pygame.sprite.Sprite):
        def __init__(self,x,y):
            super().__init__()
            #Loading the bullet image
            self.image = pygame.image.load('gameit/static/ARJ18/bullet.png')  
            self.image = pygame.transform.rotozoom(self.image, 0, 0.1)      
            self.rect = self.image.get_rect(center = (x,y))
        #Moving the bullet to the right
        def update(self):
            self.rect.x+=7
        #Destroys the bullet if it goes out of screen
        def destroy_bullet(self):
            if self.rect.right>= SCREEN_WIDTH:
                self.kill()
    
    class Score():
        def __init__(self):
            self.score =0

        #Updates the score
        def score_update(self):
            self.score +=1
            #Checking whether the score is a multiple of 10 or 20 to update the bullet count or player speed
            if (self.score%10)==0:
                increment_sound.play()
                bullet_set.bullet_update(1)
            if (self.score%20)==0:
                scroll_and_update.update_speed()
        #Displays the score
        def score_display(self):
            score_surf = game_font.render(f'Score : {self.score}', 0, (43,20,158))
            score_rect = score_surf.get_rect(center = (640,100))
            screen.blit(score_surf,score_rect)
        #Sets the score back to 0
        def reset(self):
            self.score = 0

    class Bullet_Set():
        def __init__(self):
            self.bullet_count = 10
        #Increments the bullet count by 2 or decrements it by 1 depending on the value parameter
        def bullet_update(self,value):
            if value:
                self.bullet_count+=2
            else:
                self.bullet_count-=1
        #Displays the number of bullets remaining
        def bullet_display(self):
            bullet_surf = game_font.render(f'Bullets : {self.bullet_count}', 0, (43,20,158))
            bullet_surf = pygame.transform.rotozoom(bullet_surf, 0, 0.75)
            bullet_rect = bullet_surf.get_rect(center = (200,100))
            screen.blit(bullet_surf,bullet_rect)
        #Sets the bullet count back to initial
        def reset(self):
            self.bullet_count = 10
    
    class Scroll_and_Update():
        def __init__(self):
            self.scroll_speed =5
            self.obstacle_speed = 5
            self.scroll =0
        #Creates the background scrolling effect
        def scroll_set(self):
            for i in range(0,tiles):
                screen.blit(background, (i*background.get_width()+self.scroll,0))
            self.scroll -= self.scroll_speed
            if abs(self.scroll) > background.get_width():
                self.scroll = 0
        #Increments the background and obstacle speeds to give the effect of increasing the player speed
        def update_speed(self):
            self.scroll_speed +=1
            self.obstacle_speed +=1
            
        #Sets the speeds back to initial speeds
        def reset(self):
            self.scroll_speed =self.obstacle_speed = 5
            obstacle_group.empty()
            bullet_group.empty()
            score.reset()
            bullet_set.reset()
    #Checks whether the player collides with any of the obstacles
    def collision():
        if pygame.sprite.spritecollide(player,obstacle_group,False):
            kill_sound.play()
            gamestate.state = 'gameover'
            obstacle_group.empty()
    #Checks whether the bullet collides with the monster type obstacles
    def enemy_collision():
        for bullet in bullet_group:
            obstacle_list = pygame.sprite.spritecollide(bullet, obstacle_group, False)
            for obstacle in obstacle_list:
                if obstacle.type != 'spike' and obstacle.rect.right<= SCREEN_WIDTH:
                    kill_sound.play()
                    obstacle.kill()
                    bullet.kill()
                    score.score_update()
    
    #Creating the player and obstacle sprite groups
    player_group = pygame.sprite.Group()
    player = Player()
    player_group.add(player)
    obstacle_group = pygame.sprite.Group()
    #Setting the obstacle timer
    obstacle_timer = pygame.USEREVENT+1
    pygame.time.set_timer(obstacle_timer, 1100)
    bullet_group = pygame.sprite.Group()
    #Creating the remaining class objects
    score = Score()
    bullet_set = Bullet_Set()
    scroll_and_update = Scroll_and_Update()
    gamestate = Gamestate()

    #Game Loop
    while True:
        #Managing the states
        gamestate.state_manage()
        #Checking for collisions
        enemy_collision()
        collision()
        
        clock.tick(120)
