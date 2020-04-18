# LIBRARIES 
import pygame
import thorpy
import random
import math 

""" TO-DO 
- GUI

"""

# PARAMETERS
pygame.init()

WIN_W = 750
WIN_H = 750
SCREEN = pygame.display.set_mode([WIN_W, WIN_H])
pygame.display.set_caption("Snake")

SIZE_W = 25
SIZE_H = 25

# OBJECTS
def round_nearest(n, nearest):
    return int(nearest * round(float(n)/nearest))

class Snake():
    def __init__(self, x, y):
        self.width = SIZE_W
        self.height = SIZE_H
        self.x = round_nearest(WIN_W/2, self.width)
        self.y = round_nearest(WIN_H/2, self.height)
        self.length = 1
        self.dir = 'down'
        self.tail = []

    # move head
    def move(self):
        if self.dir == 'left':
            self.x += -self.width
        elif self.dir == 'right':
            self.x += self.width
        elif self.dir == 'up':
            self.y += -self.height
        elif self.dir == 'down':
            self.y += self.height
    
    # move tail
    def move_tail(self):
        self.tail.insert(0, [self.x, self.y])
        self.tail.pop()

    def eat(self):
        self.length +=1
        self.tail.insert(-1, [self.x, self.y])

    def draw(self, screen):
            pygame.draw.rect(screen, (255,0,0), (self.x, self.y, self.width, self.height))
            if self.length > 1:
                self.move_tail()
            print(self.tail)
            for tail in list(self.tail):
                pygame.draw.rect(screen, (255,0,0), (tail[0], tail[1], self.width, self.height))

class Food():
    def __init__(self):
        self.width = SIZE_W
        self.height = SIZE_H
        self.x = round_nearest(random.randint(0, WIN_W), self.width)
        self.y = round_nearest(random.randint(0, WIN_H), self.height)
    
    def spawn(self, screen):
        pygame.draw.rect(screen, (0,255,0), (round_nearest(self.x, self.width),
                                             round_nearest(self.y, self.height), 
                                             self.width, self.height))

    def eaten(self):
        self.x = round_nearest(random.randint(0, WIN_W), self.width)
        self.y = round_nearest(random.randint(0, WIN_H), self.height)

        self.spawn(SCREEN)
    
# MAIN LOOP #
def main():
    # Declarations
    snake = Snake(WIN_W/2, WIN_H/2)
    food = Food()

    running = True
    alive = True
    while running:
        SCREEN.fill((0,0,0))

        font = pygame.font.Font(None, 74)
        score = font.render(f"Score: {snake.length-1}", 1, (255,255,255))

        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Key input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake.dir != 'right':
                    snake.dir = 'left'
                elif event.key == pygame.K_RIGHT and snake.dir != 'left':
                    snake.dir = 'right'
                elif event.key == pygame.K_DOWN and snake.dir != 'up':
                    snake.dir = 'down'
                elif event.key == pygame.K_UP and snake.dir != 'down':
                    snake.dir = 'up'
        
        # Draw score, snake & food
        if alive: 
            # Check if food eaten
            SCREEN.blit(score, (250,10))
            food.spawn(SCREEN)
            if [food.x, food.y] == [snake.x, snake.y]: 
                food.eaten()
                snake.eat()
                print(snake.tail)
            snake.draw(SCREEN)
            snake.move()
        else: 
            SCREEN.blit(score, (250,10))
            snake.draw(SCREEN)
            
        # End scenarios - (1) Hit sides OR (2) hit self == pause snake, pause screen updates, display 'End' message,
        ## (1) Boundaries
        out_of_bounds = (snake.x < 0) or (snake.x > WIN_W) or (snake.y < 0) or (snake.y > WIN_H)
        ## (2) Check if crashed into self
        if ([snake.x, snake.y] in snake.tail) or (out_of_bounds): 
            alive = False
        
        pygame.display.update()
    
    pygame.quit()

main()