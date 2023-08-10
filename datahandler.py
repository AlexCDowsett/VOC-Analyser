import pickle
import os
import re
from zipfile import ZipFile
import pandas as pd
import numpy as np


class Open:
    def __init__(self, file=None, data=None):
        self.error = False

        if file == None and data != None:

            data = list(data)
            filename = data[0][1].filename
            filename1 = re.split("day", filename, flags=re.IGNORECASE, maxsplit=1)
            if len(filename1) == 1:
                filename2 = filename1[0].split("_", 1)
                self.filename = filename2[0] + '_average'
            else:
                filename2 = filename1[1].split("_", 1)
                if len(filename2) != 1:
                    self.filename = filename1[0] + 'Day' + filename2[0] + '_average'
                else:
                    self.filename = filename + '_average'

            self.details = data[0][1].details
            self.date = data[0][1].date
            self.time = None
            self.name = data[0][1].name
            self.smartname = data[0][1].smartname
            self.day = data[0][1].day
            self.room = data[0][1].room
            self.repeats = ['avg', data[0][1].repeats[1]]
            self.baseline = data[0][1].baseline
            self.absorb = data[0][1].absorb
            self.pause = data[0][1].pause
            self.desorb = data[0][1].desorb
            self.flush = data[0][1].flush
            self.wait = data[0][1].wait
            self.hflow = data[0][1].hflow
            self.mflow = data[0][1].mflow
            self.lflow = data[0][1].lflow
            self.profiletime = data[0][1].profiletime
            self.datarate = data[0][1].datarate
            self.datatotal = data[0][1].datatotal
            self.sensors = data[0][1].sensors
            self.triggers = data[0][1].triggers
            self.vacprot = data[0][1].vacprot

            self.data = [[0.0 for x in range(len(data[0][1].data[0]))] for y in range(len(data[0][1].data))] 
            for x in range(len(self.data)):
                for y in range(len(self.data[0])):
                    sum_ = 0.0
                    for i in range(len(data)):
                        sum_ += data[i][1].data[x][y]
                    self.data[x][y] = sum_ / (i+1)

            self.create_data_frame()


        else:
            try:
                f = open(file, 'r')
                lines = f.readlines()
                f.close()
                file = file.split('.')
                file.pop()
                file = '.'.join(file)

                file = file.split('/')
                self.filename = file.pop()


                self.read(lines)
            except FileNotFoundError as e:
                self.error = True

    def read(self, lines): 

        if re.search('Test', self.filename):
                print('Sampler test')
                self.sampler = True

        line = 1
        self.details = []
        while not lines[line].startswith('---'):
            self.details.append(lines[line])
            line += 1
   
        self.date = lines[line+1][7:17]
        self.time = lines[line+2][7:15]

        self.name = lines[line+5][25:].replace('"', '').replace('\n', '')

        temp = re.split("day", self.name, flags=re.IGNORECASE)



        self.smartname = temp[0].replace('_', ' ').strip()
        if len(temp) > 1:
            self.day = int(temp[1])
        elif self.smartname == 'Water end':
            self.day = 'water'
            self.smartname = 'Pen3A 60'

        elif self.smartname == 'water f':
            self.day = 'water'
            self.smartname = 'Pen5a60'
        elif self.smartname == 'water d': 
            self.day = 'water'
            self.smartname = 'Pen 6A'
        elif 'water' in temp[0].casefold():
            temp2 = re.split("water", temp[0], flags=re.IGNORECASE)
            if len(temp2) > 1:
                if int(temp2[1]) == 1:
                    self.day = -2
                if int(temp2[1]) == 2:
                    self.day = -1
                if int(temp2[1]) == 3:
                    self.day = 0
            else:
                self.day = -999
        else:
            self.day = -999

        if 'pen' in self.smartname.casefold():
            temp = re.split("pen", self.smartname, flags=re.IGNORECASE)
        else:
            temp = re.split("room", self.smartname, flags=re.IGNORECASE)

        self.room = int(temp[1].strip()[0])

        self.repeats = [int(lines[line+7][13]), int(lines[line+7][15])]
        self.baseline = float(lines[line+11][11:])
        self.absorb = float(lines[line+12][9:])
        self.pause = float(lines[line+13][8:])
        self.desorb = float(lines[line+14][9:])
        self.flush = float(lines[line+15][8:])
        self.wait = float(lines[line+16][7:])
        self.hflow = float(lines[line+17][18:])
        self.mflow = float(lines[line+18][18:])
        self.lflow = float(lines[line+19][15:])

        y = 0
        try:
            self.profiletime = int(lines[line+21][21:23])
        except ValueError:
            y = 1
            line += 11
            self.profiletime = int(lines[line+21][21:23])

        self.datarate = int(lines[line+23][33:])
        self.datatotal = int(lines[line+25][(27-y):])
        self.sensors = int(lines[line+27][31:33])

        self.triggers = [0.0, self.baseline, self.absorb, self.pause, self.desorb, self.flush, self.wait]
        time = 0
        for i in range(len(self.triggers)):
            time += (self.triggers[i]) * self.datarate
            self.triggers[i] = time
        line += 31
        self.data = []
        while not line == len(lines):
            strs = lines[line].split()
            #floats = [float(val) for val in strs]
            floats = []
            for val in strs:
                temp = float(val)
                if temp > 9999 or temp < -9999:
                    temp = 0.0
                floats.append(temp)
            self.data.append(floats[1:9999])

            line += 1

        if self.smartname == 'Pen2A 60' or 'Room 2':
            order = ['Saline', 'Lawsonia', 'Circoflex']

        elif self.smartname == 'Pen3A 60' or 'Room 3':
            ''

        elif self.smartname == 'Pen5a60' or 'Room 5':
            order = ['Lawsonia', 'Circoflex', 'Saline']

        elif self.smartname == 'Pen 6A' or 'Room 6':
            order = ['Circoflex', 'Saline', 'Lawsonia']

        else:
            print('Warning: Failed to allocating vaccine protocol (1).')
            self.vacprot = 'N/A'
            self.create_data_frame()
            return

        if self.day == 'water':
            self.vacprot = 'Water Removed' 

        elif (self.day <= 4) | (self.smartname == 'Pen3A 60' or self.smartname == 'Room 3'):
            self.vacprot = 'No treatment'

        elif self.day <= 11:
            self.vacprot = order[0] + '+' + str(self.day-5)

        elif self.day <= 18:
            self.vacprot = order[1] + '+' + str(self.day-12)

        elif self.day <= 24:
            self.vacprot = order[2]  + '+' + str(self.day-19)
        else:
            print('Warning: Failed to allocating vaccine protocol (2).')
            self.vacprot = 'N/A'


        self.create_data_frame()




        #import matplotlib.pyplot as plt
        #Fs = 250
        #tstep = 1 / Fs

        #humidity = self.dataframe['Humidity']

        #print(humidity)
        #n = len(humidity)



        #t = np.linspace(0, (n-1)*tstep, n)
        #fstep = Fs / n
        #f = np.linspace(0, (n-1)*fstep, n)

        #humidity = 1 * np.sin(2* np.pi * f0 * t)

        #x = np.fft.fft(humidity)
        #xmag = np.abs(x) / n

        #f_plot = f[0:int(n/2+1)]
        #xmagplot = 2 * xmag[0:int(n/2+1)]
        #xmagplot[0] = 0#xmagplot[0] /2

        #fig, [ax1, ax2] = plt.subplots(nrows=2, ncols=1)
        #ax1.plot(t, humidity, '.-')
        #ax2.plot(f_plot, xmagplot, '.-')
        #plt.show()


    def create_data_frame(self):

        self.timelabels = [x for x in range(0, len(self.data))]
        self.sensorlabels = ['Sen-' + str(x) for x in range(1, len(self.data[0]))]
        self.sensorlabels.append('Humidity')

        self.dataframe = pd.DataFrame(self.data, columns=self.sensorlabels, index=self.timelabels)

        for i in self.dataframe.index:
            self.dataframe.loc[i] = self.data[i]

        self.dataframe = self.dataframe.replace(0, np.NaN)

        baseline = range(round(self.triggers[0]), round(self.triggers[1]))
        baseline_values = []
        for index in baseline:
            baseline_values.append(list(self.dataframe.iloc[index]))

        from scipy.optimize import curve_fit
        self.decaya = {}
        self.decayb = {}
        for label in self.sensorlabels:
            df = self.dataframe[label][round(self.triggers[4]):round(self.triggers[5])]
            df = df.dropna()
            try:
                (a, b), *_ = curve_fit(self.model, range(0, len(df)), df.values / df.values.max())

                a *= df.values.max()

                self.decaya[label] = a
                self.decayb[label] = b
            except ValueError:
                pass


        #print(self.decay)

        self.max_gradient = [(self.dataframe[l] / self.dataframe[l].shift(-1)).sort_values(ascending = False).iloc[0] for l in self.sensorlabels]
        #print(self.max_gradient)

        #print(baseline_values)
        average = []
        for i in zip(*baseline_values):
            sum_ = 0
            count = 0
            for v in i:
                if not np.isnan(v):
                    sum_ += v
                    count += 1
            average.append(sum_ / count)
        self.normdf = self.dataframe.sub(average, axis='columns')
        self.bl_average = dict(zip(self.sensorlabels, average))
        self.bl_return_point = {}
        self.ampbl = []
        k = 2
        for label in self.sensorlabels:
            df = self.dataframe[label].between(self.bl_average[label]-k, self.bl_average[label]+k)
            
            for i in range(round(self.triggers[3]), round(self.triggers[5])-2):
                self.bl_return_point[label] = round(self.triggers[5])
                try:
                    if df[i] and df[i+1] and df[i+2] and df[i+3] and df[i+4]:
                        self.bl_return_point[label] = self.dataframe[label].index[i]
                        break
                except KeyError:
                    break
        self.amplitude = []
        for label in self.sensorlabels:
            df = self.dataframe[label][round(self.triggers[2])+1:round(self.triggers[3])]
            self.amplitude.append(df.mean(axis=0))
        
        for i in range(len(self.amplitude)):
            self.ampbl.append(self.amplitude[i] - list(self.bl_average.values())[i])



    def model(self, t, a, b):
        return a * np.exp(-b * t)

    def dump(self):

        if not os.path.exists('data'): 
            os.mkdir('data') 


        file = open('data/' + self.filename + '.data', 'wb')
        pickle.dump(self, file)
        file.close()
            
            
          


def open_files(files):
    if files == []:
        return


    for i in range(len(files)):
    
        if files[i].endswith('.zip'):
            with ZipFile(files[i], 'r') as zip:

                temp = zip.namelist()
            
                files += ['temp/' + x for x in temp]
            
                #print('Extracting all the files now from ' + files[0])
            
                zip.extractall(path ='temp/')
            
                #zip.printdir()
            
                #print('Done!')

    #print(files)

    recalculate_average = []


    for i in range(len(files)):

        #if re.search('Sampler|Test', files[i]):
        #    print('Sampler test')

        if files[i].endswith('.txt'):
            print("Opening " + files[i])
            f = Open(files[i])
            if not recalculate_average.count([f.smartname, f.day]):
                recalculate_average.append([f.smartname, f.day])
            f.dump()





    for file in files:
        if file.startswith('temp/') and os.path.isfile(file):
            os.remove(file)

    if os.path.isdir('temp') and not os.listdir('temp'):
        os.rmdir('temp')

    return recalculate_average

def load(avg=False):

    if not os.path.exists('data'): 
        return {}

    files = os.listdir('data')
    data = {}

    for i in range(len(files)):
        if 'Test' in files[i]:
            break
        if ((not avg and files[i].endswith('.data') and not files[i].endswith('average.data')) or (avg and files[i].endswith('average.data'))):
            temp = open(('data/' + files[i]), 'rb')
            file = pickle.load(temp)

            new_room = True
            keys = list(data.keys())
            for j in range(len(data)):
                if keys[j] == file.smartname:
                    new_room = False
                    break

            if new_room:
                data[file.smartname] = {}
                data[file.smartname][file.day] = {}

            else:
                new_day = True
                keys = list(data[file.smartname].keys())
                for j in range(len(data[file.smartname])):
                    if keys[j] == file.day:
                        new_day = False
                        break

                if new_day:
                    data[file.smartname][file.day] = {}

            data[file.smartname][file.day][file.repeats[0]] = file
            #print(data[file.smartname][file.day][file.repeats[0]].smartname + ', ' + str(data[file.smartname][file.day][file.repeats[0]].day) + ', ' + str(data[file.smartname][file.day][file.repeats[0]].repeats[0]))

    return data       

def avgload(data, recalculate_average):
    if recalculate_average != None:

        for keys in recalculate_average:
            pen = keys[0]
            day = keys[1]
            f = Open(data=data[pen][day].items())
            f.dump()

    avgdata = load(avg=True)
    return avgdata



def main():

    test_filename = 'Room 2 Day 1 31-10-2022 09.43.17 Repeat 1 Test'
    #test_filename = 'Room 2 Water 1 31-10-2022 09.14.59 Repeat 1 Test'

    test = Open(test_filename + '.txt')
    if test.error == True:
        print("FileNotFoundError")
    test.dump()

    file = open('data/' + test_filename + '.data', 'rb')
    data = pickle.load(file)
    file.close()
    #print(vars(data))
    #print(data.triggers)

    file = open('data/' + 'Pen2A 60 Day 1_15_05_46.44.data', 'rb')
    data = pickle.load(file)
    file.close()
    #print(vars(data))
    #print(data.triggers)


    #print('\n\n------------AVERAGE---------------\n\n')
    #file = open('data/Room 2 Day 1 31-10-2022 09.43.17 Repeat 1.data', 'rb')
    #data = pickle.load(file)
    #file.close()
    #print(vars(data))

    #print(data.data)



if __name__ == '__main__':
    main()
