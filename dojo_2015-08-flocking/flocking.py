import numpy as np
import matplotlib.pyplot as plt
import time

class Bird:

    def __init__(self, position, direction):
        self.xpos = position[0]
        self.ypos = position[1]
        self.xdir, self.ydir = direction

    def updateBird(self, newx, newy, newxdir, newydir):
        self.xpos = newx
        self.ypos = newy
        self.xdir = newxdir
        self.ydir = newydir


class Simulation:

    def __init__(self, nx=200, ny=200):
        self.nx = nx
        self.ny = ny
        self.birds = []
        #self.plott = plt.figure(num=1, figsize=(10, 7), dpi=100, facecolor='w')
        plt.ion()
        plt.show(block=False)
        self.nbirds = 0

    def addBird(self, birdy):
        self.birds.append(birdy)
        self.nbirds += 1

    def printBirds(self):
        plt.clf()

        # put locations and directions in some arrays
        xs = np.zeros(self.nbirds)
        ys = np.zeros(self.nbirds)
        blankdir = np.ones(self.nbirds)
        xdir = np.zeros(self.nbirds)
        ydir = np.zeros(self.nbirds)
        for i in range(self.nbirds):
            xs[i] = self.birds[i].xpos
            ys[i] = self.birds[i].ypos
            xdir[i] = self.birds[i].xdir
            ydir[i] = self.birds[i].ydir

        X, Y = np.meshgrid(xs, ys)
        U, V = np.meshgrid(xdir, ydir)
        #plt.figure()

        Q = plt.quiver(xs, ys, xdir, ydir)
        #plt.show()
        plt.draw()


    def evolveBirds(self):
        newBirds = np.copy(self.birds)

        for i in range(self.nbirds):
            #do something
            [newBirds[i].xpos, newBirds[i].ypos, newBirds[i].xdir, newBirds[i].ydir] = self.calcNewPos(self.birds[i])

        self.birds = np.copy(newBirds)


    def calcNewPos(self, birdy):
        # fixed speed = 1
        speed = 1.
        meanFlockX = 0 # mean flock xdir
        meanFlockY = 0 # mean flock ydir

        # look for all birds within sphere of radius 40
        neighbours = []
        for bb in self.birds:
            if np.sqrt((bb.xpos - birdy.xpos)**2 + (bb.ypos - birdy.ypos)**2) < 40.:
                neighbours.append(bb)
            meanFlockX += bb.xdir
            meanFlockY += bb.ydir

        meanFlockX /= self.nbirds
        meanFlockY /= self.nbirds
        # calculate 'centre of mass' = 2d mean
        x = 0.
        y = 0.
        for i in range(len(neighbours)):
            x += neighbours[i].xpos
            y += neighbours[i].ypos

        x /= np.round(len(neighbours))
        y /= np.round(len(neighbours))

        displace = np.sqrt(np.sqrt((x - birdy.xpos)**2 + (y - birdy.ypos)**2))

        if displace > 0:
            xdir = speed * (x - birdy.xpos) / displace
            ydir = speed * (y - birdy.ypos) / displace
        else:
            xdir = birdy.xdir
            ydir = birdy.ydir

        x = birdy.xpos + birdy.xdir
        y = birdy.ypos + birdy.ydir

        xdir = 0.5 * (xdir + meanFlockX)
        ydir = 0.5 * (ydir + meanFlockY)

        # need to normalise speeds again
        norm = np.sqrt(xdir**2 + ydir**2)
        xdir = speed * xdir / norm
        ydir = speed * ydir / norm

        return x, y, xdir, ydir


if __name__ == "__main__":

    nIts = 200
    nBirds = 50
    sim = Simulation()

    # generate random set of 50 birds
    randomness = np.random.random_integers(0, sim.nx, (2,nBirds))

    for row in range(nBirds):
        sim.addBird(Bird(randomness[:, row], (1,0)))

    sim.printBirds()

    for i in range(nIts):
        #time.sleep(0.02)
        sim.evolveBirds()
        sim.printBirds()


    plt.show(block=True)
