import pygame
import math

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)

block_width = 23
block_height = 15

class Block(pygame.sprite.Sprite):
    
    def __init__(self, color, x, y):
        
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((block_width, block_height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
class Ball(pygame.sprite.Sprite):
    
    speed = 5.0
    x = 0.0
    y = 180.0
    direction = 200
    width = 10 
    height = 10
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.screen_width = pygame.display.get_surface().get_width()
        self.screen_height = pygame.display.get_surface().get_height()
        
    def bounce(self, diff):
        
        self.direction = (180 - self.direction) % 360
        self.direction -= diff
        
    def update(self):
        direction_radians = math.radians(self.direction)
        
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
        
        self.rect.x = self.x
        self.rect.y = self.y
        
        if self.y <= 0:
            self.bounce(0)
            self.y = 1
            
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1
            
        if self.x > self.screen_width - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screen_width - self.width - 1
            
        if self.y > 600:
            return True
        else:
            return False
           
class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.width = 75
        self.height = 15
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(white)
        
        self.rect = self.image.get_rect()
        self.screen_height = pygame.display.get_surface().get_height()
        self.screen_width = pygame.display.get_surface().get_width()
        
        
        self.rect.x = 0 
        self.rect.y = self.screen_height - self.height
        
    def update(self):
        
        pos = pygame.mouse.get_pos()
        
        self.rect.x = pos[0] - (self.width/2)
        
        if self.rect.x > self.screen_width-self.width:
            self.rect.x = self.screen_width-self.width
            
pygame.init()

screen = pygame.display.set_mode((575, 350))



def quit(events):
    for event in events:
        if event.type == pygame.QUIT:
            return True
        else:
            return False

block_list = pygame.sprite.Group()
balls = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

# add the blocks
row_pos = 80
for row in range(4):
    for column in range(0,23):
        block = Block(blue, column*(block_width+2) + 1, row_pos)
        all_sprites_list.add(block)
        block_list.add(block)
    row_pos += block_height+2

# add the player
player = Player()
all_sprites_list.add(player)

# add the ball
ball = Ball()
all_sprites_list.add(ball)
balls.add(ball)

clock = pygame.time.Clock()


running = True
while running:
    
    events = pygame.event.get()
    if quit(events):
        break
        

    
    player.update()
    ball.update()
    
    if pygame.sprite.spritecollide(player, balls, False):
        diff = (player.rect.x + player.width/2) - (ball.rect.x+ball.width/2)
        ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
        ball.bounce(diff)
        
    dead_blocks = pygame.sprite.spritecollide(ball, block_list, True)
    if len(dead_blocks) > 0:
        ball.bounce(0)
        
    # DRAWING BELOW
    screen.fill(black)
    all_sprites_list.draw(screen)
    pygame.display.flip()
    
    clock.tick(50)
pygame.quit()
    
        