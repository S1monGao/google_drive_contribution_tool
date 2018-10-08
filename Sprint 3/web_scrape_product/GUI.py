from tkinter import *

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


#Time boxes
Label(window, text="Time", height=3, bg="grey39", fg="white", font="none 12 bold", width=80).grid(row=2,column=0,columnspan=5,sticky=S)

time1=Entry(window, width=20, bg="white")
time1.grid(row=3, column=1, sticky=E)

time2=Entry(window, width=20, bg="white")
time2.grid(row=3, column=3, sticky=W)


#nothing
Label(window, text="",bg="grey39", fg="white", font="none 12 bold", width=80).grid(row=4,column=0,columnspan=5)

#generate button
def click():
    #generate function goes here
    return

Button(window,text="Generate",width=20, command=click).grid(row=5,column=2)


window.mainloop()

