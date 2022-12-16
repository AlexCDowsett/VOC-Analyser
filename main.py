import tkinter as tk # Imports the tkinter module. Any functions from this module will be start with a 'tk.' to show what module it came from.
import tkinter.ttk as ttk
from tkinter import filedialog as fd
import random
from openfile import Open
from zipfile import ZipFile
import pickle
import os


root = tk.Tk()

def openfiles():
    
    files = list(fd.askopenfilenames(filetypes = (("Data files", '*.txt;*.zip'),)))

    remove = []

    for i in range(len(files)):
    
        if files[i].endswith('.zip'):
            with ZipFile(files[i], 'r') as zip:

                temp = zip.namelist()
            
                files += ['temp/' + x for x in temp]
            
                #print('Extracting all the files now from ' + files[0])
            
                zip.extractall(path ='temp/')
            
                #zip.printdir()
            
                #print('Done!')

            remove.append(i)

    for i in range(len(remove)):
        del files[remove[len(remove)-i-1]]

    #print(files)


    data_objects = []
    for i in range(len(files)):
        data_objects.append(Open(files[i]))
        print("Opening " + files[i])
        data_objects[i].dump()


def openfolder():
    ''


def load():

    if not os.path.exists('data'): 
        return False

    files = os.listdir('data')
    data = {}
    for i in range(len(files)):
        if files[i].endswith('.data'):
            temp = open(('data/' + files[i]), 'rb')
            file = pickle.load(temp)

            new_room = True
            keys = list(data.keys())
            for j in range(len(data)):
                if keys[j] == file.smartname:
                    new_room = False
                    break

            if new_room == True:
                data[file.smartname] = {}
                data[file.smartname][file.day] = {}

            else:
                new_day = True
                keys = list(data[file.smartname].keys())
                for j in range(len(data[file.smartname])):
                    if keys[j] == file.day:
                        new_day = False
                        break

                if new_day == True:
                    data[file.smartname][file.day] = {}

            data[file.smartname][file.day][file.repeats[0]] = file

    print(list(data['Pen 6A'].keys()))
    #print(data['Pen 6A'])
    #print(list(data['Pen 6A'].values()))
    #for i in range(len(data['Pen 6A'])):
    #    print(list(data['Pen 6A'].values())[i].day)


    print(data['Pen 6A']['water'][3].data[0][1])

    l = tk.Label(root, text = data['Pen 6A']['water'][3].data[0][1])
    l.place(x=10, y=100, w=200, h=80)

    return True





button = tk.Button(root, text='Files', command=openfiles)
button.place(x=10, y=10, w=50, h=50)

button2 = tk.Button(root, text='Load', command=load)
button2.place(x=80, y=10, w=50, h=50)






root.mainloop()
