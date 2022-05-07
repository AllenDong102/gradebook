#Imports
from tkinter import *
from multiListBox import *
from myClass import *
from accessClassesWindow import *
from createHelpers import *

import threading

#Sets up the window to get the class information
def classInfoSetup(window,oldFrame):
    #Resize window, change the name
    window.minsize(400,300)
    window.title("Creating Classes")

    #Destroy the previous onscreen objects, create new frame
    threading.Thread(target=oldFrame.destroy()).start()
    createFrame = Frame(window)

    #Class name entry field setup
    nameFrame = Frame(createFrame)
    nameLabel = Label(nameFrame, text="Class name:")
    nameField = Entry(nameFrame)

    nameLabel.pack(side=LEFT,pady=30)
    nameField.pack(side=RIGHT,pady=30)
    
    #Class code entry field setup
    codeFrame = Frame(createFrame)
    codeLabel = Label(codeFrame, text="Class code:")
    codeField = Entry(codeFrame)
    
    codeLabel.pack(side=LEFT,pady=30)
    codeField.pack(side=RIGHT,pady=30)

    #Continue button setup, goes to the next step when pressed
    continueFrame = Frame(createFrame)
    continueButton = Button(continueFrame, text="Continue", \
                            command=lambda:classAssignmentSetup(window, createFrame,nameField.get(), codeField.get()),\
                            width=12,height=3)

    continueButton.pack(pady=30)

    #Organize each frame
    nameFrame.pack()
    codeFrame.pack()
    continueFrame.pack()

    createFrame.pack()

#Setup window for assignment type information
def classAssignmentSetup(window,oldFrame,className,classCode):
    #"\" is not allowed in any text that will get saved to the class file
    if "\\" in className or "\\" in classCode:
        print("Text may not contain \"\\\"")

    #If the name and code have been entered, continue
    elif len(className) > 0 and len(classCode) > 0:

        #Destroy all old objects, create new frame
        threading.Thread(target=oldFrame.destroy()).start()
        createFrame = Frame(window)

        #Assignment name entry setup
        nameFrame = Frame(createFrame)
        nameLabel = Label(nameFrame, text="Assignment type:")
        nameField = Entry(nameFrame)
        
        nameLabel.pack(side=LEFT,pady=30)
        nameField.pack(side=RIGHT,pady=30)

        #Assignment weight entry setup
        weightFrame = Frame(createFrame)
        weightLabel = Label(weightFrame, text="% of total grade:")
        weightField = Entry(weightFrame)
        
        weightLabel.pack(side=LEFT,pady=30)
        weightField.pack(side=RIGHT,pady=30)

        #Listing of the created assignments
        listFrame = Frame(createFrame)
        assignmentList = MultiListbox(listFrame)
        assignmentList.pack(pady=30,side=BOTTOM)

        #Buttons to add or remove assignment types
        addButton = Button(listFrame, text=" + ", \
                           command=lambda:threading.Thread(target=addAssignment(assignmentList,nameField,weightField)).start(),\
                           width=4,height=2)
        deleteButton = Button(listFrame, text=" - ", \
                              command=lambda:threading.Thread(delAssignment(assignmentList)).start(),\
                              width=4,height=2)

        addButton.pack(side=LEFT)
        deleteButton.pack(side=RIGHT)

        #When pressed, continue to next step
        continueFrame = Frame(createFrame)
        continueButton = Button(continueFrame, text="Continue",\
                                command=lambda:classStudentSetup(window,createFrame,assignmentList,className,classCode),\
                                width=16, height=4)

        continueButton.pack(pady=30)

        #Organize onscreen objects
        nameFrame.pack()
        weightFrame.pack()
        listFrame.pack()
        continueFrame.pack(side=BOTTOM)

        createFrame.pack()

#Setup window for the students in the class
def classStudentSetup(window,oldFrame,assignments,className,classCode):

    #Retrieve the entered data from the assignment list
    assignNames = assignments.boxes[0].get(0,END)
    assignWeights = assignments.boxes[1].get(0,END)

    total = 0
    #Loop through assignment weights
    for w in assignWeights:
        total += int(w) #Convert to int from string

    if total != 100: #Total weights must add to 100
        print("Assignment weights must add to 100%!")
    else:
        #Destroy old objects, create new frame
        oldFrame.destroy()
        createFrame = Frame(window)

        #Student name entry setup
        nameFrame = Frame(createFrame)
        nameLabel = Label(nameFrame, text="Student name:")
        nameField = Entry(nameFrame)
        
        nameLabel.pack(side=LEFT,pady=30)
        nameField.pack(side=RIGHT,pady=30)

        #Student list setup
        listFrame = Frame(createFrame)
        studentList = Listbox(listFrame,width=20,height=10)
        studentList.pack(pady=30,side=BOTTOM)

        #Buttons to add or remove students
        addButton = Button(listFrame, text=" + ", \
                           command=lambda:threading.Thread(addStudent(studentList,nameField)).start(),\
                           width=4,height=2)
        deleteButton = Button(listFrame, text=" - ", \
                              command=lambda:threading.Thread(studentList.delete(ANCHOR)).start(),\
                              width=4,height=2)
    
        addButton.pack(side=LEFT)
        deleteButton.pack(side=RIGHT)

        #Continue button setup; when pressed, finalize entered data
        continueFrame = Frame(createFrame)
        continueButton = Button(continueFrame, text="Create class",\
                                command=lambda:createClass(window, createFrame,studentList, assignNames, assignWeights,className,classCode),\
                                width=16,height=4)


        continueButton.pack(pady=30)

        #Organize onscreen objects
        nameFrame.pack()
        listFrame.pack()
        continueFrame.pack(side=BOTTOM)

        createFrame.pack()

