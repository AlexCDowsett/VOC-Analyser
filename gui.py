from PyQt6 import QtCore, QtGui, QtWidgets

from datahandler import open_files, load, avgload
from plot import MplCanvas, MplWidget
from PCA import Calculate_PCA, Calculate_PCA_2
from time import sleep
import pandas as pd
import numpy as np
import re
import os

def main():

    #profiling();return

    import sys
    app = QtWidgets.QApplication(sys.argv)
    global win
    win = Window()
    win.show()

    sys.exit(app.exec())


def profiling():
    import sys
    import cProfile
    import pstats

    with cProfile.Profile() as pr:
        app = QtWidgets.QApplication(sys.argv)
        global win
        win = Window()
        win.show()

        app.exec()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    #stats.print_stats()
    stats.dump_stats(filename='stats.prof')


class Window(QtWidgets.QMainWindow):
    '''Main Window.'''
    def __init__(self, parent=None):
        '''Initializer.'''
        try:
            self.isVisible()
        except RuntimeError:
            super().__init__(parent)

        self.setWindowTitle("VOC Tool")
        self.resize(800, 600)
        self.setFixedSize(800, 600)
        self.setWindowIcon(QtGui.QIcon('logo.png'))

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")

        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 800, 600))
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setMovable(True)
        #self.tabWidget.setDocumentMode(True)
        #self.tabWidget.tabBarClicked(self.show_wait)
        self.tabWidget.blockSignals(True)
        self.tabWidget.currentChanged.connect(lambda x: self.update_plot())

        self.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")

        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")

        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")

        self.menuSettings = QtWidgets.QMenu(self.menubar)
        self.menuSettings.setObjectName("menuSettings")

        self.menuWindow = QtWidgets.QMenu(self.menubar)
        self.menuWindow.setObjectName("menuWindow")

        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")

        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")

        self.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage('')

        self.actionOpen = QtGui.QAction(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/icons/folder-open-document.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        self.actionOpen.triggered.connect(self.openfile)

        self.actionOpen_folder = QtGui.QAction(self)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/icons/folder-open.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionOpen_folder.setIcon(icon3)
        self.actionOpen_folder.setObjectName("actionOpen_folder")
        self.actionOpen_folder.triggered.connect(self.openfolder)

        self.actionQuit = QtGui.QAction(self)
        self.actionQuit.setObjectName("actionQuit")
        self.actionQuit.triggered.connect(self.close)

        self.actionAverage = QtGui.QAction(self)
        self.actionAverage.setObjectName("actionAverage")
        self.actionAverage.setCheckable(True)
        self.actionAverage.triggered.connect(self.show_avg)
        self.avg = False

        self.actionNorm = QtGui.QAction(self)
        self.actionNorm.setObjectName("actionNorm")
        self.actionNorm.setCheckable(True)
        self.actionNorm.triggered.connect(self.show_norm)
        self.shownorm = False

        self.actionMinimise = QtGui.QAction(self)
        self.actionMinimise.setObjectName("actionMinimise")
        self.actionMinimise.triggered.connect(self.showMinimized)

        self.actionAnnotate = QtGui.QAction(self)
        self.actionAnnotate.setObjectName("actionAnnotate")
        self.actionAnnotate.setCheckable(True)
        self.actionAnnotate.setChecked(True)
        self.actionAnnotate.triggered.connect(self.show_annotate)
        self.annotate = True


        self.actionShowwait = QtGui.QAction(self)
        self.actionShowwait.setObjectName("actionShowwait")
        self.actionShowwait.setCheckable(True)
        self.actionShowwait.triggered.connect(self.show_wait)
        self.showwait = False

        #self.actionExport_to_excel = QtGui.QAction(self)
        #icon1 = QtGui.QIcon()
        #icon1.addPixmap(QtGui.QPixmap("icons/icons/document-excel-table.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        #self.actionExport_to_excel.setIcon(icon1)
        #self.actionExport_to_excel.setObjectName("actionExport_to_excel")

        self.actionDelete_all_imports = QtGui.QAction(self)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/icons/table--minus.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionDelete_all_imports.setIcon(icon2)
        self.actionDelete_all_imports.setObjectName("actionDelete_all_imports")
        self.actionDelete_all_imports.triggered.connect(self.deleteimports)

        self.actionPreferences = QtGui.QAction(self)
        self.actionPreferences.setObjectName("actionPreferences")

        self.actionHelp = QtGui.QAction(self)
        self.actionHelp.setObjectName("actionHelp")

        self.actionLicense = QtGui.QAction(self)
        self.actionLicense.setObjectName("actionLicense")

        self.noneLabel = QtWidgets.QLabel(self, text='No data found.\nGo to File -> Import... to get started.')
        self.noneLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.noneLabel.setGeometry(QtCore.QRect(300, 200, 200, 200))
        self.noneLabel.setObjectName("None Label")

        #self.avgCheckBox = QtWidgets.QCheckBox(self, text="Average")
        #self.avgCheckBox.setGeometry(QtCore.QRect(705, 548, 100, 20))
        #self.avgCheckBox.setChecked(True)
        #self.avgCheckBox.stateChanged.connect(self.show_avg)
        #self.avgCheckBox.setStatusTip('If enabled, data is averaged for each day')
        #self.showavg = True

        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.actionOpen_folder)
        self.menuFile.addSeparator()
        #self.menuFile.addAction(self.actionExport_to_excel)
        self.menuFile.addAction(self.actionDelete_all_imports)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)

        self.menuEdit.addAction(self.actionAverage)
        self.menuEdit.addAction(self.actionNorm)

        self.menuView.addAction(self.actionAnnotate)
        self.menuView.addAction(self.actionShowwait)

        self.menuSettings.addAction(self.actionPreferences)

        self.menuWindow.addAction(self.actionMinimise)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionLicense)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())
        self.menubar.addAction(self.menuWindow.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.data = load()

        if not hasattr(self, 'recalculate_average'):
            self.recalculate_average = None

        if self.data != {}:
            self.noneLabel.setText('')
        else:
            self.tabWidget.hide()

        self.avgdata = avgload(self.data, self.recalculate_average)


        #self.data = {}
        self.tabs = {}
        self.tabSliders = {}
        self.tabDaySpin = {}
        self.tabRepeatSpin = {}
        self.tabPlot = {}
        self.vals = {}
        self.avgvals = {}
        self.tabLabel = {}
        self.tabButton = {}
        self.tabButton2 = {}
        self.detailsButton = {}
        self.min_repeats = {}
        self.max_repeats = {}
        self.sensorLabel = {}

        for key in self.data:
            self.tabs[key] = QtWidgets.QWidget()
            self.tabs[key].setObjectName(key)
            self.tabs[key].pen = key
            self.tabWidget.addTab(self.tabs[key], "")

        self.showdetails = True

        for key, tab in self.tabs.items():

            title = f"{key} sensor data"

            self.tabPlot[key] = MplWidget(tab)
            self.tabPlot[key].canvas.ax.plot([0,1,2,3,4], [10,1,20,3,40])
            self.tabPlot[key].setGeometry(QtCore.QRect(-30, 0, 680, 500))
            self.tabPlot[key].setObjectName(key + " plot")
            self.tabPlot[key].canvas.setTitle(title)

            self.tabSliders[key] = QtWidgets.QSlider(tab)
            self.tabSliders[key].setGeometry(QtCore.QRect(50, 500, 500, 20))
            self.tabSliders[key].setOrientation(QtCore.Qt.Orientation.Horizontal)
            self.tabSliders[key].setObjectName(key + " slider")
            self.tabSliders[key].setStatusTip('Change the test displayed')

            self.vals[key] = []

            max_day = 0
            temp = list(self.data[key].keys())
            for i in range(len(temp)): 
                if temp[i] == 'water':
                    temp[i] = -1
            self.avgvals[key] = sorted(temp)

            for day in range(len(self.avgvals[key])):
                if self.avgvals[key][day] == -1:
                    self.avgvals[key][day] = 'water'
                    day = 'water'

            for day in range(len(self.avgvals[key])+1):

                for repeat in range(0, 5):
                    if self.data[key].get(day):
                        if self.data[key][day].get(repeat):
                            self.vals[key].append([day, repeat])


            self.min_repeats[key] = {}
            self.max_repeats[key] = {}
            for day, repeat in self.vals[key]:
                if not self.min_repeats[key].get(day):
                    self.min_repeats[key][day] = repeat
                if not self.max_repeats[key].get(day) or self.max_repeats[key].get(day) < repeat:
                    self.max_repeats[key][day] = repeat

            #for day in self.min_repeats[key].keys():
            #    print(day, self.min_repeats[key][day], self.max_repeats[key][day])



            self.tabSliders[key].setRange(0, (len(self.vals[key])-1))
            self.tabSliders[key].setSingleStep(1)
            self.tabSliders[key].setValue(0)              
            self.tabSliders[key].setTickPosition(QtWidgets.QSlider.TickPosition.TicksAbove)
            self.tabSliders[key].setTickInterval(1)
            self.tabSliders[key].valueChanged.connect(self.slider_change)

            self.tabDaySpin[key] = QtWidgets.QSpinBox(tab)
            self.tabDaySpin[key].setGeometry(QtCore.QRect(560, 500, 60, 20))
            self.tabDaySpin[key].setObjectName(key + " daySpin")
            self.tabDaySpin[key].setRange(0, self.avgvals[key][-1:][0])
            self.tabDaySpin[key].setPrefix('Day ')

            temp = self.vals[key][0][0]
            if temp == 'water':
                temp = -1
            self.tabDaySpin[key].setValue(temp)
            self.tabDaySpin[key].setSpecialValueText('Water')
            self.tabDaySpin[key].valueChanged.connect(self.day_spin_change)
            self.tabDaySpin[key].setStatusTip('Change the test displayed by day')

            self.tabRepeatSpin[key] = QtWidgets.QSpinBox(tab)
            self.tabRepeatSpin[key].setGeometry(QtCore.QRect(630, 500, 70, 20))
            self.tabRepeatSpin[key].setObjectName(key + " repeatSpin")
            self.tabRepeatSpin[key].setRange(self.min_repeats[key][self.vals[key][0][0]], self.max_repeats[key][self.vals[key][0][0]])
            self.tabRepeatSpin[key].setPrefix('Repeat ')
            self.tabRepeatSpin[key].setValue(self.vals[key][0][1])
            self.tabRepeatSpin[key].valueChanged.connect(self.repeat_spin_change)
            self.tabRepeatSpin[key].setStatusTip('Change the test displayed by repeat')

            self.tabLabel[key] = QtWidgets.QLabel(tab)
            self.tabLabel[key].setGeometry(QtCore.QRect(585, 50, 200, 450))
            self.tabLabel[key].setObjectName(key + " label")
            self.tabLabel[key].setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)

            self.sensorLabel[key] = {}
            self.sensorlabels = self.data[key][list(self.data[list(self.data)[0]])[0]][list(self.data[key][list(self.data[key])[0]])[0]].sensorlabels
            y = 15
            n = 0
            self.showsensor = {}
            for sensorlabel in self.sensorlabels:
                self.sensorLabel[key][sensorlabel] = QtWidgets.QCheckBox(self, text=sensorlabel)
                self.showsensor[sensorlabel] = True
                self.sensorLabel[key][sensorlabel].setGeometry(QtCore.QRect(642, 156+(y*n), 100, y))
                n += 1
                self.sensorLabel[key][sensorlabel].setChecked(True)
                self.sensorLabel[key][sensorlabel].stateChanged.connect(lambda state, x=sensorlabel: self.show_sensor(state, x))
                self.sensorLabel[key][sensorlabel].setStatusTip('Show/hide ' + sensorlabel)
                self.sensorLabel[key][sensorlabel].setStyleSheet("font-size : 10px")
                #self.showavg = True

            self.detailsButton[key] = QtWidgets.QPushButton("Show details", tab)
            self.detailsButton[key].setGeometry(QtCore.QRect(625, 20, 100, 25))
            self.detailsButton[key].setObjectName(key + " detailsButton")
            self.detailsButton[key].clicked.connect(self.show_details)
            self.detailsButton[key].setStatusTip('Show further test details')
            self.showdetails = False

            self.tabButton[key] = QtWidgets.QPushButton("Show Sensor PCA", tab)
            self.tabButton[key].setGeometry(QtCore.QRect(60, 463, 110, 25))
            self.tabButton[key].setObjectName(key + " pcabutton")
            self.tabButton[key].clicked.connect(self.show_pca)

            self.tabButton2[key] = QtWidgets.QPushButton("Analyse", tab)
            self.tabButton2[key].setGeometry(QtCore.QRect(477, 463, 100, 25))
            self.tabButton2[key].setObjectName(key + " analysebutton")
            self.tabButton2[key].clicked.connect(self.analyse)
            

            self.update_plot(key, self.vals[key][0][0], self.vals[key][0][1])


        self.retranslateUi()
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.blockSignals(False)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.show_details()


        return
        ####
        try:
            self.Display_PCA()
        except ValueError:
            pass

    def analyse(self):
        self.w = AnalyseWindow()
        self.setDisabled(True)
        self.w.show()
        self.setDisabled(False)




    def Display_PCA(self, options=None):

        type = 'a'

        if options != None:
            if options[0] == 'Amplitude':
                type = 'a'
            elif options[0] == 'Decay Value':
                type = 'd'
            elif options[0] == 'Time to return to baseline':
                type = 'r'
            elif options[0] == 'Maximum gradient':
                type = 'g'
            elif options[0] == 'Amplitude - baseline':
                type = 'ab'


        if options[2]: # If exclude first repeat
            pass

        dfs = {}
        sensorlabels = ['Sen-' + str(x) for x in range(1, 25)]
        sensorlabels.append('Humidity')
        vp = {}

        for pen in self.avgdata.keys():

            descriptors = []
            column_names = []
            for day in self.avgdata[pen]:
                if type == 'g':
                    descriptors.append(self.avgdata[pen][day]['avg'].max_gradient)
                elif type == 'd':
                    descriptors.append(list(self.avgdata[pen][day]['avg'].decayb.values()))
                elif type == 'r':
                    descriptors.append(list(self.avgdata[pen][day]['avg'].bl_return_point.values()))
                elif type == 'a':
                    descriptors.append(self.avgdata[pen][day]['avg'].amplitude)
                elif type == 'ab':
                    descriptors.append(self.avgdata[pen][day]['avg'].ampbl)

                vacprot = self.avgdata[pen][day]['avg'].vacprot

                column_names.append(str(self.avgdata[pen][day]['avg'].room) + '_' + str(self.avgdata[pen][day]['avg'].day))
                if vacprot == 'No treatment':
                    colour = 'gray'
                elif 'Lawsonia' in vacprot:
                    colour = 'orange'
                elif 'Circoflex' in vacprot:
                    colour = 'purple'
                elif 'Saline' in vacprot:
                    colour = 'green'
                elif vacprot == 'Water Removed':
                    colour = 'blue'
                else:
                    colour = 'red'


                vp[(str(self.avgdata[pen][day]['avg'].room) + '_' + str(self.avgdata[pen][day]['avg'].day))] = colour

        
            descriptors = list(zip(*descriptors))

            descdf = pd.DataFrame(descriptors, columns=column_names, index=sensorlabels)

            descdf = descdf.replace(0, np.NaN)
            if type == 'g':
                descdf.type = 'Gradient'
            elif type == 'd':
                descdf.type = 'Decay Value'
            elif type == 'r':
                descdf.type = 'Return to Baseline Time'
            elif type == 'a':
                descdf.type = 'Amplitude'
            elif type == 'ab':
                descdf.type = 'Amplitude - baseline'


            dfs[pen] = descdf.astype(float)

        #for pen in self.avgdata.keys():
                #Calculate_PCA_2(dfs[pen])

        result = pd.concat(list(dfs.values()), axis=1)


        #print(result)


        if not options[1]:  #If include only selected sensors
            for k, v in self.showsensor.items():
                #print(k, v)
                if not v:
                    result = result.drop(k) 

        #print(result)
        result.type = descdf.type
        result.pen = pen
        del descdf

        #print(result[['2_19 Circoflex+0']].to_string(index=False))
        #print(result[['2_20 Circoflex+1']].to_string(index=False)) 
        Calculate_PCA_2(result, vp)




    def show_sensor(self, state, sensor):
        if state:
            self.showsensor[sensor] = True
        else:
            self.showsensor[sensor] = False

        self.update_plot()

    def show_details(self):
        if self.showdetails:
            self.showdetails = False
        else:
            self.showdetails = True

        for key, tab in self.tabs.items():
            for sensorlabel in self.sensorlabels:
                if self.showdetails:
                    self.sensorLabel[key][sensorlabel].hide()
                else:
                    self.sensorLabel[key][sensorlabel].show()

            if self.showdetails:
                self.detailsButton[key].setText("Edit sensors")
                self.detailsButton[key].setStatusTip('Edit visible sensors')
            else:
                self.detailsButton[key].setText("Show details")
                self.detailsButton[key].setStatusTip('Show further test details')
        if self.data != {}:
            self.update_plot()

    def show_pca(self):
        pen = self.tabWidget.currentWidget().pen
        day = self.tabDaySpin[pen].value()
        if day < 1:
            day = 'water'
        repeat = self.tabRepeatSpin[pen].value()

        pca = Calculate_PCA(self.data[pen][day][repeat])


    def slider_change(self):
        val = self.sender().value()
        pen = self.tabWidget.currentWidget().pen
        if self.avg:
            day, repeat = [self.avgvals[pen][val], 'avg']
        else:
            day, repeat = self.vals[pen][val]
            self.tabRepeatSpin[pen].setValue(repeat)
            self.tabRepeatSpin[pen].setRange(self.min_repeats[pen][day], self.max_repeats[pen][day])

        #print('Slider calculated day:{0}, repeat:{1}'.format(day, repeat))

        if day == 'water':
            temp = -1
        else:
            temp = day
        self.tabDaySpin[pen].setValue(temp)
        self.update_plot(pen, day, repeat)


    def day_spin_change(self):
        day = self.sender().value()
        if day < 1:
            day = 'water'
        #print('Day Spinbox value: ' + str(day))
        pen = self.tabWidget.currentWidget().pen

        if self.avg:
            val = self.avgvals[pen].index(day)
            self.tabSliders[pen].setValue(val)
        else:
            repeat = self.tabRepeatSpin[pen].value()
            if self.min_repeats[pen].get(day) and self.max_repeats[pen].get(day):
                self.tabRepeatSpin[pen].setRange(self.min_repeats[pen][day], self.max_repeats[pen][day])
            try:
                val = self.vals[pen].index([day, repeat])
                self.tabSliders[pen].setValue(val)
            except ValueError:
                pass

    def repeat_spin_change(self):
        if not self.avg:
            repeat = self.sender().value()
            pen = self.tabWidget.currentWidget().pen
            day = self.tabDaySpin[pen].value()
            try:
                val = self.vals[pen].index([day, repeat])
                self.tabSliders[pen].setValue(val)
            except ValueError:
                pass


    def update_plot(self, pen=None, day=None, repeat=None):
        if pen == None:
            pen = self.tabWidget.currentWidget().pen
        if day == None:
            day = self.tabDaySpin[pen].value()
            if day < 1:
                day = 'water'
        if repeat == None:
            if self.avg:
                repeat = 'avg'
            else:
                repeat = self.tabRepeatSpin[pen].value()

        if repeat == 'avg':
            avg = True
            test = self.avgdata[pen][day][repeat]
        else:
            avg = False
            test = self.data[pen][day][repeat]


        text = f"Test: {test.name}\n"
        if avg:
            text += f"Date: {test.date}\nRepeat: Average\n\n"
        else:
            text += f"Time & Date: {test.time} {test.date}\n"
            text += f"Repeat: {test.repeats[0]}/{test.repeats[1]}\n\n"

        if self.showdetails:
            #text += "Details:\n"
            text += ''.join(test.details)
            text += f"\nBaseline: {test.baseline}\n"
            text += f"Absorb: {test.absorb}\nPause: {test.pause}\nDesorb: {test.desorb}\n"
            text += f"Flush: {test.flush}\nWait: {test.wait}\nHigh Flow: {test.hflow}\n"
            text += f"Medium Flow: {test.mflow}\nLow Flow: {test.lflow}\n\nProfile Time: {test.profiletime}\n"
            text += f"Data Rate: {test.datarate}\nData Total: {test.datatotal}\nNumber of Sensors: {test.sensors}\n"
            if day == 'water':
                age = 28
            else:
                age = test.day + 28

            text += f"Pig's Age: {age} days old\nTreatment/Vaccine: {test.vacprot}"
            #text += f"Max Gradient {test.max_gradient}\n Baseline Return Point: {test.bl_return_point}"

        self.tabLabel[pen].setText(text)
        self.tabPlot[pen].update_plot(test, self.showsensor,
            self.annotate, self.showwait, self.showdetails, self.shownorm)

        #self.tabPlot[pen].savefigure()

    def retranslateUi(self):
        ''
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "VOC Tool"))

        for key, tab in self.tabs.items():
            self.tabWidget.setTabText(self.tabWidget.indexOf(tab), _translate("MainWindow", (key)))
        
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.menuWindow.setTitle(_translate("MainWindow", "Window"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.menuView.setTitle(_translate("MainWindow", "View"))

        self.actionOpen.setText(_translate("MainWindow", "Import file(s)..."))
        self.actionOpen.setToolTip(_translate("MainWindow", "Open a .txt or .zip file."))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))

        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))

        self.actionMinimise.setText(_translate("MainWindow", "Minimize"))
        self.actionMinimise.setShortcut(_translate("MainWindow", "Ctrl+M"))

        self.actionAnnotate.setText(_translate("MainWindow", "Annotate Graph"))
        self.actionAnnotate.setShortcut(_translate("MainWindow", "Ctrl+A"))

        self.actionShowwait.setText(_translate("MainWindow", "Show Wait Period"))

        self.actionAverage.setText(_translate("MainWindow", "Average Repeats"))

        self.actionNorm.setText(_translate("MainWindow", "Standardize Data"))

        #self.actionExport_to_excel.setText(_translate("MainWindow", "Export to Excel (WIP)"))
        self.actionDelete_all_imports.setText(_translate("MainWindow", "Delete Imported Data"))

        self.actionPreferences.setText(_translate("MainWindow", "Preferences..."))
        self.actionPreferences.setShortcut(_translate("MainWindow", "Ctrl+P"))

        self.actionOpen_folder.setText(_translate("MainWindow", "Import folder..."))
        self.actionOpen_folder.setShortcut(_translate("MainWindow", "Ctrl+Shift+O"))

        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionHelp.setShortcut(_translate("MainWindow", "Ctrl+?"))

        self.actionLicense.setText(_translate("MainWindow", "About"))

    def openfile(self):
        self.statusbar.showMessage('Importing file(s)...')
        fname = QtWidgets.QFileDialog.getOpenFileNames(
            self, 
            'Select file(s)', 
            "", 
            "Data files (*.txt *.zip)",
        )
        if not fname[0]:
            self.statusbar.showMessage('')
            return

        self.recalculate_average = open_files(fname[0])

        #self.close()
        self.__init__()
        self.show()

    def openfolder(self):
        self.statusbar.showMessage('Importing file(s)...')
        folder = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select folder')
        if not folder:
            self.statusbar.showMessage('')
            return

        folder += '/'
        fnames = os.listdir(folder)
        longfnames = [folder + file for file in fnames]

        self.recalculate_average = open_files(longfnames)

        #self.close()
        self.__init__()
        self.show()


    def deleteimports(self):
        text = f"Are you sure you want to continue and remove all imported data?\nThis includes {len(os.listdir('data'))} data files."
        msg = QtWidgets.QMessageBox(text=text, parent=self)
        msg.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.Cancel)
        msg.buttonClicked.connect(self.output)
        ret = msg.exec()

    def output(self, button):
        if button.text() == '&Yes':
            files = os.listdir('data')
            for file in files:
                file = 'data/' + file
                if os.path.isfile(file):
                    os.remove(file)

            msg = QtWidgets.QMessageBox(text="Data files deleted successfully.", parent=self)
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            ret2 = msg.exec()

            self.data = {}
            self.avgdata = {}
            self.recalculate_average = None
            #self.close()
            self.__init__()
            self.show()

    def show_wait(self, action):
        self.showwait = action
        self.update_plot()

    def show_annotate(self, action):
        self.annotate = action
        self.update_plot()

    def show_norm(self, action):
        self.shownorm = action
        self.update_plot()

    def show_avg(self, action):
        if action:
            self.avg = True
        else:
            self.avg = False

        for key, tab in self.tabs.items():
            self.tabRepeatSpin[key].setReadOnly(self.avg)
            self.tabSliders[key].setValue(0) 
            if self.avg:
                self.tabRepeatSpin[key].hide()
                self.tabSliders[key].setRange(0, (len(self.avgdata[key])-1))

            else:
                self.tabRepeatSpin[key].show()
                self.tabRepeatSpin[key].setValue(self.min_repeats[key][self.vals[key][0][0]]) 
                self.tabRepeatSpin[key].setRange(self.min_repeats[key][self.vals[key][0][0]], self.max_repeats[key][self.vals[key][0][0]])
                self.tabSliders[key].setRange(0, (len(self.vals[key])-1))
        self.update_plot()

class AnalyseWindow(QtWidgets.QWidget):
    """

    Window for confirming analyse and allow configuration of settings before analysing.

    """

    def __init__(self):
        super().__init__()

        win.analyseConfig = None


        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)

        self.firstRepeatCheckbox = QtWidgets.QCheckBox("  Do not include first\n  repeat in test", self)
        self.firstRepeatCheckbox.setGeometry(QtCore.QRect(20, 110, 180, 50))
        self.firstRepeatCheckbox.setChecked(True)

        self.setWindowTitle("VOC Tool: Anaylse data")
        size = [200, 190]
        self.resize(size[0], size[1])
        self.setFixedSize(size[0], size[1])
        self.setWindowIcon(QtGui.QIcon('logo.png'))

        self.descriptorLabel = QtWidgets.QLabel("Descriptor Type:", self)
        self.descriptorLabel.setGeometry(QtCore.QRect(20, 10, 180, 25))

        self.descriptorCombobox = QtWidgets.QComboBox(self)
        self.descriptorCombobox.setGeometry(QtCore.QRect(20, 32, 160, 25))
        self.descriptorCombobox.addItems(['Amplitude', 'Decay Value', 'Time to return to baseline', 'Maximum gradient', 'Amplitude - baseline'])

        self.confirmButton = QtWidgets.QPushButton("Analyse Data", self)
        self.confirmButton.setGeometry(QtCore.QRect(20, 160, 160, 25))
        self.confirmButton.clicked.connect(self.confirm)

        self.sensorLabel = QtWidgets.QLabel("Sensors used:", self)
        self.sensorLabel.setGeometry(QtCore.QRect(20, 58, 180, 25))

        self.sensorCombobox = QtWidgets.QComboBox(self)
        self.sensorCombobox.setGeometry(QtCore.QRect(20, 80, 160, 25))
        self.sensorCombobox.addItems(['Visible sensors', 'All sensors'])

    def confirm(self):
        options = []

        options.append(str(self.descriptorCombobox.currentText()))

        if str(self.sensorCombobox.currentText()) == 'All sensors':
            options.append(True)
        else:
            options.append(False)

        options.append(self.firstRepeatCheckbox.isChecked())

        #print(options)

        self.close()
        win.Display_PCA(options)











if __name__ == "__main__":
    main()
