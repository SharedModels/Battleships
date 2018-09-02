import numpy as np
import PlayerClass as pc

positions = np.array([[0,0],[0,1],[0,2],[0,3],[0,4]])
orientations  = np.array([0,0,0,0,0])

P1 = pc.Player()
P2 = pc.Player()

P1.populate(positions,orientations)
P2.populate(positions,orientations)

# Do the attack functions work?
P1.sendAttack(P2,5,5)
P2.sendAttack(P1,0,1)

## Do the Ship Classes Work??
P2.sendAttack(P1,1,1)
P2.sendAttack(P1,2,1)
P2.sendAttack(P1,3,1)
P2.sendAttack(P1,4,1)

P1.sendAttack(P2,2,1)
## 

P1.ViewBoard()
P2.ViewBoard()