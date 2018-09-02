import numpy as np
import GameTemplate as gt

positions = np.array([[0,0],[0,1],[0,2],[0,3],[0,4]])
orientations  = np.array([0,0,0,0,0])

P = gt.Player(positions, orientations)
#P.ViewBoard()

P.Attack(5,5)
P.Attack(1,2)
P.ViewBoard()

