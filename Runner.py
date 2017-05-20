import Eveloop

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
            index = (int(states[0])*pow(9,4)) + (int(states[1])*pow(9,3)) + (int(states[2])*pow(9,2)) + (int(states[3])*pow(9,1)) + int(states[4])
            rules[index] = int(image)
    #Return list of rules
    return rules

def main():
    #Read in state-transition rules for eveloop
    rules = readRules('StateTransitionRules.txt')
    #Set up eveloop
    eveloop = Eveloop.Eveloop(150, 13, 2)
    #Set state-transition rules
    eveloop.setRules(rules)
    #Run over 1000 timesteps
    for i in range(100):
        pass
        print(i)
        eveloop.tick()

main()
