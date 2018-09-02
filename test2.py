import numpy as np
import PlayerClass as pc

positions = np.array([[0,0],[0,1],[0,2],[0,3],[0,4]])
orientations  = np.array([0,0,0,0,0])

P1 = pc.Player(positions,orientations)
P2 = pc.Player(positions,orientations)

P1.sendAttack(P2,5,5)
P2.sendAttack(P1,0,1)

P1.ViewBoard()
P2.ViewBoard()