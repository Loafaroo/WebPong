
import sys, os
import pygame
from pygame.locals import *
import numpy as np
import math
from PIL import Image
from LogicState import size, black, white, background, width, height, Player1, Player2, Ball, LogicState
import requests

screen = pygame.display.set_mode(size)
"""
set display mode (with openGL rendering, if desired)
"""
clock = pygame.time.Clock()
framerate = 60
"""
set framerate below with clock.tick
"""
        
            
def main():
    pygame.init()
    
    Paddle1 = Player1()
    Paddle2 = Player2()
    ball = Ball()

    requests.get('http://127.0.0.1:5000/joinserver')
        
    State = LogicState(Paddle1, Paddle2, ball, screen) # the darkness on the face of the deep
    
    while True:

        screen.fill(background)
        
        State.event_listen()

        State.update_logic_state()
        
        State.Draw()
                
        pygame.display.flip()
        
        clock.tick(framerate)
        
if __name__ == "__main__":
    main()
