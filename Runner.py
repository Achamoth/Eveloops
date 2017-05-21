import Eveloop
import EVAnimate
import FileOps

def main():
    rules = FileOps.readRules('StateTransitionRules.txt')
    species = int(raw_input('What species do you want to start with? '))
    var = int(raw_input('What variant (i.e. 2, 3, 4, 5 etc.)? '))
    ev = Eveloop.Eveloop(200,species,var)
    ev.setRules(rules)
    time = int(raw_input('How many timesteps do you want to run the CA for? '))
    for i in range(time):
        print('Timestep: ' + str(i))
        ev.tick()
    viewer = EVAnimate.EViewer(ev)
    print('\nAnimation beginning. Note that animation is very slow.\nWhen it completes, it will display the last state as a still image\n (i.e. it will not close automatically)\n')
    time = int(raw_input('How many animated timesteps do you want to run the CA for (warning: very slow)? '))
    viewer.animate(time)

main()
