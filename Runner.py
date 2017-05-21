import Eveloop
import EVAnimate
import FileOps

def main():
    """Controls flow of program, and sets up & executes eveloop CA, before animating results"""

    #Read in state transition rules for Eveloop CA from text file
    rules = FileOps.readRules('StateTransitionRules.txt')

    #Ask user for starting species and what type of eveloop (i.e. 2-eveloop, 3-eveloop, 4-eveloop etc.)
    species = int(raw_input('What species do you want to start with? '))
    var = int(raw_input('What variant (i.e. 2, 3, 4, 5 etc.)? '))

    #Create eveloop (on 200x200 grid)
    ev = Eveloop.Eveloop(200,species,var)
    #Set state transition rules (read in earlier)
    ev.setRules(rules)

    #Ask user how many timesteps they want to run CA for
    time = int(raw_input('How many timesteps do you want to run the CA for? '))

    #Run CA for specified number of timesteps
    for j in range(10):
        for i in range(time):
            print(str(j+1) + ' - Timestep: ' + str(i+1))
            ev.tick()
        #Save Eveloop config to file
        outName = 'Eveloop ' + str(species) + ' ' + str(var) + ' ' + str(j+1) + '.txt'
        FileOps.writeEveloop(outName, ev)

    #Set up viewer for animation
    viewer = EVAnimate.EViewer(ev)

    #Ask user how many timesteps they want to animate
    print('\nAnimation beginning. Note that animation is very slow.\nWhen it completes, it will display the last state as a still image\n (i.e. it will not close automatically)\n')
    time = int(raw_input('How many animated timesteps do you want to run the CA for (warning: very slow)? '))

    #Animate CA over specified number of timesteps
    viewer.animate(1)

def animateCA(filename):
    """Start from a configuratio stored in the specified file, and animate that configuration"""
    """Used for results gathering. Every 5000 timesteps, I save a CA grid into a file, and this method lets me open those files and animate the grids to get screenshots and data"""
    rules = FileOps.readRules('StateTransitionRules.txt')
    ev = Eveloop.Eveloop()
    ev.setRules(rules)
    FileOps.readEveloop(filename, ev)
    viewer = EVAnimate.EViewer(ev)
    viewer.animate(1)

main()
