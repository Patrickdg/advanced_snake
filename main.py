import pygame
import random 

pygame.init()

WIN_W = 750
WIN_H = 750
SCREEN = pygame.display.set_mode([WIN_W, WIN_H])
pygame.display.set_caption("Snake")

# Objects
class Snake():
    def __init__(self, x, y):
        self.width = 30
        self.height = 30
        self.x = 50-0.5*self.width 
        self.y = 50-0.5*self.height
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
        if self.tail:
            self.tail.insert(0, [self.x, self.y])

    def eat(self):
        self.length +=1
        self.tail.insert(-1, [self.x, self.y])

    def draw(self, screen):
            pygame.draw.rect(screen, (255,0,0), (self.x, self.y, self.width, self.height))
            self.move_tail()
            print(self.tail)

class Food():
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = random.randint(0, WIN_W-0.5*self.width)
        self.y = random.randint(0, WIN_H-0.5*self.height)
    
    def spawn(self, screen):
        pygame.draw.rect(screen, (0,255,0), (self.x, self.y, self.width, self.height))

    def eaten(self):
        self.x = random.randint(0, WIN_W-0.5*self.width)
        self.y = random.randint(0, WIN_H-0.5*self.height)

        self.spawn(SCREEN)
    
# Main Loop
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