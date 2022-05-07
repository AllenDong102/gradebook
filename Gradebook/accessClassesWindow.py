#Import tkinter things
from tkinter import *
from tkinter.filedialog import askopenfilename

#Other project files
from myClass import *
from multiListBox import *
from accessHelpers import *

#Threading module
import threading

#Prompts user to select class
def findClass(window,oldFrame):
    #In the classes folder, tell user to select a .big file
    filename = askopenfilename(filetypes = (("big files","*.big"),("all files","*.*")))

    #If they did not cancel the file select
    if len(filename) > 0:
        #New window setup
        window.minsize(500,400)
        window.title("Choose Student")

        #Reads the class from the selected file
        c = readClass(filename)
        classWindow(window, oldFrame,filename, c)
        
#Creates a class object from the selected file
def readClass(path):

    #Open the file in read mode
    f = open(path,mode="r")
    txt = f.read()

    #Split up into array of lines
    lines = txt.splitlines()
    assigns = lines[2].split() #Assignment types + weights

    aNames = []
    aWeights = []

    for i in range(int(len(assigns)/2)):
        aNames.append(assigns[2*i].replace("$"," "))
        aWeights.append(assigns[2*i+1])

    #Create initial class object with class information at top of file
    retrieved = MyClass(lines[0],lines[1],aNames,aWeights)

    #Add student for each line after the first 3
    for stu in lines[3:]:
        retrieved.readStudent(stu)

    #Return the retrieved class
    return retrieved

#Window with the class information, list of students and grades
def classWindow(window, oldFrame,filename, c):
    window.minsize(500,400)
    window.title(c.name + " " + c.code)
    
    #Save for good measure, this function is called in a few places
    #Can be done in thread because nothing depends on this
    threading.Thread(target=c.writeClass()).start()

    #Destroy old objects and create a new frame
    oldFrame.destroy()
    readFrame = Frame(window)

    #Class info setup
    textFrame = Frame(readFrame)
    className = Label(textFrame, text="Class Name: " + c.name)
    className.pack(side=LEFT, pady=30, padx=30)
    classCode = Label(textFrame, text="Class Code: " + c.code)
    classCode.pack(side=RIGHT, pady=30, padx=30)

    #Student list setupd
    stuFrame = Frame(readFrame)

    stuList = MultiListbox(stuFrame)
    c.calculateAllGrades()
    #Loop through the students
    for s in c.students:
        #Adds the name and both grades to the student list
        stuList.add_data([s.name, "Grade: " + str(s.grade) + " / " + s.letterGrade])
        
    stuList.pack()

    #Buttons continue to the next steps
    buttonFrame = Frame(readFrame)

    #Access a student and their assignments
    accessButton = Button(buttonFrame, text="Select Student",\
                          command=lambda:studentWindow(window,readFrame,filename,stuList,c),\
                          width=13,height=3)
    accessButton.pack(side=TOP, pady=30, padx=30)
    #Change the current student list
    changeButton = Button(buttonFrame, text="Change Students",\
                       command=lambda:changeStudentsWindow(window,readFrame,filename, c),\
                          width=13,height=3)
    changeButton.pack(side=BOTTOM, pady=30, padx=30)


    
    #Arrange onscreen objects
    textFrame.pack()
    stuFrame.pack()
    buttonFrame.pack()

    readFrame.pack()


#Creates a window to view a student's assignements
def studentWindow(window, oldFrame, filename, stuList, c):
    #Check if the user has selected a student
    if stuList.curselection() != None:

        #Get the student's name
        stuName = stuList[stuList.curselection()][0]

        #Loop through and find the student in the class' list
        for i in range(len(c.students)):
            if stuName == c.students[i].name:
                #Get the index of the correct student rather than the object
                stuIndex = i
                break

        window.minsize(700,400)
        window.title(c.students[stuIndex].name) 

        #Destroy old objects, create new frame
        threading.Thread(target=oldFrame.destroy()).start()

        accessFrame = Frame(window)

        #Student info setup
        infoFrame = Frame(accessFrame)
        studentName = Label(infoFrame, text=c.students[stuIndex].name)
        studentGrade = Label(infoFrame, text="Grade: " + str(c.students[stuIndex].grade) + " / " + c.students[stuIndex].letterGrade)

        studentName.pack(side=LEFT,padx=30)
        studentGrade.pack(side=RIGHT,padx=30)

        #Assignment input setup
        inputFrame = Frame(accessFrame)

        #Select type of assignment from set list
        optionsFrame = Frame(inputFrame)
        options = []
        for key in c.assignments:
            options.append(key)

        #String variable for the option menu
        var = StringVar(inputFrame)
        var.set(options[0])

        #Assignment type entry setup
        assignLabel = Label(optionsFrame, text="Assignment type:")
        assignOptions = OptionMenu(optionsFrame, var, *options)
    
        assignLabel.pack(side=LEFT,pady=30)
        assignOptions.pack(side=RIGHT,pady=30)

        #Assignment name entry setup
        nameFrame = Frame(inputFrame)
        nameLabel = Label(nameFrame, text="Assignment name:")
        nameField = Entry(nameFrame)
        
        nameLabel.pack(side=LEFT,pady=30)
        nameField.pack(side=RIGHT,pady=30)

        #Assignment grade entry setup
        gradeFrame = Frame(inputFrame)
        gradeLabel = Label(gradeFrame, text="Assignment grade:")
        gradeField = Entry(gradeFrame)
        
        gradeLabel.pack(side=LEFT,pady=30)
        gradeField.pack(side=RIGHT,pady=30)

        #Arrange the inputs
        optionsFrame.pack(side=LEFT)
        nameFrame.pack(side=LEFT)
        gradeFrame.pack(side=LEFT)

        #Add or subtract assignments
        buttonFrame = Frame(accessFrame)

        #Adds assignment from user input
        addButton = Button(buttonFrame, text=" + ",\
                           command=lambda:threading.Thread(target=addAssignment(assignList,var.get(),nameField,gradeField)).start(),\
                           width=4,height=2) 
        
        #Delete selected assignment
        subButton = Button(buttonFrame, text=" - ",\
                           command=lambda:threading.Thread(target=delAssignment(assignList)).start(),\
                           width=4,height=2)

        addButton.pack(side=LEFT, padx=30)
        subButton.pack(side=RIGHT, padx=30)

        #List of assignments setup
        assignFrame = Frame(accessFrame)

        assignList = MultiListbox(assignFrame, columns=3)

        #Add assignments
        for a in c.students[stuIndex].assignList:
            assignList.add_data(a)

        #Button returns to the class list when finished
        doneButton = Button(assignFrame, text="Return to Class List",\
                        command=lambda:returnToList(window,accessFrame,stuIndex,assignList,filename,c),\
                            width=16,height=4)

        assignList.pack()

        doneButton.pack(pady=30)

        #Arrange onscreen objects
        infoFrame.pack(side=TOP)
        inputFrame.pack()
        buttonFrame.pack()
        assignFrame.pack()
                              
        accessFrame.pack()
    
#Sets up a window to alter the current class's student list
def changeStudentsWindow(window, oldFrame,filename, c):
    
    #Destroy old objects, create new frame
    threading.Thread(target=oldFrame.destroy()).start()
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

    #Add current students
    for s in c.students:
        studentList.insert(END, s.name)

    #Buttons to add or delete students, use helper methods
    addButton = Button(listFrame, text=" + ",\
                       command=lambda:threading.Thread(addStudent(studentList,nameField,c)).start(),\
                       width=4,height=2)
    deleteButton = Button(listFrame, text=" - ",\
                          command=lambda:threading.Thread(delStudent(studentList,filename, c)).start(),\
                          width=4,height=2)
    studentList.pack(pady=30,side=BOTTOM)
    addButton.pack(side=LEFT)
    deleteButton.pack(side=RIGHT)

    #When pressed, return to the class window
    continueFrame = Frame(createFrame)
    continueButton = Button(continueFrame, text="Done",\
                            command=lambda:classWindow(window, createFrame,filename, c),\
                            width=16,height=4)

    continueButton.pack(pady=30)

    #Arrange the frames
    nameFrame.pack()
    listFrame.pack()
    continueFrame.pack(side=BOTTOM)

    createFrame.pack()
