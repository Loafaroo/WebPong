import sys, os
import pygame
from pygame.locals import *
import numpy as np
import math
from PIL import Image
import time
import random
import requests

size = width, height = 448, 256
black = 0, 0, 0
white = 255, 255, 255

background = 0, 140, 178

UP, DOWN = 0, 1

MAX_V = 3

_velocity = {DOWN: [0, MAX_V],
             UP: [0, -MAX_V]}

player_width = 10
player_height = 40

ball_width = 10
ball_height = 10

player1_h_offset = 5
player2_h_offset = 5 + player_width

class Player():
    def __init__(self, world_coordinate = [width // 2, height // 2], player_keys = [ord('w'), ord('s')]):
        self.X, self.Y = world_coordinate
        self.k_up, self.k_down = player_keys
        self.velocity = [0,0]
        self.moving = None
        self.width = player_width
        self.height = player_height
        
                
    def update_movement(self):
        self.accelerate()
        self.update_position()

    def accelerate(self):
        if self.moving != None:
            self.velocity = _velocity[self.moving]
        else:
            self.velocity = [0,0]

    def update_position(self):
       #TODO: add boundaries so dude doesn't go off the map
        self.Y = np.clip(self.Y + self.velocity[1], 0, height - player_height)

    def update_animation(self):
        pass
        
    def step_animation(self):        
        pass

    def detail_step_animation(self):        
        pass

    def direction_listen(self, keys):
        if keys[self.k_up]:
            self.moving = UP                            
            
        elif keys[self.k_down]:
            self.moving = DOWN

        else:
            self.moving = None

    def Draw(self, screen):
        new_rect = pygame.Rect(self.X, self.Y, player_width, player_height)
        pygame.draw.rect(screen, white, new_rect)

            
class Player1(Player):
    def __init__(self):
        self.world_coord = [5, 5]
        self.player_keys = [ord('w'), ord('s')]
        super().__init__(self.world_coord, self.player_keys)
        

class Player2(Player):
    
    def __init__(self):
        self.world_coord = [width - player_width - 5, height - player_height - 5]
        self.player_keys = [K_UP, K_DOWN]
        super().__init__(self.world_coord, self.player_keys)

class Ball(Player):
    def __init__(self):
        self.world_coord = [width // 2, height //2]
        self.X, self.Y = self.world_coord
        self.velocity = [0,0]
        self.width = 10
        self.height = 10

    def serve(self):
        self.velocity = [random.uniform(-4, 4), random.uniform(-1, 1)]

    def update(self, player1, player2):
        if self.Y_Collision():
            self.velocity[1] = -self.velocity[1]

        if self.Player1_Collision(player1):
            self.velocity[0] = abs(self.velocity[0])
        if self.Player2_Collision(player2):
            self.velocity[0] = -abs(self.velocity[0])
            
        self.X = self.X + self.velocity[0]
        self.Y = self.Y + self.velocity[1]
        
    def Draw(self, screen):
        new_rect = pygame.Rect(self.X, self.Y, self.width, self.height)
        pygame.draw.rect(screen, white, new_rect)

    def Y_Collision(self):
        if self.Y < 0 or self.Y + self.height > height:
            return True
        else: return False

    def Player1_Collision(self, player1):
        if abs(self.X - (player1.X + player1.width - 2)) < 2:
            if self.Y -self.width > player1.Y and self.Y < player1.Y + player2.height:
                return True
    def Player2_Collision(self, player2):
        if abs((self.X + self.width )- (player2.X + 2)) < 2:
            if self.Y -self.width > player2.Y and self.Y < player2.Y + player2.height:
                return True

    def listen(self, keys):
        if keys[K_RETURN]:
            self.__init__()
            self.serve()
        
        
class LogicState():
    #A state should have at least three methods: handle its own events, update the game world, and draw something different on the screen
    def __init__(self, Player1, Player2, Ball, screen):
        
        self.Player1 = Player1
        self.Player2 = Player2
        self.ball = Ball
        self.screen = screen

        self.gameState = 'play'

    """
    Main Loop
    """
    def event_listen(self):
       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:                
                quit()

        
    def update_logic_state(self):
        keys = pygame.key.get_pressed()

        keys_params = {'W':keys[ord('w')],
                       'S':keys[ord('s')],
                       'up':keys[K_UP],
                       'down':keys[K_DOWN],
                       'enter':keys[K_RETURN]}

        r = requests.get('http://127.0.0.1:5000/update', keys_params)

        self.Player1.Y = r.json()['player1_y']
        self.Player2.Y = r.json()['player2_y']
        self.ball.X = r.json()['ball_x']
        self.ball.Y = r.json()['ball_y']
        
    def Draw(self):        
        self.Player1.Draw(self.screen)
        self.Player2.Draw(self.screen)
        self.ball.Draw(self.screen)


def main():
    pass
if __name__ == "__main__":
    main()
