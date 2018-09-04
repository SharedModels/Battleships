# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 10:18:37 2018

@author: Dan
"""

import numpy as np
import matplotlib.pyplot as mp
from matplotlib.colors import LinearSegmentedColormap

# Setting Custom Colormap  for visualisation #
colors = [(1,1,1),(0,0,0),(1,0,0)] 
#  White(miss) -> Black(empty) ->Red(hit)  
cmap_name = 'Battleships'
n_bin = 3
cm = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bin)

class Ship:
    ## Class used to identify nature and status of ships on the board
        def __init__(self,length):
            self.length = length
            self.hits = 0
            self.status = "Afloat"
            
        def hit(self):
            self.hits += 1
            # print("hit")
            if self.hits == self.length:
                self.status = "Sunk!"
                # print("Sunk!")
            return self.status
            

        def reset(self):
            self.hits = 0
            self.status = "Afloat"

class player:
    
    def __init__(self):
        # creates a game board
        # order goes: Carrier(5), Battleship(4), Cruiser(3), Submarine(3), Destroyer(2)
        # 0 is horizontal, 1 is vertical, position taken from Top/left
        
        self.shipBoard = np.zeros((10,10)) # board containing positions of this players ships
        self.bombBoard = np.zeros((10,10)) # board containing bomb placement and hit or miss history
        self.Carrier = Ship(5)
        self.Battleship = Ship(4)
        self.Cruiser = Ship(3)
        self.Submarine = Ship(3)
        self.Destroyer = Ship(2)
        
    def populate(self, tiles):
        for i in range(5):
            self.shipBoard[tiles[0][i][0],tiles[0][i][1]] = 1
        for i in range(4):
            self.shipBoard[tiles[1][i][0],tiles[1][i][1]] = 2
        for i in range(3):
            self.shipBoard[tiles[2][i][0],tiles[2][i][1]] = 3
        for i in range(3):
            self.shipBoard[tiles[3][i][0],tiles[3][i][1]] = 4
        for i in range(2):
            self.shipBoard[tiles[4][i][0],tiles[4][i][1]] = 5

    def recieveAttack(self, x,y):
        # player recieves an attack from other player at position X
        if self.shipBoard[x,y] == 1:
            self.Carrier.hit()
        if self.shipBoard[x,y] == 2:
            self.Battleship.hit()
        if self.shipBoard[x,y] == 3:
            self.Cruiser.hit()
        if self.shipBoard[x,y] == 4:
            self.Submarine.hit()
        if self.shipBoard[x,y] == 5:
            self.Destroyer.hit()
        self.shipBoard[x,y] = -1

    def sendAttack(self, player2, x, y):
        if player2.shipBoard[x,y] == 0:
            # Miss
            self.bombBoard[x,y] = -1
        else:
            # Hit
            self.bombBoard[x,y] = 1
        player2.recieveAttack(x,y)

    def ViewBoard(self):
        mp.figure()
        mp.imshow(self.bombBoard,cmap=cm)
        
    def Reset(self):
        self.shipBoard = np.zeros((10,10))
        self.bombBoard = np.zeros((10,10))
        self.Carrier.reset()
        self.Battleship.reset()
        self.Cruiser.reset()
        self.Submarine.reset()
        self.Destroyer.reset()