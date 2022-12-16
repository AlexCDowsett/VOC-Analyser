import pickle
import os
import re

class Open:
    def __init__(self, file):
        self.error = False
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
        else:
            self.day = -1

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
        self.profiletime = int(lines[line+21][21:23])
        self.datarate = int(lines[line+23][33:])
        self.datatotal = int(lines[line+25][27:])
        self.sensors = int(lines[line+27][31:33])

        line += 31
        self.data = []
        while not line == len(lines):
            self.data.append(lines[line].split())
            line += 1



    def dump(self):

        if not os.path.exists('data'): 
            os.mkdir('data') 


        file = open('data/' + self.filename + '.data', 'wb')
        pickle.dump(self, file)
        file.close()
            
            
            
            


def main():
    test = Open('test.txt')

    if test.error == True:
        return
    

    test.dump()

    file = open('data/test.data', 'rb')
    data = pickle.load(file)
    file.close()
    #print(vars(data))



if __name__ == '__main__':
    main()
