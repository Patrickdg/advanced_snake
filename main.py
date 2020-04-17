# LIBRARIES 
import pygame
import random
import math 

 
""" TO-DO 
- death scenarios (2): edge boundaries + eat self
- GUI
- Score system & display

"""

# PARAMETERS
pygame.init()

WIN_W = 750
WIN_H = 750
SCREEN = pygame.display.set_mode([WIN_W, WIN_H])
pygame.display.set_caption("Snake")

# OBJECTS
def round_nearest(n, nearest):
    return int(nearest * round(float(n)/nearest))

class Snake():
    def __init__(self, x, y):
        self.width = 30
        self.height = 30
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
            if self.tail:
                self.move_tail()
            print(self.tail)
            for tail in list(self.tail):
                pygame.draw.rect(screen, (255,0,0), (tail[0], tail[1], self.width, self.height))

def round_nearest(n, nearest):
    return int(nearest * round(float(n)/nearest))

class Food():
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = round_nearest(random.randint(0, WIN_W), self.width)
        self.y = round_nearest(random.randint(0, WIN_H), self.height)
    
    def spawn(self, screen):
        pygame.draw.rect(screen, (0,255,0), (round_nearest(self.x, self.width),
                                             round_nearest(self.y, self.height), 
                                             self.width, self.height))

    def eaten(self):
        self.x = random.randint(0, WIN_W)
        self.y = random.randint(0, WIN_H)

        self.spawn(SCREEN)
    
# MAIN LOOP #
def main():
    snake = Snake(WIN_W/2, WIN_H/2)
    food = Food()
    threshold = 0.75*snake.width

    running = True
    while running:
        SCREEN.fill((0,0,0))

        # Check if food eaten
        if (abs(snake.x - food.x) < threshold) & (abs(snake.y - food.y) < threshold): 
            food.eaten()
            snake.eat()
            print(snake.tail)

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
        
        snake.draw(SCREEN)
        food.spawn(SCREEN)
        snake.move()

        # End scenarios - (1) Hit sides OR (2) hit self == pause snake, pause screen updates, display 'End' message,
        ## (1) Boundaries
        
        pygame.display.update()
    
    pygame.quit()

main()