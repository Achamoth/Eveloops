def readRules(filename):
    """Opens the specified file, and reads all of the Eveloop CA state-transition rules from it"""
    """Returns a list of the rules, indexed carefully such that the same rule can be retrieved again if the Von Neumann neighbourhood states are known"""
    """Each entry in the list corresponds to one configuration of Von Neumann neighbourhood states, and contains the state the center cell should take on for that configuration"""
    """i.e. CTRBL = 00132 means that right cell is state 1, bottom cell state 3, and left cell state 2"""
    """The index into the array would then be 110, and the value would be whatever state the center cell should take on in the next timestep"""
    """The array index is determined by simply treating the CTRBL value as a base-9 value, and converting to a base-10 value, and then using that value as the index"""

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

            #Remove leading and trailing whitespace
            token = token.strip()
            #Split current token around specified delimiter (separates CTRBL from I, since each token is a CTRBL->I value)
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


def writeEveloop(fileName, ev):
    """Writes an eveloop CA grid to a text file, so it can be read in later and animated"""
    fout = open(fileName, 'w')
    grid = ev.curGrid
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            fout.write(str(grid[y][x]) + ',')
        fout.write('\n')

def readEveloop(fileName, ev):
    """Reads an eveloop CA grid from a specified text file, and sets it as the current grid for a specified eveloop object"""
    grid = [[0 for x in range(200)] for y in range(200)]
    fin = open(fileName)
    y = 0
    for line in fin:
        x = 0
        tokens = line.split(',')
        for token in tokens:
            try:
                token = token.strip()
                state = int(token)
                grid[y][x] = state
                x = x+1
            except ValueError:
                pass
        y = y+1
    ev.setGrid(grid)
