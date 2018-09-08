import PlayerClass as pc
import random as r
import NNAction as nn


class game:
    def __init__(self, runs=100):
        self.runs = runs
        self.nn = nn.NNAction()

    def placeShip(self, length):
        """ Places a ship randomly on the board, without crossing the boards
        limits. Takes the ships length as a parameter """
        while True:
            tiles = []
            startX = r.randint(0, 9)
            startY = r.randint(0, 9)
            orientation = r.randint(0, 1)
            # Horizontal Case
            if orientation == 0:
                # Exceeds board space
                if 9 - startX < length:
                    pass
                # Does not exceed board space
                elif 9 - startX >= length:
                    for i in range(length):
                        tiles.append([startX + i, startY])
                    return tiles
                    break
            # Vertical Case
            elif orientation == 1:
                # Exceeds board space
                if 9 - startY < length:
                    pass
                # Does not exceed board space
                elif 9 - startY >= length:
                    for i in range(length):
                        tiles.append([startX, startY + i])
                    return tiles
                    break

    def playerInit(self):
        """ Creates the position data for all 5 ships for a single player """
        tilesTaken = []
        for i in [5, 4, 3, 3, 2]:
            run = True
            collision = False
            while run == True:
                tiles = self.placeShip(i)
                if tilesTaken != []:
                    for a in tiles:
                        for b in tilesTaken:
                            if a not in b:
                                pass
                            elif a in b:
                                collision = True
                else:
                    collision = False
                if collision == False:
                    tilesTaken.append(tiles)
                    run = False
                elif collision == True:
                    collision = False
                    pass
        return tilesTaken

    def gameInit(self):
        """ Creates two player classes """
        p1 = pc.player()
        p2 = pc.player()
        tiles = self.playerInit()
        p1.populate(tiles)
        tiles = self.playerInit()
        p2.populate(tiles)
        return p1, p2

    def playGame(self):
        """ Plays a randomly generated move set game between two player """
        p1win = False
        p2win = False
        p1, p2 = self.gameInit()

        def getstatus(player):
            """ Update the player's ship status """
            status = [player.Carrier.status, player.Battleship.status,
                      player.Cruiser.status, player.Submarine.status
                , player.Destroyer.status]
            return status

        p1status = getstatus(p1)
        p2status = getstatus(p2)

        # Generate random attack order
        # To be replaced with NN attack order
        attacks1 = []
        attacks2 = []
        for i in range(10):
            for j in range(10):
                attacks1.append([i, j])
                attacks2.append([i, j])
        r.shuffle(attacks1)
        r.shuffle(attacks2)

        # Data set up
        state = []
        action = []
        reward = []
        # Begin game
        while True:
            if "Afloat" in p1status:
                # attack = attacks1.pop()
                # print(p1.bombBoard)
                state.append(p1.bombBoard.copy())
                attack = self.nn.action(p1.bombBoard)
                action.append(attack)
                reward.append(p1.sendAttack(p2, attack[0], attack[1]))
                p2status = getstatus(p2)
                if "Afloat" not in p2status:
                    p1win = True
                    break
            if "Afloat" in p2status and p1win == False:
                attack = attacks2.pop()
                p2.sendAttack(p1, attack[0], attack[1])
                p1status = getstatus(p1)
                if "Afloat" not in p1status:
                    p2win = True
                    break
        if p1win == True:
            print("Player 1 wins")
        if p2win == True:
            print("Player 2 wins")
        return state, action, reward

    def runGames(self):
        for i in range(self.runs):
            state, action, reward = self.playGame()
            if i % 100 == 0:
                self.nn.save()
                print('breakpoint')
            # print(state[0])
            self.nn.save_data(state, action, reward)
            self.nn.train()
            if i % 10 == 0:
                self.nn.train_target_q()
        print('done')

if __name__ == '__main__':
    gm = game(10000000)
    gm.runGames()