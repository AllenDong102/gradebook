from tkinter import *

#Alter students of current class
def changeStudentsWindow(window, oldFrame,filename, c):
    
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

    #Add current students
    for s in c.students:
        studentList.insert(END, s.name)

    #Buttons to add or delete students, use helper methods
    addButton = Button(listFrame, text=" + ",\
                       command=lambda:addStudent(studentList,nameField,c))
    deleteButton = Button(listFrame, text=" - ",\
                          command=lambda:delStudent(studentList,filename, c))
    studentList.pack(pady=30,side=BOTTOM)
    addButton.pack(side=LEFT)
    deleteButton.pack(side=RIGHT)

    #When pressed, return to the class window
    continueFrame = Frame(createFrame)
    continueButton = Button(continueFrame, text="Done",command=lambda:classWindow(window, createFrame,filename, c))

    continueButton.pack(pady=30)

    #Arrange the frames
    nameFrame.pack()
    listFrame.pack()
    continueFrame.pack(side=BOTTOM)

    createFrame.pack()

#Helper method for changeStudents, adds the input student
def addStudent(studentList, nameField,c):
    #Get student name
    name = nameField.get()

    if len(name) > 0: #Name must exist

        #Clear the entry
        nameField.delete(0,END)

        #Add the student
        studentList.insert(0,name)
        c.addStudent(name)

#Helper method for changeStudents, deletes selected student
def delStudent(studentList,filename, c):
    #Check if anything has been selected
    if studentList.curselection() != None:
        #Get selected student
        student = studentList.get(studentList.curselection())

        #Delete the student from the class and the list
        c.delStudent(student,filename)
        studentList.delete(studentList.curselection())
