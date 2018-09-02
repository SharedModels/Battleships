import numpy as np
import matplotlib.pyplot as mp

class Player:
    def __init__(self, Posns, Orientations):
        # creates a game board with poisitons and orientations of game pieces
        # order goes: Carrier(5), Battleship(4), Cruiser(3), Submarine(3), Destroyer(2)
        # 0 is horizontal, 1 is vertical, position taken from Top/left
        self.shipBoard = np.zeros((10,10))
        self.bombBoard = np.zeros((10,10))
        ### Populating board with ships ###
        
    def populate(self, posns, orientations):
        # Carrier
        if orientations[0] == 0:
            self.shipBoard[posns[0][0]:posns[0][0]+5,posns[0][1]] = 1
        else:
            self.shipBoard[posns[0][0],posns[0][1]:posns[0][1]:posns[0][1]+5] = 1
        # BattleShip
        if orientations[1] == 0:
            self.shipBoard[posns[1][0]:posns[1][0]+4,posns[1][1]] = 1
        else:
            self.shipBoard[posns[1][0],posns[0][1]:posns[1][1]:posns[1][1]+4] = 1
        # Cruiser
        if orientations[2] == 0:
            self.shipBoard[posns[2][0]:posns[1][0]+3,posns[2][1]] = 1
        else:
            self.shipBoard[posns[2][0],posns[2][1]:posns[2][1]:posns[2][1]+3] = 1
        # Submarine
        if orientations[3] == 0:
            self.shipBoard[posns[3][0]:posns[3][0]+3,posns[3][1]] = 1
        else:
            self.shipBoard[posns[3][0],posns[3][1]:posns[3][1]:posns[3][1]+3] = 1
        # Destroyer
        if orientations[4] == 0:
            self.shipBoard[posns[4][0]:posns[4][0]+2,posns[4][1]] = 1
        else:
            self.shipBoard[posns[4][0],posns[4][1]:posns[4][1]:posns[4][1]+2] = 1
    def recieveAttack(self, x,y):
        # player recieves an attack from other player at position X
        self.board[x,y] = 2
    def sendAttack(self, player, x, y):
        if player.shipBoard[x,y] == 0:
            # Miss
            self.bomBoard[x,y] = 1
        if player.shipBoard[x,y] == 1:
            # Hit
            self.bombBoard[x,y] = 2
    def ViewBoard(self):
        mp.imshow(self.board,cmap = "hot")
    def 