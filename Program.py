import copy
import sys
import numpy
import matplotlib
import scipy.ndimage
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as pyplot

class Eveloop(object):

    def __init__(self, n=200, species=13, var=2):
        self.lastGrid = [[0 for x in range(n)] for y in range(n)]
        self.lastGrid = numpy.array(self.lastGrid)
        self.curGrid = [[0 for x in range(n)] for y in range(n)]
        self.curGrid = numpy.array(self.curGrid)
        messenger = self.setGridAndBox()
        self.setSpecies(species, var, messenger)
        self.n = n

    def setSpecies(self, species, var, messenger):
        #Get location of messenger cell
        y, x = messenger

        #First, place the two green Gene cells
        self.curGrid[y+1][x-1] = 4 #First green gene cell
        self.curGrid[y+1][x-2] = 0 #Trailing background cell
        self.curGrid[y+1][x-4] = 4 #Second green gene cell
        self.curGrid[y+1][x-5] = 0 #Trailing background cell

        #Next, place the leading white gene cells
        numLeading = var
        y = y+2
        direction = 0 #0 is up, 1 is left, 2 is down
        for i in range(numLeading):
            #Place white gene cell and trailing background cell
            #Moving up
            if(direction == 0):
                self.curGrid[y][x] = 0 #Trailing backgrund cell
                if(self.curGrid[y+1][x] == 2):
                    direction = 1
                    x = x-1
                    self.curGrid[y][x] = 7 #White gene cell
                    x = x-2
                else:
                    y = y+1
                    self.curGrid[y][x] = 7 #White gene cell
                    if(self.curGrid[y+1][x] == 2):
                        direction = 1
                        x = x-2
                    elif(self.curGrid[y+2][x] == 2):
                        y = y+1
                        x = x-1
                        direction = 1
                    else:
                        y = y+2

            #Moving Left
            elif(direction == 1):
                #Moving left
                self.curGrid[y][x] = 0 #Trailing background cell
                if(self.curGrid[y][x-1] == 2):
                    direction = 2
                    y = y+1
                    self.curGrid[y][x] = 7 #White gene cell
                    y = y+2
                else:
                    x = x-1
                    self.curGrid[y][x] = 7 #White gene cell
                    if(self.curGrid[y][x-1] == 2):
                        direction = 2
                        y = y+2
                    elif(self.curGrid[y][x-2] == 2):
                        x = x-1
                        y = y+1
                        direction = 2
                    else:
                        x = x-2

            #Moving Down
            #TODO: Don't need to do any checks here, as long as the species isn't larger than 13/14
            elif(direction == 2):
                self.curGrid[y][x] = 0 #Trailing background cell
                y = y-1
                self.curGrid[y][x] = 7 #White gene cell
                y = y-2

        #Finally, place the trailing white gene cells
        numTrailing = species - var
        y,x = messenger
        x= x-7
        y = y+1
        direction = 0 #0 is left, 1 is up, 2 is right
        for i in range(numTrailing):
            #Place white gene cell and trailing background cell

            #Moving left
            if(direction == 0):
                self.curGrid[y][x] = 7 #White gene cell
                if(self.curGrid[y][x-1] == 2):
                    y = y+1
                    self.curGrid[y][x] = 0 #Trailing background cell
                    y = y+2
                    direction = 1
                else:
                    x = x-1
                    self.curGrid[y][x] = 0 #Trailing background cell
                    if(self.curGrid[y][x-1] == 2):
                        direction = 1
                        y = y+2
                    elif(self.curGrid[y][x-2] == 2):
                        direction = 1
                        x = x-1
                        y = y+1
                    else:
                        x = x-2

            #Moving up
            elif(direction == 1):
                self.curGrid[y][x] = 7 #White gene cell
                if(self.curGrid[y+1][x] == 2):
                    x = x+1
                    self.curGrid[y][x] = 0 #Trailing background cell
                    x = x+2
                    direction = 2
                else:
                    y = y+1
                    self.curGrid[y][x] = 0 #Trailing background cell
                    if(self.curGrid[y+1][x] == 2):
                        direction = 2
                        x = x+2
                    elif(self.curGrid[y+2][x] == 2):
                        direction = 2
                        y = y+1
                        x = x+1
                    else:
                        y = y+2

            #Moving right
            #TODO: Don't need to do any checks here, as long as species isn't larger than 13, and var is at least 2
            elif(direction == 2):
                self.curGrid[y][x] = 7 #White gene cell
                x = x+1
                self.curGrid[y][x] = 0 #Trailing background cell
                x = x+2

    def setGridAndBox(self):
        #First, set all cells to background state
        for y in range(0,len(self.curGrid)):
            for x in range(0,len(self.curGrid[y])):
                self.curGrid[y][x] = 0

        #Now, set up (in roughly the middle of the grid), an empty square
        y = len(self.curGrid)/2
        x = len(self.curGrid[0])/2 #Bottom lefthand corner of inner sheath

        #Create the inner sheath
        for i in range(13):
            self.curGrid[y+i][x] = 2
            self.curGrid[y+i][x+12] = 2
        for i in range(13):
            self.curGrid[y][x+i] = 2
            self.curGrid[y+12][x+i] = 2
        y = y-2
        x = x-1 #Leftmost position on outer lower sheath
        for i in range(15):
            self.curGrid[y][x+i] = 2
            self.curGrid[y+16][x+i] = 2
        self.curGrid[y][x+14] = 5 #Create the messenger, to point where a new sprout should be generated
        messenger = (y, x+14)
        y = y+1
        x = x-1 #Bottom of outer left sheath
        for i in range(15):
            self.curGrid[y+i][x] = 2
            self.curGrid[y+i][x+16] = 2

        #Finally, create the core cells, which fill the tube and conduct genes in it
        for i in range(15):
            self.curGrid[y][x+1+i] = 1
            self.curGrid[y+14][x+1+i] = 1
        for i in range(15):
            self.curGrid[y+i][x+1] = 1
            self.curGrid[y+i][x+15] = 1

        #Return the position of the messenger cell
        return messenger

    def setRules(self, rules):
        self.rules = rules

    def getState(self, x, y):
        #Given an (x, y) tuple, get the state of the cell at that position in the last timestep's grid
        xPos = x
        yPos = y
        if(yPos == -1):
            yPos = len(self.lastGrid)-1
        elif(yPos == len(self.lastGrid)):
            yPos = 0
        if(xPos == -1):
            xPos = len(self.lastGrid[yPos])-1
        elif(xPos == len(self.lastGrid[yPos])):
            xPos = 0
        return self.lastGrid[yPos][xPos]

    def getNextState(self, c, t, r, b, l):
        #Given the states of a neighbourhood, get the next state for the center
        #First, check if we have a defined state-transition in 'rules' for the states of the neihbourhood
        index = (c*pow(9,4)) + (t*pow(9,3)) + (r*pow(9,2)) + (b*pow(9,1)) + (l)
        if(self.rules[index] != -1):
            return self.rules[index]
        else:
            #Transition not defined manually in table. Find next state according to the following rules
            if(c == 8):
                #8->0 in all cases
                return 0
            elif(t==8 or r==8 or b==8 or l==8):
                #At least one neighbour (TRBL) in state 8
                if(c==0 or c==1):
                    #Center is 0 or 1
                    if((t>=2 and t<=7) or (r>=2 and r<=7) or (b>=2 and b<=7) or (l>=2 and l<=7)):
                        #At least one neighbour in state 2,3,...,7
                        #0,1->8
                        return 8
                    else:
                        #No neighbours in state 2,3,...,7
                        #0->0 and 1->1
                        return c
                elif(c==2 or c==3 or c==5):
                    #2,3,5->0
                    return 0
                elif(c==4 or c==6 or c==7):
                    #4,6,7->1
                    return 1
            else:
                #No neighbours in state 8, and center not in state 8
                if(c==0):
                    #0->0
                    return 0
                else:
                    #1,2,...,7,8->8
                    print(c,t,r,b,l)
                    return 8

    def getGrid(self):
        return self.curGrid

    def tick(self):
        self.lastGrid = copy.deepcopy(self.curGrid)
        #Loop over all cells
        for y in range(0,len(self.lastGrid)):
            for x in range(0,len(self.lastGrid[y])):
                #Check states of current cell's neighbours, and its own state
                c = self.getState(x, y)
                t = self.getState(x, y+1)
                r = self.getState(x+1, y)
                b = self.getState(x, y-1)
                l = self.getState(x-1, y)
                #Determine cell's next state
                image = self.getNextState(c,t,r,b,l)
                #Update grid
                self.curGrid[y][x] = image

class EViewer(object):
    """Generates an animated view of the grid."""
    def __init__(self, ev, cmap=matplotlib.cm.Paired):
        self.ev = ev
        self.cmap = cmap

        self.fig = pyplot.figure()
        pyplot.axis([0, ev.n, 0, ev.n])
        pyplot.xticks([])
        pyplot.yticks([])

        self.pcolor = None
        self.update()

    def update(self):
        """Updates the display with the state of the grid."""
        if self.pcolor:
            self.pcolor.remove()

        a = self.ev.curGrid
        self.pcolor = pyplot.pcolor(a, cmap=self.cmap)
        self.fig.canvas.draw()

    def animate(self, steps=10):
        """Creates the GUI and then invokes animate_callback.

        Generates an animation with the given number of steps.
        """
        self.steps = steps
        self.fig.canvas.manager.window.after(1000, self.animate_callback)
        pyplot.show()

    def animate_callback(self):
        """Runs the animation."""
        for i in range(self.steps):
            self.ev.tick()
            self.update()

def readRules(filename):
    #Create empty list in which to store all of the rules
    rules = [-1 for y in range(59049)]
    #Open file containing state transition rules
    fin = open(filename)
    fin.readline() #Skip first line (header)
    #Read all lines in file
    for curLine in fin:
        #Split current line around whitespace delimiter
        tokens = curLine.split('  ')
        #Remove newline character from last token
        tokens[len(tokens)-1] = tokens[len(tokens)-1][:-1]
        #Loop over each token (each token is one state-transition rule)
        for token in tokens:
            token.strip() #Remove leading and trailing whitespace
            states,image = token.split('->')
            #Store state-transition rule in list
            index = (int(states[0])*pow(9,4)) + (int(states[1])*pow(9,3)) + (int(states[2])*pow(9,2)) + (int(states[3])*9) + int(states[4])
            rules[index] = int(image)
            #Store all rotationally symmetric rules in list
            index = (int(states[0])*pow(9,4)) + (int(states[2])*pow(9,3)) + (int(states[3])*pow(9,2)) + (int(states[4])*9) + int(states[1])
            rules[index] = int(image)
            index = (int(states[0])*pow(9,4)) + (int(states[3])*pow(9,3)) + (int(states[4])*pow(9,2)) + (int(states[1])*9) + int(states[2])
            rules[index] = int(image)
            index = (int(states[0])*pow(9,4)) + (int(states[4])*pow(9,3)) + (int(states[1])*pow(9,2)) + (int(states[2])*9) + int(states[3])
            rules[index] = int(image)
    #Return list of rules
    return rules

def main():
    rules = readRules('StateTransitionRules.txt')
    ev = Eveloop(150,13,2)
    ev.setRules(rules)
    for i in range(5000):
        print(i)
        ev.tick()
    viewer = EViewer(ev)
    viewer.animate(100)

main()
