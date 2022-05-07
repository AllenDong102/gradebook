from tkinter import * #tkinter is the main GUI library used in this app
from createClassWindow import * #Each button on homescreen goes to a different file
from accessClassesWindow import *

def mainMenuSetup(window):
    window.minsize(400,300)
    window.title("Gradebook")
    window.config(background="white")
    #Used to position the buttons
    homeFrame = Frame(window) 

    #Buttons, one creates a new class, other access old class
    newClass = Button(homeFrame, text = "Create New Class", \
                      command=lambda:classInfoSetup(window,homeFrame),\
                      width=20,\
                      height=5)
    accessClass = Button(homeFrame, text = "Access Existing Class", \
                         command=lambda:findClass(window,homeFrame),\
                         width=20,\
                         height=5)

    #Position the buttons
    newClass.pack(pady=20)
    accessClass.pack(pady=20)

    #Pack the frame
    homeFrame.pack()

    #Main loop of the program
    window.mainloop()

