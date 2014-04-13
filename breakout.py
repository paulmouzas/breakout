import pygame
from pygame import *
import random
import math

RED     = (255,0,0)
GREEN   = (0,255,0)
BLUE    = (0,0,255)
YELLOW  = (255,255,0)
PURPLE  = (255,0,255)

COLORS = (RED, GREEN, BLUE, YELLOW, PURPLE)

WIN_WIDTH = 480
WIN_HEIGHT = 320

BLOCK_WIDTH = 78
BLOCK_HEIGHT = 16

BALL_WIDTH = 10
BALL_HEIGHT = 10

DISPLAY = (WIN_WIDTH, WIN_HEIGHT)

class Scene(object):
    def __init__(self):
        pass

    def render(self, screen):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def handle_events(self, events):
        raise NotImplementedError
        
class GameScene(Scene):
    def __init__(self, level):
        self.all_sprites = pygame.sprite.Group()
        self.level = level
        
        # create the paddle
        self.paddle = Paddle()
        self.all_sprites.add(self.paddle)

        
        # create the blocks
        self.blocks = pygame.sprite.Group()
        top = 50
        for row in range(3):
            for col in range(6):
                block = Block(col*(BLOCK_WIDTH+2)+1,top)
                self.blocks.add(block)
                self.all_sprites.add(block)
            top += (BLOCK_HEIGHT + 2)
        
        # create the ball
        self.balls = pygame.sprite.GroupSingle()
        self.ball = Ball()
        self.ball.add(self.balls)
        self.all_sprites.add(self.ball)
        
    def render(self, screen):
        screen.fill((0, 0, 0))
        self.all_sprites.draw(screen)
        
    def update(self):
        pressed = pygame.key.get_pressed()
        left, right = [pressed[key] for key in (K_LEFT, K_RIGHT)]
        self.paddle.update(left, right)
        if self.ball.update():
            self.manager.go_to(GameOver())
        
        # block collision
        if pygame.sprite.spritecollide(self.ball, self.blocks, True):
            self.ball.bounce(0)
        if len(self.blocks) == 0:
            self.manager.go_to(Win())
        # paddle collision
        if pygame.sprite.spritecollide(self.paddle, self.balls, False):
            diff = (self.paddle.rect.x +BLOCK_WIDTH/2) - (self.ball.rect.x - 5)
            self.ball.rect.y = WIN_HEIGHT-31
            self.ball.bounce(diff)

    def handle_events(self, events):
        for e in events:
            if e.type == KEYDOWN and e.key == K_ESCAPE:
                self.manager.go_to(TitleScene())
        
class TitleScene(Scene):
    def __init__(self):
        self.font = pygame.font.SysFont('Arial', 56)
        self.sfont = pygame.font.SysFont('Arial', 32)

    def render(self, screen):
        screen.fill((0, 0, 0))
        text1 = self.font.render('Game', True, (255, 255, 255))
        text2 = self.sfont.render('> press space to start <', True, (255, 255, 255))
        screen.blit(text1, (50, 50))
        screen.blit(text2, (50, 120))

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == KEYDOWN and e.key == K_SPACE:
                self.manager.go_to(GameScene(0))

class GameOver(Scene):
    def __init__(self):
        self.font = pygame.font.SysFont('Arial', 56)
        self.sfont = pygame.font.SysFont('Arial', 32)
    def render(self, screen):
        screen.fill((0, 0, 0))
        text1 = self.font.render('You Lose', True, (255, 255, 255))
        text2 = self.sfont.render('> press space to play again <', True, (255, 255, 255))
        screen.blit(text1, (50, 50))
        screen.blit(text2, (50, 120))

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == KEYDOWN and e.key == K_SPACE:
                self.manager.go_to(GameScene(0))
                
class Win(Scene):
    def __init__(self):
        self.font = pygame.font.SysFont('Arial', 56)
        self.sfont = pygame.font.SysFont('Arial', 32)
    def render(self, screen):
        screen.fill((0, 0, 0))
        text1 = self.font.render('You Win! Play again?', True, (255, 255, 255))
        text2 = self.sfont.render('> press space to play again <', True, (255, 255, 255))
        screen.blit(text1, (40, 50))
        screen.blit(text2, (50, 120))

    def update(self):
        pass

    def handle_events(self, events):
        for e in events:
            if e.type == KEYDOWN and e.key == K_SPACE:
                self.manager.go_to(GameScene(0))
                
class SceneMananger(object):
    def __init__(self):
        self.go_to(TitleScene())

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self
#        __________________
# ______/ sprite classes   \_____________________
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        
        self.color = (255,255,255)
        self.width = 80
        self.height = 20
        
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.rect.x = WIN_WIDTH/2
        self.rect.y = WIN_HEIGHT-20
        
    def update(self, left, right):
        if left:
            self.rect.x -= 6
        elif right:
            self.rect.x += 6
        if self.rect.x > WIN_WIDTH-80:
            self.rect.x = WIN_WIDTH-80
        elif self.rect.x < 0:
            self.rect.x = 0
            
class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.color = random.choice(COLORS)
        self.width = BLOCK_WIDTH
        self.height = BLOCK_HEIGHT
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.image.fill(self.color)
        self.rect.x = x
        self.rect.y = y
            
class Ball(pygame.sprite.Sprite):
    
    speed = 6
    x = 0.0
    y = 180.0
    
    direction = 45
    
    width = 10
    height = 10
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
            
        self.image = pygame.Surface([self.width, self.height])
        self.rect = self.image.get_rect()
        self.image.fill((255,255,255))
        
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        
    def update(self):
        direction_radians = math.radians(self.direction)
        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y
            
        if self.y <= 0:
            self.bounce(0)
            self.y = 1
        # Do we bounce off the left of the screen?
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1
        # Do we bounce of the right side of the screen?
        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1
        # Did we fall off the bottom edge of the screen?
        if self.y > WIN_HEIGHT+20:
            return True
        else:
            return False
    def bounce(self, diff):
        self.direction = (180 - self.direction) % 360
        self.direction -= diff
#        _____________
# ______/ main loop   \_____________________
        
def main():
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption("Breakout!")
    timer = pygame.time.Clock()
    running = True

    manager = SceneMananger()

    while running:
        timer.tick(60)

        if pygame.event.get(QUIT):
            running = False
            return
        manager.scene.handle_events(pygame.event.get())
        manager.scene.update()
        manager.scene.render(screen)
        pygame.display.flip()
        
if __name__ == '__main__':
    main()
    pygame.quit()