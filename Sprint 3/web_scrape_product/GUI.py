from tkinter import *

#make window
window = Tk()

window.title("We Showed up")
window.pack_propagate(False)
window.grid_propagate(False)
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.configure(width=screen_width,height=screen_height, bg="grey39")

Label(window, text="File selector",  bg="grey23", fg="white", font="none 12 bold").grid(row=1,column=2)

fileList=Listbox(window,width =60)

fileList.pack()


window.mainloop()

