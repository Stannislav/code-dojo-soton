from game import AI
import random
import copy


class BattleshipsAI(AI):

    """ Your class name must be BattleshipsAI and must extend AI. """

    # Use something unique as team name. This will identify your bot
    # on the server
    TEAM_NAME = "Stan"

    def __init__(self):
        self.shots_taken = [[0 for i in xrange(10)] for j in xrange(10)]
        self.shots_count = 0
        self.q = []
        self.victims = []
        pass

    def print_shots(self):
        # copy the list to also display the queued items
        cplist = [l[:] for l in self.shots_taken]
        cplist = map(list, zip(*cplist)) # transpose list
        # insert the queued items as '*'
        for tup in self.q:
            cplist[tup[0]][tup[1]] = '*'
        # print the field configuration
        for row in cplist:
            print " ".join("?" if not i else str(i) for i in row)

    def place_ships(self, game):

        """ While we have ships to place, place ships. """
        
        #print game.ships_to_place
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

        if len(self.q) == 0: # if nothing in queue, then just shoot randomly
            while self.shots_count < 100: # this limit shoot normally not be exceeded
                x = random.randint(0, 9)
                y = random.randint(0, 9)
                if not self.shots_taken[x][y]:
                    break
        else: # take the first element in queue
            x, y = self.q[0]
            self.q = self.q[1:]

        # Shoot
        self.shots_taken[x][y] = '.'
        self.shots_count += 1
        ret = game.take_shot(x, y)

        # Analyze the shot
        if ret[0] == True: # We have hit something!
            self.shots_taken[x][y] = "@"
            if ret[1] == None: # The ship is not dead yet! Put the neighbouring fields into queue
                tq = []
                if x > 0:
                    tq.append([x-1,y])
                if x < 9:
                    tq.append([x+1,y])
                if y > 0:
                    tq.append([x,y-1])
                if y < 9:
                    tq.append([x,y+1])
                for tup in tq:
                    if tup not in self.q and not self.shots_taken[tup[0]][tup[1]]:
                        self.q.append(tup)
            else: # This ship is done
                self.victims.append(ret[1])
                self.q = []

        # Debug
        print "This is shot number {}".format(self.shots_count)
        print "Shot at ({},{})".format(x+1,y+1)
        self.print_shots()
        print "Victims: {}".format(self.victims)
        print "---"