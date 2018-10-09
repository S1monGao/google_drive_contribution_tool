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
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print ('You selected item ',index,": ",value)


def folderOnselect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print ('You selected item ',index,": ",value)

def fileOnselect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    print ('You selected item ',index,": ",value)
    value=value.split(', ')
    global chosenFiles
    chosenFiles= [(value[0],value[1])]
    print(chosenFiles[0][0])
    print(chosenFiles[0][1])


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

#Window
window = Tk()
window.title("We Showed up")
window.resizable(False, False)
window.grid_propagate(False)
#screen_width = window.winfo_screenwidth()
#screen_height = window.winfo_screenheight()
window.configure(width=800,height=3000, bg="grey39")


Label(window, text="Team Drive Selector",  bg="grey39", fg="white", font="none 12 bold", width=80).grid(row=0,column=0, columnspan=5)


teamList=Listbox(window, width=100, height=10)
teamList.grid(row=1, column=0, columnspan=5)
for i in range(100):
    teamList.insert(END, 'Team',i)
teamList.bind('<<ListboxSelect>>', teamOnselect)

Label(window, text="Folder Selector",  bg="grey39", fg="white", font="none 12 bold", width=80).grid(row=2,column=0, columnspan=5)


folderList=Listbox(window, width=100, height=10)
folderList.grid(row=3, column=0, columnspan=5)
folderList.insert(END,"Folder")
folderList.bind('<<ListboxSelect>>', folderOnselect)


Label(window, text="File Selector",  bg="grey39", fg="white", font="none 12 bold", width=80).grid(row=4,column=0, columnspan=5)


fileList=Listbox(window, width=100, height=10)
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


Button(window,text="Generate",width=20, command=click).grid(row=90,column=2)

#nothing
Label(window, text="",bg="grey39", fg="white", font="none 12 bold", width=80).grid(row=11,column=0,columnspan=5)

#Error output
output = Text(window, bg="grey39", fg="red", font="none 12 bold", width=80, height=1, bd=0)
output.grid(row=11,column=0,columnspan=5)
window.mainloop()

