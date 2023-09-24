"""
Date created: 9/15/2023
Creators: Trevor Hitchcock & Joshua Castro
Description: This program is an implementation of a vacuum cleaner and its environment. The vacuum cleaner is a simple reflexive agent.
"""

import copy
import random
import time


class Agent():
    def __init__(self, locX, locY, isActive, cost, battery, isChild):
        self.locX = locX
        self.locY = locY
        self.isActive = isActive
        self.cost = cost
        self.battery = battery
        self.cleaned = 0
        self.wall = False
        self.up = True

    def __str__(self):
        return "loc x: " + str(self.locX) + "\nloc y: " + str(self.locY) + "\nisActive: " + str(
            self.isActive) + "\ncost: " + str(self.cost) + "\nbattery: " + str(self.battery) + "\n"

    def movePattern(self, e):
        # if facing up, move up, subtract battery
        if self.up:
            self.locY -= 1
            self.battery -= 0.5 * self.cost
            # if hit top wall, turn around and move right one and back to y = 1
            if self.locY == 0:
                self.locY += 1
                self.up = False
                self.battery -= self.cost
                self.locX += 1
                # if at right wall, drive all the way back to the left wall, cleaning along the way
                if self.locX == (e.size - 1):
                    while self.locX != (1):
                        self.locX -= 1
                        self.battery -= 0.5 * self.cost
                        self.clean(e)
        else:
            self.locY += 1
            self.battery -= 0.5 * self.cost
            # if at bottom wall do appropriate movements
            if self.locY == (e.size - 1):
                self.locY -= 1
                self.up = True
                self.battery -= self.cost
                self.locX += 1
                # if at right wall, drive all the way back to the left wall, cleaning along the way
                if self.locX == (e.size - 1):
                    while self.locX != (1):
                        self.locX -= 1
                        self.battery -= 0.5 * self.cost
                        self.clean(e)

    def moveRandom(self, e):
        self.locX = random.randint(1, e.size - 2)
        self.locY = random.randint(1, e.size - 2)
        self.battery -= 0.5 * self.cost

    def moveRandomDir(self, e):
        direction = random.randint(0, 3)

        if direction == 0:
            self.moveUp(e)
        elif direction == 1:
            self.moveRight(e)
        elif direction == 2:
            self.moveDown(e)
        elif direction == 3:
            self.moveLeft(e)

    def moveRight(self, e):
        self.locX = self.locX + 1
        if (e.envy[self.locY][self.locX] == 2):  # collided with the wall
            self.locX = self.locX - 1

    def moveLeft(self, e):
        self.locX = self.locX - 1
        if (e.envy[self.locY][self.locX] == 2):  # collided with the wall
            self.locX = self.locX + 1

    def moveUp(self, e):
        self.locY = self.locY + 1
        if (e.envy[self.locY][self.locX] == 2):  # collided with the wall
            self.locY = self.locY - 1

    def moveDown(self, e):
        self.locY = self.locY - 1
        if (e.envy[self.locY][self.locX] == 2):  # collided with the wall
            self.locY = self.locY + 1

    def dirty(self, e):
        if (e.envy[self.locY][self.locX] == 0):
            e.setDirty(self.locX, self.locY)

    def clean(self, e):
        if (e.envy[self.locY][self.locX] == 1):
            e.setClean(self.locX, self.locY)
            self.cleaned = self.cleaned + 1
            self.battery -= 0.5 * self.cost  # costs .5 battery to clean


class Environment():
    # Environment class, "type" is what type of environment we have. 0 is random, 1 is fixed
    def __init__(self, size, type):
        if type == 0:
            self.size = size
            self.envy = [[2 if (i == 0 or i == size - 1 or j == 0 or j == size - 1) else random.randint(0, 1) for j in
                          range(size)] for i in range(size)]
        elif type == 1:
            # this environment is fixed and 50% dirty
            self.envy = [
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                [2, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 2],
                [2, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 2],
                [2, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 2],
                [2, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 2],
                [2, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 2],
                [2, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 2],
                [2, 0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 2],
                [2, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 2],
                [2, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 2],
                [2, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 2],
                [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            ]

    def getDirty(self, size):
        dirty = 0
        for i in range(size):
            for j in range(size):
                if (self.envy[i + 1][j + 1] == 1):
                    dirty = dirty + 1
        fin_score = int((dirty / (size * size)) * 100)

        return fin_score

    def retPrintable(self, agent, size):
        ret = [["" for i in range(size)] for j in range(size)]
        for x, i in enumerate(self.envy):
            for y, j in enumerate(i):
                if (self.envy[x][y] == 1):  # dirty
                    ret[x][y] = "\U0001f4A9"
                elif (self.envy[x][y] == 2):  # border
                    ret[x][y] = "\U0001f9F1"
                else:
                    ret[x][y] = "\U0001f9FC"  # clean
        ret[agent.locY][agent.locX] = "\U0001f9FD"  # vacuum
        return ret

    def retPrintable2A(self, agent, kid, size):
        ret = [["" for i in range(size)] for j in range(size)]
        for x, i in enumerate(self.envy):
            for y, j in enumerate(i):
                if (self.envy[x][y] == 1):  # dirty
                    ret[x][y] = "\U0001f4A9"
                elif (self.envy[x][y] == 2):  # border
                    ret[x][y] = "\U0001f9F1"
                else:
                    ret[x][y] = "\U0001f9FC"  # clean
        ret[agent.locY][agent.locX] = "\U0001f9FD"  # vacuum
        ret[kid.locY][kid.locX] = "\U0001f476"  # kid
        return ret

    # This method exists so that the agent prints in the correct starting spot
    def retPrintableInitial(self, agentX, agentY, size):
        ret = [["" for i in range(size)] for j in range(size)]
        for x, i in enumerate(self.envy):
            for y, j in enumerate(i):
                if (self.envy[x][y] == 1):  # dirty
                    ret[x][y] = "\U0001f4A9"
                elif (self.envy[x][y] == 2):  # border
                    ret[x][y] = "\U0001f9F1"
                else:
                    ret[x][y] = "\U0001f9FC"  # clean
        ret[agentY][agentX] = "\U0001f9FD"  # vacuum
        return ret

    # Prints array for the third experiment
    def retPrintableInitial2A(self, agentX, agentY, kidX, kidY, size):
        ret = [["" for i in range(size)] for j in range(size)]
        for x, i in enumerate(self.envy):
            for y, j in enumerate(i):
                if (self.envy[x][y] == 1):  # dirty
                    ret[x][y] = "\U0001f4A9"
                elif (self.envy[x][y] == 2):  # border
                    ret[x][y] = "\U0001f9F1"
                else:
                    ret[x][y] = "\U0001f9FC"  # clean
        ret[agentY][agentX] = "\U0001f9FD"  # vacuum
        ret[kidY][kidX] = "\U0001f476"  # kid
        return ret

    def setClean(self, x, y):
        # swap x and y values
        self.envy[y][x] = 0

    def setDirty(self, x, y):
        # swap x and y values
        self.envy[y][x] = 1


def exp1():
    totalScore = 0
    size = 10  # size of grid without walls
    envy = Environment(size + 2, 0)  # size +2 because of borders
    envycop = copy.deepcopy(envy)  # for printing initial state
    dirty = envy.getDirty(size)
    numExperiments = 100

    for z in range(numExperiments):
        envy.envy = copy.deepcopy(envycop.envy)  # deep copy for printing original at end
        xSt = random.randint(0, size - 1) + 1
        ySt = random.randint(0, size - 1) + 1
        battery = 75

        a = Agent(xSt, ySt, True, 1, battery, True)
        while (a.battery > 0.9):
            """
            # code used to print out each step of the experiment. left commented out
            print("Current situation: ")
            print(*envy.retPrintable(a, size+2), sep = "\n")
            print()
            print("Current Location: ")
            print("x: "+str(a.locX)+"\ny: "+str(a.locY))
            print(f'Battery: {round(a.battery, 1)}')
            print("Number Cleaned: "+str(a.cleaned))
            """
            a.clean(envy)
            a.movePattern(envy)
        score = a.cleaned
        print("Start situation: ")
        print(*envycop.retPrintableInitial(xSt, ySt, size + 2), sep="\n")
        print()
        print("Final situation: ")
        print(*envy.retPrintable(a, size + 2), sep="\n")
        print()
        print("Score: " + str(score) + "\n\n\n")
        totalScore += score

    print("Total dirty in each sim " + str(dirty))
    print("Total amount cleaned overall " + str(totalScore))
    print(f'Average Score: {round((totalScore * 100) / (dirty * numExperiments), 2)}%\n\n')
    main()


def exp2():
    totalScore = 0
    size = 10  # size of grid without walls
    envy = Environment(size + 2, 0)
    envycop = copy.deepcopy(envy)
    dirty = envy.getDirty(size)
    numExperiments = 100

    for z in range(numExperiments):
        envy.envy = copy.deepcopy(envycop.envy)
        xSt = random.randint(0, size - 1) + 1
        ySt = random.randint(0, size - 1) + 1
        a = Agent(xSt, ySt, True, 1, 75, True)
        while (a.battery > 0.9):
            a.clean(envy)
            a.moveRandom(envy)
        score = a.cleaned
        print("Start situation: ")
        print(*envycop.retPrintableInitial(xSt, ySt, size + 2), sep="\n")
        print()
        print("Final situation: ")
        print(*envy.retPrintable(a, size + 2), sep="\n")
        print()
        print("Score: " + str(score) + "\n\n\n")
        totalScore += score

    print("Total dirty in each sim " + str(dirty))
    print("Total amount cleaned overall " + str(totalScore))
    print(f'Average Score: {round((totalScore * 100) / (dirty * numExperiments), 2)}%\n\n')
    main()


def exp3():
    size = 10  # size of grid without walls
    envy = Environment(size + 2, 0)
    envycop = copy.deepcopy(envy)
    dirtyAtStart = envy.getDirty(size)
    dirtyAtEnd = 0
    numExperiments = 100

    for z in range(numExperiments):
        envy.envy = copy.deepcopy(envycop.envy)
        xSt = random.randint(0, size - 1) + 1
        ySt = random.randint(0, size - 1) + 1
        xStb = random.randint(0, size - 1) + 1
        yStb = random.randint(0, size - 1) + 1
        a = Agent(xSt, ySt, True, 1, 125, True)
        b = Agent(xStb, yStb, True, 0, 9999, False)
        while (a.battery > 0.9):
            b.dirty(envy)
            a.clean(envy)
            b.moveRandomDir(envy)
            a.movePattern(envy)
        print("Start situation: ")
        print(*envycop.retPrintableInitial2A(xSt, ySt, xStb, yStb, size + 2), sep="\n")
        print()
        print("Final situation: ")
        print(*envy.retPrintable2A(a, b, size + 2), sep="\n")
        print()
        dirtyAtEnd += envy.getDirty(size)

    print("Total dirty at start of each sim " + str(dirtyAtStart))
    print("Average dirty at the end of each sim " + str(dirtyAtEnd / numExperiments))
    averageDif = dirtyAtStart - dirtyAtEnd / numExperiments
    s = (averageDif / dirtyAtStart) * 100
    print(f'Avg. Percent Cleaned: {round(s, 2)}%\n\n')
    main()


def main():
    # main menu
    test = -1
    try:
        print("This program simulates a vacuum cleaner in an environment.")
        print("There are three different expiriments we have programmed.")
        print("Experiment 1: The program is ran 100 times in an environment that is 50% dirty.")
        print("              The agent gets 75 moves to clean as much as it can.")
        print("Experiment 2: The environment is the same as before, but the agent moves randomly")
        print("              in the environment instead of up, down, left, or right.")
        print("Experiment 3: The environment is the same as in experiment one, except there is a")
        print("              'child' moving around dirtying the environment.\n")
        test = int(input("Enter the test you would like to perform (0 to quit): "))
        if (test == 1):
            print("Running experiment 1...\n")
            exp1()
        elif (test == 2):
            print("Running experiment 2...\n")
            exp2()
        elif (test == 3):
            print("Running experiment 3...\n")
            exp3()
        elif (test == 0):
            print("Exiting program")
        else:
            print("Enter a number 1, 2, or 3\n")
            main()
    except ValueError:
        print("Enter an integer\n")
        main()


main()