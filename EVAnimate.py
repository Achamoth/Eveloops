import numpy
import matplotlib
import scipy.ndimage
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as pyplot

"""Much of the code for this class has been adapted/borrowed from 'Think Complexity: Chapter 7', by Allen B. Downey"""

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
