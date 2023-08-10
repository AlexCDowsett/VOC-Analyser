# Imports
from PyQt6 import QtCore, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Qt5Agg')


class MplCanvas(Canvas):
    def __init__(self):
        self.fig = Figure(figsize=(6,4), dpi=100)
        self.ax = self.fig.add_subplot(111)


        Canvas.__init__(self, self.fig)
        #Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        Canvas.updateGeometry(self)

    def setTitle(self, title):
        self.fig.suptitle(f"{title}\n", fontweight ="bold")

# Matplotlib widget
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)   # Inherit from QWidget
        self.canvas = MplCanvas()                  # Create canvas object
        self.vbl = QtWidgets.QVBoxLayout()         # Set box for plotting
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)

        self.smartname = None
        self.day = None
        self.repeats = None
        self.showsensor = {}
        self.annotate = None
        self.showwait = None
        self.showdetails = None
        self.shownorm = None


    def update_plot(self, data, showsensor, annotate=True, showwait=True, showdetails=False, shownorm=False):
        change = False
        if self.smartname != data.smartname:
            self.smartname = data.smartname
            change = True

        if self.day != data.day:
            self.day = data.day
            change = True

        if self.repeats != data.repeats:
            self.repeats = data.repeats
            change = True

        temp = list(showsensor.values())
        if self.showsensor != temp:
            self.showsensor = temp
            change = True

        if self.annotate != annotate:
            self.annotate = annotate
            change = True

        if self.showwait != showwait:
            self.showwait = showwait
            change = True

        if self.shownorm != shownorm:
            self.shownorm = shownorm
            change = True

        if self.showdetails != showdetails:
            self.showdetails = showdetails
            change = 2

        if not change:
            return

        self.canvas.ax.cla()
        #self.canvas.ax.plot((range(len(data.data))), data.data, label=data.sensorlabels)
        
        if annotate:
            if showwait:
                r = 6
                triggers=data.triggers
            else:
                r = 5
                triggers=data.triggers[:-1]

            trigger_names = ['Baseline', 'Absorb', 'Pause', 'Desorb', 'Flush', 'Wait']
            trigger_length = [len(n) * 1.1 for n in trigger_names]

            if shownorm:
                y = -107.5
            else:
                y = +14

            if not 'pen' in data.smartname.casefold():
                y += 5

            for i in range(r):
                self.canvas.ax.text(
                    ((data.triggers[i]+data.triggers[i+1]-trigger_length[i])/2),
                    y, trigger_names[i], fontsize = 8)

        if shownorm:
            self.canvas.ax.plot(data.normdf, label=data.sensorlabels)
            if annotate:
                self.canvas.ax.vlines(x=triggers, ymin=-100, ymax=100, colors='black', ls='--', lw=1)
        else:
            self.canvas.ax.plot(data.dataframe, label=data.sensorlabels)
            if annotate:
                if 'pen' in data.smartname.casefold():
                    self.canvas.ax.vlines(x=triggers, ymin=25, ymax=320, colors='black', ls='--', lw=1)
                else:
                    self.canvas.ax.vlines(x=triggers, ymin=35, ymax=500, colors='black', ls='--', lw=1)



        #humidity = [x[-1:] for x in data.data]
        #self.canvas.ax.plot(humidity, label="Humidity (%r.h.)")

        if change == 2:
            if showdetails:
                self.canvas.ax.leg.remove()
            else:
                self.canvas.ax.leg = self.canvas.fig.legend(loc='right', 
                bbox_to_anchor=(1.08, 0.40), 
                frameon=False, 
                prop={'size': 7}
                )

        n = 0
        for sensor in showsensor.items():
            if not sensor[1]:
                self.canvas.fig.gca().lines[n].set_alpha(0)
            n += 1

        self.canvas.ax.set_xlabel('Datapoint /{0}ms'.format(int(round(1000/data.datarate))), 
               fontweight ='bold')
        self.canvas.ax.set_ylabel('Response /V', 
               fontweight ='bold')
        self.canvas.draw()

    #def savefigure(self):
    #    plt.savefig('file.jpeg', edgecolor='black', dpi=400, facecolor='black', transparent=True)

if __name__ == "__main__":
    ''#import sys

    #app = QtWidgets.QApplication(sys.argv)
    #win = MplCanvas()
    #win.show()

    #sys.exit(app.exec())