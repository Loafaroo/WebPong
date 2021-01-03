from flask import Flask, request
import numpy as np
import random

app = Flask(__name__)

MAX_V = 3
UP, DOWN = 0, 1
_velocity = [-3, 3]

width = 448
height = 256

player_width = 10
player_height = 40

ball_width = 10
ball_height = 10

player1_h_offset = 5
player2_h_offset = 5 + player_width

class Logicstate:
    def __init__(self):
        self.player1 = Player1(5, 5)
        self.player2 = Player2(width - player2_h_offset, height - player2_h_offset)
        self.ball = Ball()

        self.gameState = 'play'

        self.ball.serve()

    def update(self, W, S, up, down, enter):
        ls.player1.direction_listen(W, S)
        ls.player2.direction_listen(up, down)

        self.ball.listen(enter)

        self.player1.update_movement()
        self.player2.update_movement()
        self.ball.update(self.player1, self.player2)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.moving = None

    def update_movement(self):
        if self.moving != None:
            self.velocity = _velocity[self.moving]
        else:
            self.velocity = 0

        self.y = int(np.clip(self.y + self.velocity, 0, height - player_height))

    def direction_listen(self, up, down):
        if up == 1:
            self.moving = UP                            
            
        elif down == 1:
            self.moving = DOWN

        else:
            self.moving = None

class Player1(Player):
    def __init__(self, x, y):
        super().__init__(x, y)
        
class Player2(Player):
    def __init__(self, x, y):
        super().__init__(x, y)

class Ball(Player):
    def __init__(self):
        self.x, self.y = width // 2, height // 2
        self.width = ball_width
        self.height = ball_height

    def serve(self):
        self.velocity = [random.uniform(-4, 4), random.uniform(-1, 1)]

    def listen(self, enter):
        if enter == 1:
            self.__init__()
            self.serve()

    def update(self, player1, player2):
        if self.Y_Collision():
            self.velocity[1] = -self.velocity[1]

        if self.Player1_Collision(player1):
            self.velocity[0] = abs(self.velocity[0])
        if self.Player2_Collision(player2):
            self.velocity[0] = -abs(self.velocity[0])
            
        self.x = self.x + self.velocity[0]
        self.y = self.y + self.velocity[1]

    def Y_Collision(self):
        if self.y < 0 or self.y + self.height > height:
            return True
        else: return False

    def Player1_Collision(self, player1):
        if abs(self.x - (player1.x)) < player_width:
            if self.y -self.width > player1.y and self.y < player1.y + player_height:
                return True
    def Player2_Collision(self, player2):
        if abs((self.x)- (player2.x)) < player_width:
            if self.y -self.width > player2.y and self.y < player2.y + player_height:
                return True
            
ls = Logicstate()

@app.route("/update")
def update():
    W = request.args.get("W")
    S = request.args.get("S")
    up = request.args.get("up")
    down = request.args.get("down")
    enter = request.args.get("enter")

    ls.update(int(W), int(S), int(up), int(down), int(enter))

    key_params = {"player1_y" : ls.player1.y,
                  "player2_y" : ls.player2.y,
                  "ball_x" : ls.ball.x,
                  "ball_y" : ls.ball.y,
                  "gameState" : ls.gameState}

    return key_params
    
app.run()

