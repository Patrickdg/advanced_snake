# LIBRARIES 
import os
import pygame
import thorpy
import random
import math 

""" TO-DO 
Features:
o GUI: Menu, Score, Difficulty options, Color, background, Snake image, Game stats
o Music & selection :) 
o Difficulty features: 
    x bombs & levels
    x speed difficulty
    o progressive speed
    o colored food & required course order
    o colored food & map blindness (memorization)
    o food respawn timer
    x Teleport mechanics

Bugs:
o Spawn mechanics fix: food/bomb potential to spawn on/in front of snake 
o Food spawning off-map (random int rounding)
"""

# PARAMETERS
pygame.init()

WIN_W = 750
WIN_H = 750
SCREEN = pygame.display.set_mode([WIN_W, WIN_H])
pygame.display.set_caption("Snake")

SIZE_W = 25
SIZE_H = 25

SPEED_STAGES = {1: 200, 2: 150, 3: 100, 4: 75, 5: 40}

# SOUNDS 
MUSIC_TRACKS = []
for track in os.listdir('music'):
    MUSIC_TRACKS.append("music/" + track)

# OBJECTS
def round_nearest(n, nearest):
    return int(nearest * round(float(n)/nearest))

class Snake():
    def __init__(self, x, y, teleport):
        self.width = SIZE_W
        self.height = SIZE_H
        self.x = round_nearest(WIN_W/2, self.width)
        self.y = round_nearest(WIN_H/2, self.height)
        self.length = 1
        self.dir = 'down'
        self.tail = []
        self.teleport = teleport

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
        
        # Teleport 
        if self.teleport:
            if self.x == WIN_W:
                self.x = 0
            elif self.x < 0: 
                self.x = WIN_W
            elif self.y == WIN_H:
                self.y = 0
            elif self.y < 0: 
                self.y = WIN_H
    
    # move tail
    def move_tail(self):
        self.tail.insert(0, [self.x, self.y])
        self.tail.pop()

    def eat(self):
        self.length +=1
        self.tail.insert(-1, [self.x, self.y])

    def draw(self, screen):
            pygame.draw.rect(screen, (0,255,0), (self.x, self.y, self.width, self.height))
            if self.length > 1:
                self.move_tail()
            for tail in list(self.tail):
                pygame.draw.rect(screen, (0,255,0), (tail[0], tail[1], self.width, self.height))

class Food():
    def __init__(self):
        self.width = SIZE_W
        self.height = SIZE_H
        self.x = round_nearest(random.randint(0, WIN_W), self.width)
        self.y = round_nearest(random.randint(0, WIN_H), self.height)

    def spawn(self, screen, color):
        pygame.draw.rect(screen, color, (round_nearest(self.x, self.width),
                                             round_nearest(self.y, self.height), 
                                             self.width, self.height))

    def eaten(self):
        self.x = round_nearest(random.randint(0, WIN_W), self.width)
        self.y = round_nearest(random.randint(0, WIN_H), self.height)

        self.spawn(SCREEN, (0,0,255))
        print(self.x, self.y)
    
# MAIN LOOP #
def main():
    # GAME OPTIONS
    SPEED_DIFFICULTY = 3 #scale: 1 (Easy) to 5 (Impossible)
    TELEPORT_ON = True
    BOMBS_ON = True

    # Declarations
    snake = Snake(WIN_W/2, WIN_H/2, True if TELEPORT_ON else False)
    food = Food()
    bombs = []
    speed = SPEED_STAGES[SPEED_DIFFICULTY]
    # music_track = MUSIC_TRACKS[SPEED_DIFFICULTY-1]
    pygame.mixer.music.load(MUSIC_TRACKS[SPEED_DIFFICULTY-1])
    pygame.mixer.music.play(-1)

    running = True
    while running:
        SCREEN.fill((0,0,0))

        font = pygame.font.Font(None, 74)
        score = snake.length - 1
        score_disp = font.render(f"Score: {score}", 1, (255,255,255))

        pygame.time.delay(speed)
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
        
        # Draw score, snake, food, bombs
        # Check if food eaten
        SCREEN.blit(score_disp, (250,10))
        food.spawn(SCREEN, (0,0,255))
        if BOMBS_ON:
            for bomb in bombs:
                bomb.spawn(SCREEN, (255,0,0))
                if [bomb.x, bomb.y] == [snake.x, snake.y]:
                    running = False

        if [food.x, food.y] == [snake.x, snake.y]: 
            food.eaten()
            snake.eat()
            for level in range(0, score+1):
                bombs.append(Food())
        
        snake.draw(SCREEN)
        snake.move()
        
        # End scenarios - (1) Hit sides OR (2) hit self == pause snake, pause screen updates, display 'End' message,
        ## (1) Boundaries
        if not TELEPORT_ON:
            out_of_bounds = (snake.x < 0) or (snake.x > WIN_W) or (snake.y < 0) or (snake.y > WIN_H)
        else:
            out_of_bounds = False
        ## (2) Check if crashed into self
        if ([snake.x, snake.y] in snake.tail) or (out_of_bounds): 
            alive = False
        
        pygame.display.update()
    print(f"Great job! You got {score} points.")
    pygame.quit()

main()