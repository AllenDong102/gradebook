import threading
from tkinter import *
from myClass import *
from accessClassesWindow import *

#Helper method for classAssignmentSetup, adds to the assignment list
def addAssignment(assignmentList,nameField,weightField):

    #Retrieve the name and weight from the entry
    name = nameField.get()
    weight = weightField.get()

    #Check for problems in the text
    if "\\" in name:
        print("Text may not contain \"\\\"")
    elif "$" in name:
        print("Text may not contain \"$\"")
    elif len(name) == 0:
        print("Name must exist")
    elif not weight.isdecimal():
        print("Weight must be a number")
    elif int(weight) <= 0:
        print("Weight may not be less than or equal to 0")

    #All good
    else:
        #Clear the entry fields
        nameField.delete(0,END)
        weightField.delete(0,END)

        #Add the assignment
        assignmentList.add_data([name,weight])

#Helper method for classAssignmentSetup, deletes selected item
def delAssignment(assignmentList):
    #Checks if an item has been selected
    if assignmentList.curselection() != None:
        assignmentList.__delitem__(assignmentList.curselection())

#Helper method for classStudentSetup
def addStudent(studentList,nameField):
    #Get the entered name
    name = nameField.get()
    if "$" in name: #Name cannot contain $
        print("Student names may not contain $")
    elif "\\" in name: #Name cannot contain \
        print("Text may not contain \"\\\"")

    #Get current list of students
    arr = studentList.get(0,END)

    if len(name) > 0 and not name in arr: #Name must exist, cannot be a duplicate

        #Clear the entry and add the name
        nameField.delete(0,END)
        studentList.insert(0,name)

#Create the final class object and return to the main menu
def createClass(window, oldFrame, students, assignNames, assignWeights, className, classCode):
    #Get the list of students before destroying the student list object
    arr = students.get(0,END)

    #Destroy all old objects
    threading.Thread(target=oldFrame.destroy()).start()

    #New class object
    newClass = MyClass(className,classCode, assignNames, assignWeights)

    #Adds students to the class
    for s in arr:
        newClass.addStudent(s)

    #Save the class to a file
    threading.Thread(target=newClass.writeClass()).start()

    #Main menu window setup
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
 
