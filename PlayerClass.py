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
            if self.hits == self.length:
                self.status = "Sunk!"
                print("Sunk!")
                return self.status
            
        def reset(self):
            self.hits = 0
            self.status = "Afloat"
    

class Player:
    
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
    
    def populate(self, posns, orientations):
        ### Populating board with ships ###
        ### Each ship has a corresponding value used to identiy it when hit
        # Carrier
        if orientations[0] == 0:
            self.shipBoard[posns[0][0]:posns[0][0]+5,posns[0][1]] = 1
        else:
            self.shipBoard[posns[0][0],posns[0][1]:posns[0][1]:posns[0][1]+5] = 1
        # BattleShip
        if orientations[1] == 0:
            self.shipBoard[posns[1][0]:posns[1][0]+4,posns[1][1]] = 2
        else:
            self.shipBoard[posns[1][0],posns[0][1]:posns[1][1]:posns[1][1]+4] = 2
        # Cruiser
        if orientations[2] == 0:
            self.shipBoard[posns[2][0]:posns[1][0]+3,posns[2][1]] = 3
        else:
            self.shipBoard[posns[2][0],posns[2][1]:posns[2][1]:posns[2][1]+3] = 3
        # Submarine
        if orientations[3] == 0:
            self.shipBoard[posns[3][0]:posns[3][0]+3,posns[3][1]] = 4
        else:
            self.shipBoard[posns[3][0],posns[3][1]:posns[3][1]:posns[3][1]+3] = 4
        # Destroyer
        if orientations[4] == 0:
            self.shipBoard[posns[4][0]:posns[4][0]+2,posns[4][1]] = 5
        else:
            self.shipBoard[posns[4][0],posns[4][1]:posns[4][1]:posns[4][1]+2] = 5

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

        