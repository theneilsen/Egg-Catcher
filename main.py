import pygame 
import os
import time
import random
pygame.font.init()

WIDTH,HEIGHT = 700,700

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Egg_Catcher")

EGG = pygame.image.load(os.path.join("imgs" , "egg3.png"))

PLAYER = pygame.image.load(os.path.join("imgs" , "line.png"))

BG = pygame.transform.scale(pygame.image.load(os.path.join("imgs" , "bg.png")) , (WIDTH,HEIGHT + 130))


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.player_img = PLAYER
        self.mask = pygame.mask.from_surface(self.player_img)

    def draw(self, window):
        window.blit(self.player_img, (self.x, self.y))

    def get_width(self): 
        return self.player_img.get_width()   
        
    def get_height(self): 
        return self.player_img.get_height() 


class Egg:
    def  __init__(self, x, y):
        self.x = x
        self.y = y
        self.egg_img = EGG
        self.mask = pygame.mask.from_surface(self.egg_img)

    def move(self, vel):
        self.y += vel      

    def draw(self, window):
        window.blit(self.egg_img, (self.x, self.y))      

    def get_width(self): 
        return self.egg_img.get_width()   
        
    def get_height(self): 
        return self.egg_img.get_height()     

    def off_screen(self,height):
        return not (self.y <= height and self.y >= 0) 

    def remove_egg(self, obj):
        for egg in self.eggs:
            if egg.collision(obj):
                self.eggs.remove(egg)

def collide(obj1 , obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y

    return obj1.mask.overlap(obj2.mask, (offset_x , offset_y)) != None


def main():
    run = True
    lost = False
    lost_count = 0
    FPS=  60
    clock = pygame.time.Clock()

    main_font = pygame.font.SysFont("Arial", 30) 
    lost_font = pygame.font.SysFont("Arial", 40) 

    eggs = []
    wave_length = 5
    egg_vel = 3
    lives=3
    level=0
    eggs_collected=0

    player = Player(300, 500)

    player_vel = 5

    def redraw_window():
        WIN.blit(BG , (0,0)) 

        lives_label = main_font.render(f"Lives: {lives}" , 1 , (17,42,66))
        level_label = main_font.render(f"Level: {level}" , 1 , (17,42,66))
        eggs_label = main_font.render(f"Eggs: {eggs_collected}" , 1 , (17,42,66))

        WIN.blit(lives_label , (10,150))
        WIN.blit(eggs_label , (10,200))
        WIN.blit(level_label , (WIDTH - level_label.get_width() - 10,150))

        for egg in eggs:  #draws every egg on the screen
            egg.draw(WIN)

        player.draw(WIN)

        if lost:
                lost_label = lost_font.render("YOU LOST", 1 , (17,42,66))
                WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2 , 300))  

        pygame.display.update()
        
    while run:
        clock.tick(FPS)
        redraw_window()   

        if lives <= 0 :
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS*1:  #1 sec(s)
                run = False
            else:
                continue    

        if len(eggs) == 0:  #after each level
            level += 1
            wave_length += 5
            for i in range(wave_length):
                egg = Egg(random.randrange(50 , WIDTH-100) , random.randrange(-1500 , -100)) 
                eggs.append(egg)
                
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  
                run = False

        keys = pygame.key.get_pressed() 
        if keys[pygame.K_a] and player.x - player_vel > 0:  #atleast 4.1 - 4 = 0.1
            player.x -= player_vel 
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH :  
            player.x += player_vel   
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel   
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() < HEIGHT :
            player.y += player_vel     

        for egg in eggs[:]:
            egg.move(egg_vel)

            if collide(player, egg):
                eggs.remove(egg) 
                eggs_collected +=1 

            if egg.y + egg.get_height() > HEIGHT:
                lives -= 1
                eggs.remove(egg)  


main()            
