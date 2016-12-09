"""
CHANGED: Added reflective and periodic boundary options

TODO: Maybe do a weaker extralong-range force to take care of birds that get separated.

TODO: Model force as proper potential - Lennard-Jones might work well here.

More ideas:
    - predator/obstacle mode: create a predator or obstacle that the flock must avoid
    - attack mode: Similarly, create a target (fixed or moving) that the flock must hunt down
    - variable speeds: allow the birds' speeds to vary, such that the majority are at a steady 'cruising speed', but those that are far away or in immediate danger of crashing speed up
    - wind: add background vector wind field that advects the birds. This could be interesting to see how it shapes the flocks and how long it takes them to align with the field (a vortex would also be rather amusing)

"""

import numpy as np
import matplotlib.pyplot as plt
import time
import copy

class Bird:
    """
    Bird class. Bird has position and direction.
    """
    def __init__(self, position, direction):
        self.pos = position[:]
        self.dirr = direction[:]

    def updateBird(self, newpos, newdir):
        self.pos[:] = newpos[:]
        self.dirr[:] = newdir[:]


class Simulation:
    """
    Simulation class. Stores a list of bird objects and simulation parameters.
    """

    def __init__(self, nx=np.array([100,100]), nBirds=50, speed=1., neighbDist=40., avoidDist=10., bcs=None):
        self.nx = nx

        # list of birds
        self.birds = []

        # initialis model parameters
        self.nbirds = 0
        self.speed = speed
        self.nDim = len(nx)
        self.neighbDist = neighbDist
        self.avoidDist = avoidDist

        # initalise boundary conditions
        self.bcs = bcs
        self.axlims = np.zeros(2*self.nDim)

        self.oldBirds = None
        self.oldoldBirds = None

        # initialise plotting
        plt.ion()
        if self.bcs=="periodic" or self.bcs=="reflect":
            for (i, d) in enumerate(self.nx):
                self.axlims[2*i + 1] = d
            plt.axis(self.axlims)
        plt.show(block=False)


    def addBird(self, birdy):
        # add a bird to the simulation
        self.birds.append(birdy)
        self.nbirds += 1


    def printBirds(self):
        # plot birds
        plt.clf()
        if self.bcs=="periodic" or self.bcs=="reflect":
            plt.axis(self.axlims)

        # put locations and directions in some arrays
        xs = np.zeros((self.nbirds, self.nDim))
        dirr = np.zeros_like(xs)
        cmap = plt.get_cmap('YlOrRd')

        # vector plot
        if self.oldBirds is not None:
            if self.oldoldBirds is not None:
                for (i, bird) in enumerate(self.oldoldBirds):
                    xs[i,:] = bird.pos[:]
                    dirr[i,:] = bird.dirr[:]
                plt.quiver(xs[:,0], xs[:,1], dirr[:,0], dirr[:,1], color=cmap(0.2))

            for (i, bird) in enumerate(self.oldBirds):
                xs[i,:] = bird.pos[:]
                dirr[i,:] = bird.dirr[:]
            plt.quiver(xs[:,0], xs[:,1], dirr[:,0], dirr[:,1], color=cmap(0.5))

        for (i, bird) in enumerate(self.birds):
            xs[i,:] = bird.pos[:]
            dirr[i,:] = bird.dirr[:]
        plt.quiver(xs[:,0], xs[:,1], dirr[:,0], dirr[:,1], color=cmap(0.8))

        plt.draw()


    def evolveBirds(self):
        # move birds
        newBirds = copy.deepcopy(self.birds)
        if self.oldBirds is not None:
            self.oldoldBirds = copy.deepcopy(self.oldBirds)
        self.oldBirds = copy.deepcopy(self.birds)

        for (i, bird) in enumerate(self.birds):
            # calculate new position, direction
            [newBirds[i].pos[:], newBirds[i].dirr[:]] = self.calcNewPos(bird)

        self.birds = np.copy(newBirds)

    def enforceBcs(self, pos, dirr):
        if self.bcs=="None":
            return pos[:], dirr[:]
            # check to see if falls outside of boundary
        elif self.outsideDomain(pos):
            if self.bcs=="periodic":
                return self.periodicBcs(pos[:]), dirr[:]
            elif self.bcs=="reflect":
                return self.reflectiveBcs(pos, dirr)
        else:
            return pos[:], dirr[:]

    def outsideDomain(self, pos):
        """
        test to see if bird is outside the domain, assumed to be
        """
        for (i, x) in enumerate(pos):
            if (x < 0.) or (x >= self.nx[i]):
                return True
        return False

    def periodicBcs(self, pos):
        """
        enforce periodic boundary conditions
        """
        pos[:] = (pos[:] + self.nx[:]) % self.nx[:]
        return pos[:]

    def reflectiveBcs(self, pos, dirr):
        """
        enforce reflective boundary conditions
        """
        for (i, x) in enumerate(pos):
            if x < 0:
                 x = np.absolute(x)
                 dirr[i] =  -dirr[i]
            else: # must be greater than nx
                x = 2. * self.nx[i] - x
                dirr[i] = -dirr[i]
        return pos[:], dirr[:]


    def calcNewPos(self, birdy):
        meanNeighDir = np.zeros_like(birdy.pos) # mean neighbour direction

        # look for all birds within sphere of radius self.neighDist
        # and calculate 'centre of mass' = 2d mean
        x = np.zeros_like(birdy.pos)
        dirr = np.zeros_like(birdy.pos)
        nNeighbours = 0.
        avoidDir = np.zeros_like(birdy.pos)
        nAvoid = 0.

        for bb in self.birds:
            dist = np.sqrt(np.sum((bb.pos[:] - birdy.pos[:])**2))
            if dist < self.neighbDist:
                x[:] += bb.pos[:]
                nNeighbours += 1.
                # also check to see if neighbours are too close
                if (dist < self.avoidDist) and (dist > 0.):
                    avoidDir[:] += self.speed * (bb.pos[:] - birdy.pos[:]) * (self.avoidDist - dist) / dist
                    nAvoid += 1.
                meanNeighDir[:] += bb.dirr[:]

        if nNeighbours > 1: # 1 as bird always finds itself
            x[:] /= nNeighbours
            meanNeighDir[:] /= nNeighbours

            if nAvoid > 1:
                avoidDir[:] /= nAvoid

            norm = np.sqrt(np.sum((x[:] - birdy.pos[:])**2))

            if norm > 0: # check not going to divide by zero
                dirr = self.speed * (x[:] - birdy.pos[:]) / norm
            else:
                dirr[:] = birdy.dirr[:]

            # add on avoidance and mean neighbour directions (weighted avoidance more than the mean neighbour direction as this seems to give better behaviour)
            dirr[:] = dirr[:] - avoidDir[:] + 0.5 * meanNeighDir[:]

            # need to normalise speeds again
            norm = np.sqrt(np.sum(dirr[:]**2))
            dirr[:] *= self.speed / norm

        else:
            # PANIC MODE. Bird is lost, so double speed and fly in a random direction. It's basically going to try and random walk back to the main flock.
            # TODO: be careful when using periodic bcs!
            dirr[:] = np.random.randn(2)
            dirr[:] *= 2. * self.speed / np.sqrt(np.sum(dirr[:]**2))

        x[:] = birdy.pos[:] + birdy.dirr[:]

        x[:], dirr[:] = self.enforceBcs(x[:], dirr[:])

        return x[:], dirr[:]


if __name__ == "__main__":
    nIts = 150
    nBirds = 50
    sim = Simulation(nBirds=nBirds, bcs="reflect")

    # generate random set of 50 birds
    randd = np.concatenate((sim.nx, sim.nx)) * np.random.rand(nBirds, 2 * sim.nDim)
    randd[:, sim.nDim:] -= sim.nx[:]
    # normalise velocities
    norm = sim.speed / np.sqrt(np.sum(randd[:, sim.nDim:]**2, axis=1))
    randd[:, sim.nDim:] *= norm[:, np.newaxis]

    for row in randd:
        sim.addBird(Bird(row[:sim.nDim], row[sim.nDim:]))

    sim.printBirds()

    # do evolution
    for i in range(nIts):
        #time.sleep(0.2)
        sim.evolveBirds()
        sim.printBirds()

    plt.show(block=True)
