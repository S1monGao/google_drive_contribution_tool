from tkinter import *
from apiNavigation import *
from main_file import *
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from ast import literal_eval
from classes import User, Edit
from plotting_functions import plot_pie_chart, plot_lines, save_all_plots
import time
import datetime as dt
import platform
from pdf_report import generate_pdf_report, generate_pdf_report2




def teamOnselect(evt):
    selection = evt.widget
    index = int(selection.curselection()[0])
    value = selection.get(index)
    value = value.split(', ')
    global currentChoice
    currentChoice=value

def teamSelect():
    value=currentChoice
    filesSelected = listAllFilesInTeamDrive(service, value[1])
    global chosenFiles
    chosenFiles = []
    chosenFiles = convertFilesToUrls(filesSelected, service)
    folderList.delete(0,END)
    folders=listFoldersInTeamDrive(service, value[1])
    for i in folders:
        folderList.insert(END,i[0]+", "+i[1])


def folderOnselect(evt):
    selection = evt.widget
    index = int(selection.curselection()[0])
    value = selection.get(index)
    global currentChoice
    currentChoice = value

def folderSelect():
    value = currentChoice
    filesSelected = getFilesInFolder(value[1], service)
    global chosenFiles
    chosenFiles = []
    chosenFiles = convertFilesToUrls(filesSelected, service)
    fileList.delete(0, END)
    for i in chosenFiles:
        folderList.insert(END, i[0] + ", " + i[1])


def fileOnselect(evt):
    selection = evt.widget
    index = int(selection.curselection()[0])
    value = selection.get(index)
    value=value.split(', ')
    global currentChoice
    currentChoice = value

def fileSelect():
    global currentChoice
    value = currentChoice
    global chosenFiles
    chosenFiles = [(value[0], value[1])]

def click():
    try:
        start_time = dt.datetime.strptime(time1.get(), '%d/%m/%Y')
        end_time = dt.datetime.strptime(time2.get(), '%d/%m/%Y')
    except ValueError:
        output.delete(0.0, END)
        output.insert(END,'Times are not of form dd/mm/yy')
        return

    if end_time<start_time:
        output.delete(0.0, END)
        output.insert(END,'End time is less than start time')
        return





    print(chosenFiles)


    generate_all(chosenFiles,dt.datetime.strptime(time1.get(), '%d/%m/%Y'),dt.datetime.strptime(time2.get(), '%d/%m/%Y'))

    return


chosenFiles=[]
service = authenticate()
currentChoice=''

#Window
window = Tk()
window.title("We Showed up")
window.resizable(False, False)
window.grid_propagate(False)
window.pack_propagate(False)
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.configure(width=800,height=screen_height-75, bg="grey39")

#frame=Frame(window,width=800,height=screen_height,bg="grey39",bd=0)
#canvas=Canvas(frame,width=800,height=screen_height,scrollregion=(0,0,800,3000),bg="grey39",bd=0)
#scrollbar = Scrollbar(window,orient=VERTICAL)
#scrollbar.config(command=canvas.yview)
#scrollbar.pack(side="right", fill="y", expand=False)
#scrollbar.grid(row=1,column=4,sticky=NE)

#canvas.configure(yscrollcommand=scrollbar.set)

Label(window, text="Team Drive Selector",  bg="grey39", fg="white", font="none 12 bold", width=80).grid(row=0,column=0, columnspan=5)


teamList=Listbox(window, width=100, height=5)
teamList.grid(row=1, column=0, columnspan=5)
teams=listTeamDrives(service)
for i in teams:
    teamList.insert(END,i[0]+", "+i[1])
teamList.bind('<<ListboxSelect>>', teamOnselect)
Label(window, text="Folder Selector",  bg="grey39", fg="white", font="none 12 bold", width=80).grid(row=2,column=0, columnspan=5)


folderList=Listbox(window, width=100, height=5)
folderList.grid(row=3, column=0, columnspan=5)
folderList.insert(END,"Folder")
folderList.bind('<<ListboxSelect>>', folderOnselect)


Label(window, text="File Selector",  bg="grey39", fg="white", font="none 12 bold", width=80).grid(row=4,column=0, columnspan=5)


fileList=Listbox(window, width=100, height=5)
fileList.grid(row=5, column=0, columnspan=5)
fileList.insert(END,"test_doc2, https://docs.google.com/document/d/1QnSjI74Gwx-QsVc7Atm0Q0Dp5T31NOmNZ3xZVAX6HBI/edit")
fileList.bind('<<ListboxSelect>>', fileOnselect)





#Time boxes
Label(window, text="Time (dd/mm/yyyy)", height=3, bg="grey39", fg="white", font="none 12 bold", width=80).grid(row=6,column=0,columnspan=5,sticky=S)

time1=Entry(window, width=20, bg="white")
time1.grid(row=7, column=1, sticky=E)

time2=Entry(window, width=20, bg="white")
time2.grid(row=7, column=3, sticky=W)


#nothing
Label(window, text="",bg="grey39", fg="white", font="none 12 bold", width=80).grid(row=8,column=0,columnspan=5)

#generate button


Button(window,text="Generate",width=20, command=click).grid(row=9,column=2)

#nothing
Label(window, text="",bg="grey39", fg="white", font="none 12 bold", width=80).grid(row=11,column=0,columnspan=5)

#Error output
output = Text(window, bg="grey39", fg="red", font="none 12 bold", width=80, height=1, bd=0)
output.grid(row=11,column=0,columnspan=5)


Button(window,text="Select Team Drive",width=20, command=teamSelect).grid(row=12,column=1)
Button(window,text="Select Folder",width=20, command=folderSelect).grid(row=12,column=2)
Button(window,text="Select File",width=20, command=fileSelect).grid(row=12,column=3)
#window.pack()
#frame.pack()
window.mainloop()




