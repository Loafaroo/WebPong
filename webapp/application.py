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

        self.gameState = 'wait to join'

    def update(self, W, S, up, down, enter):
        if not self.player1.ai:
            self.player1.direction_listen(W, S)
        if not self.player2.ai:
            self.player2.direction_listen(up, down)
        else:
            if self.ball.x > width / 4 and self.ball.velocity[0] > 0:
                self.player2.direction_ai(self.ball.y)
            else:
                self.player2.moving = None
                
        if self.gameState == 'play':
            self.ball.listen(enter)
        if self.player1.assigned:
            self.player1.update_movement()
        if self.player2.assigned:
            self.player2.update_movement()
        self.ball.update(self.player1, self.player2)

    def assign_players(self):
        if not self.player1.assigned:
            self.player1.assigned = True
        if self.player1.assigned and not self.player2.assigned:
            self.player2.assigned = True
            self.player2.ai = True

    def game_ready(self):
        if self.player1.assigned and self.player2.assigned:
            self.gameState = 'play'

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.moving = None

        self.assigned = False
        self.ai = False

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

    def direction_ai(self, ball_y):
        if self.y + player_height *1/4 < ball_y:
            self.moving = DOWN
        elif self.y + player_height * 3/4 >= ball_y:
            self.moving = UP
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
        self.velocity = [0,0]

    def serve(self):
        self.velocity = [random.choice([-4, 4]), random.uniform(-1, 1)]

    def listen(self, enter):
        if enter == 1:
            self.__init__()
            self.serve()

    def update(self, player1, player2):
        if self.Y_Collision():
            self.velocity[1] = -self.velocity[1]

        if self.Player1_Collision(player1):
            self.velocity[0] = abs(self.velocity[0])
            self.velocity[1] += player1.velocity /5
        if self.Player2_Collision(player2):
            self.velocity[0] = -abs(self.velocity[0])
            self.velocity[1] += player2.velocity /5
            
        self.x = self.x + self.velocity[0]
        self.y = self.y + self.velocity[1]

    def Y_Collision(self):
        if self.y < 0 or self.y + self.height > height:
            return True
        else: return False

    def Player1_Collision(self, player1):
        if abs(self.x - (player1.x)) < player_width:
            if self.y + self.width > player1.y and self.y < player1.y + player_height:
                return True
    def Player2_Collision(self, player2):
        if abs((self.x)- (player2.x)) < player_width:
            if self.y + self.width > player2.y and self.y < player2.y + player_height:
                return True
            
ls = Logicstate()



@app.route("/joinserver")
def join():
    if not ls.player1.assigned and not ls.player2.assigned:
        ls.__init__()
    
    ls.assign_players()

    ls.game_ready()    

    

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

