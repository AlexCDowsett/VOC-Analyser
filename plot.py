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


    def update_plot(self, data, annotate=True, showwait=True):
        self.canvas.ax.cla()
        self.canvas.ax.plot((range(len(data.data))), data.data)

        if annotate:
            if showwait:
                r = 6
                triggers=data.triggers
            else:
                r = 5
                triggers=data.triggers[:-1]

            self.canvas.ax.vlines(x=triggers, ymin=25, ymax=320, colors='black', ls='--', lw=1)
            trigger_names = ['Baseline', 'Absorb', 'Pause', 'Desorb', 'Flush', 'Wait']
            trigger_length = [len(n) * 1.8 for n in trigger_names]

            for i in range(r):
                self.canvas.ax.text(
                    (data.triggers[i]+data.triggers[i+1]-trigger_length[i])/2,
                    +14, trigger_names[i], fontsize = 8)


            #self.canvas.ax.text(data.triggers[2]-4.5, -10, 'Absorb', rotation=90, fontsize = 10)
            #self.canvas.ax.text(data.triggers[3]-4.5, -10, 'Pause', rotation=90, fontsize = 10)
            #self.canvas.ax.text(data.triggers[4]-4.5, -10, 'Desorb', rotation=90, fontsize = 10)
            #self.canvas.ax.text(data.triggers[5]-4.5, -10, 'Flush', rotation=90, fontsize = 10)
            
            #self.canvas.ax.text(data.triggers[6]-4.5, -10, 'Wait', rotation=90, fontsize = 10)

        humidity = [x[-1:] for x in data.data]
        self.canvas.ax.plot(humidity, label="Humidity (%r.h.)")

        leg = self.canvas.fig.legend(loc='lower right', bbox_to_anchor=(0.91,-0.012))

        self.canvas.ax.set_xlabel('Datapoint /250ms', 
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