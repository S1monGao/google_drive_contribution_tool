from tkinter import *
import datetime as dt

def checkTime(start_time,end_time):
    try:
        start_time = dt.datetime.strptime(start_time, '%d/%m/%Y')
        end_time = dt.datetime.strptime(end_time, '%d/%m/%Y')
    except ValueError:
        output.delete(0.0, END)
        output.insert(END,'Times are not of form dd/mm/yy')
        return

    if end_time<start_time:
        output.delete(0.0, END)
        output.insert(END,'End time is less than start time')
        return

def click():
    checkTime(time1.get(),time2.get())
    return

error_message=''


#Window
window = Tk()
window.title("We Showed up")
window.resizable(False, False)
window.grid_propagate(False)
#screen_width = window.winfo_screenwidth()
#screen_height = window.winfo_screenheight()
window.configure(width=800,height=3000, bg="grey39")

#Heading
Label(window, text="File selector",  bg="grey39", fg="white", font="none 12 bold", width=80).grid(row=0,column=0, columnspan=5)

#file selector
fileList=Listbox(window, width=100, height=35)
fileList.grid(row=1, column=0, columnspan=5)
fileList.insert(END,"Drive","   Folder","      File")


#Time boxes
Label(window, text="Time (dd/mm/yyyy)", height=3, bg="grey39", fg="white", font="none 12 bold", width=80).grid(row=2,column=0,columnspan=5,sticky=S)

time1=Entry(window, width=20, bg="white")
time1.grid(row=3, column=1, sticky=E)

time2=Entry(window, width=20, bg="white")
time2.grid(row=3, column=3, sticky=W)


#nothing
Label(window, text="",bg="grey39", fg="white", font="none 12 bold", width=80).grid(row=4,column=0,columnspan=5)

#generate button


Button(window,text="Generate",width=20, command=click).grid(row=5,column=2)

#nothing
Label(window, text="",bg="grey39", fg="white", font="none 12 bold", width=80).grid(row=6,column=0,columnspan=5)

#Error output
output = Text(window, bg="grey39", fg="red", font="none 12 bold", width=80, height=1, bd=0)
output.grid(row=7,column=0,columnspan=5)
window.mainloop()

