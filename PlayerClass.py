import numpy as np
import matplotlib.pyplot as mp
from matplotlib.colors import LinearSegmentedColormap

# Setting Custom Colormap  for visualisation #
colors = [(1,1,1),(0,0,0),(1,0,0)] 
#  White(miss) -> Black(empty) ->Red(hit)  
cmap_name = 'Battleships'
n_bin = 3
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)

class Player:
    def __init__(self, Posns, Orientations):
        # creates a game board with poisitons and orientations of game pieces
        # order goes: Carrier(5), Battleship(4), Cruiser(3), Submarine(3), Destroyer(2)
        # 0 is horizontal, 1 is vertical, position taken from Top/left
        
        self.shipBoard = np.zeros((10,10)) # board containing positions of this players ships
        self.bombBoard = np.zeros((10,10)) # board containing bomb placement and hit or miss history
                                    
        ### Populating board with ships ###
        # Carrier
        if Orientations[0] == 0:
            self.shipBoard[Posns[0][0]:Posns[0][0]+5,Posns[0][1]] = 1
        else:
            self.shipBoard[Posns[0][0],Posns[0][1]:Posns[0][1]:Posns[0][1]+5] = 1
        # BattleShip
        if Orientations[1] == 0:
            self.shipBoard[Posns[1][0]:Posns[1][0]+4,Posns[1][1]] = 1
        else:
            self.shipBoard[Posns[1][0],Posns[0][1]:Posns[1][1]:Posns[1][1]+4] = 1
        # Cruiser
        if Orientations[2] == 0:
            self.shipBoard[Posns[2][0]:Posns[1][0]+3,Posns[2][1]] = 1
        else:
            self.shipBoard[Posns[2][0],Posns[2][1]:Posns[2][1]:Posns[2][1]+3] = 1
        # Submarine
        if Orientations[3] == 0:
            self.shipBoard[Posns[3][0]:Posns[3][0]+3,Posns[3][1]] = 1
        else:
            self.shipBoard[Posns[3][0],Posns[3][1]:Posns[3][1]:Posns[3][1]+3] = 1
        # Destroyer
        if Orientations[4] == 0:
            self.shipBoard[Posns[4][0]:Posns[4][0]+2,Posns[4][1]] = 1
        else:
            self.shipBoard[Posns[4][0],Posns[4][1]:Posns[4][1]:Posns[4][1]+2] = 1
        
        
    def recieveAttack(self, x,y):
        # player recieves an attack from other player at position X
        self.shipBoard[x,y] = 2
                      
    def sendAttack(self, player2, x, y):
        if player2.shipBoard[x,y] == 0:
            # Miss
            self.bombBoard[x,y] = -1
        if player2.shipBoard[x,y] == 1:
            # Hit
            self.bombBoard[x,y] = 1
        player2.recieveAttack(x,y)
        
    def ViewBoard(self):
        mp.figure()
        mp.imshow(self.bombBoard,cmap=cm)
        