from game import AI
import random

shots_taken = [[0 for i in xrange(10)] for j in xrange(10)]

class BattleshipsAI(AI):

    """ Your class name must be BattleshipsAI and must extend AI. """

    # Use something unique as team name. This will identify your bot
    # on the server
    TEAM_NAME = "AWESOME-O-3000"

    def __init__(self):
        # Initialise data here
        pass

    def place_ships(self, game):

        try:
            game.place_ship(game.ships_to_place[0], 8, 4, game.VERTICAL)
            game.place_ship(game.ships_to_place[0], 1, 2, game.HORIZONTAL)
            game.place_ship(game.ships_to_place[0], 3, 7, game.HORIZONTAL)
            game.place_ship(game.ships_to_place[0], 6, 1, game.HORIZONTAL)
            game.place_ship(game.ships_to_place[0], 1, 8, game.HORIZONTAL)
        except game.CannotPlaceShip:
            pass

        """ While we have ships to place, place ships. """

        while len(game.ships_to_place) > 0:
            try:
                x = random.randint(0, 9)
                y = random.randint(0, 9)

                # We need to tell the game which ship (size) we're
                # placing, the x and y co-ordinates, and the direction to place
                # it.
                game.place_ship(game.ships_to_place[0], x, y, game.HORIZONTAL)
            except game.CannotPlaceShip:
                # This will be raised if we try to overlap ships
                # or go outside the boundary (x0-9y0-9)

                # If it is raised, ships_to_place won't change
                # so we can just loop and try again
                pass

    def take_shot(self, game):
        # ret = (False, False)
        # coords = [-1, -1]
        # for x in xrange(10):
        #     if not shots_taken[x][x]:
        #         ret = game.take_shot(x,x)
        #         coords = [x,x]
        #         shots_taken[x][x] = 1
        #         break
        #     if not shots_taken[x][(x+5)%10]:
        #         ret = game.take_shot(x,(x+5)%10)
        #         coords = [x,(x+5)%10]
        #         shots_taken[x][(x+5)%10] = 1
        #         break
        # if ret == (False, None):
        #     return
        # elif ret == (True,None):
        #     if ret[1] == False:
        #         return
        #     return
        # else:
        #     return

        # We just indicate which location we want to shoot at.
        # This will return a tuple

        # The first element of the tuple will be True or False indicating
        # if anything was hit. The second element will be None unless
        # something was destroyed - in which case it will be the size of the
        # ship destroyed.

        # E.g. If it is a miss - the return value will be
        # (False, None)

        # If it is a hit, but nothing has been destroyed completely, the return
        # value will be
        # (True, None)

        # If it is a hit, and a "Cruiser" (1x3) has been destroyed, it will be
        # (True, 3)

        x = random.randint(0, 9)
        y = random.randint(0, 9)
        check = shots_taken[x][y]
        for i in xrange(100):
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if not shots_taken[x][y]:
                break
            # print x, y
            # print shots_taken[x][y]
            # print shots_taken
        shots_taken[x][y] = 1
        ret = game.take_shot(x, y)
        if ret[0] == True:
            if ret[1] == None:
                pass
            else:
                pass
            pass
