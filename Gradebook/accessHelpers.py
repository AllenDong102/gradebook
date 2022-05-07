#Helper methods for accessClassesWindow.py
from myClass import *
from tkinter import *
import threading

#studentWindow helper method, adds assignment
def addAssignment(assignList, assignType, nameField, gradeField):
    #Get name and grade
    name = nameField.get()
    grade = gradeField.get()

    #Check for improper input
    if "\\" in name:
        print("Text may not contain \"\\\"")

    #Grade must be number, name must exist
    elif grade.isdecimal() and len(name) >= 0:
        #Delete the field entries
        nameField.delete(0,END)
        gradeField.delete(0,END)

        #Add the assignment
        assignList.add_data([assignType,name,grade])

#studentWindow helper method, deletes selected assignment
def delAssignment(assignList):
    #Check if anything has been selected
    if assignList.curselection() != None:
        assignList.__delitem__(assignList.curselection())

#studentWindow helper method, returns to the student list
def returnToList(window,oldFrame,stuIndex,newAssigns,filename,c):

    #Clear the student's assignments
    c.students[stuIndex].assignList = []

    #Retrieve data from multiListbox
    assignTypes = newAssigns.boxes[0].get(0,END)
    assignNames = newAssigns.boxes[1].get(0,END)
    assignGrades = newAssigns.boxes[2].get(0,END)

    #Add the assignments
    for i in range(len(assignTypes)):
        c.students[stuIndex].addAssignment(assignTypes[i],assignNames[i],assignGrades[i])

    #Save class
    threading.Thread(target=c.writeClass()).start()

    #Return to the class window
    from accessClassesWindow import classWindow
    classWindow(window,oldFrame,filename,c)

#Helper method for changeStudents, adds the input student
def addStudent(studentList, nameField, c):
    #Get the entered name
    name = nameField.get()
    
    #Get current list of students
    arr = studentList.get(0,END)

    if "$" in name: #Name cannot contain $
        print("Student names may not contain $")
    elif "\\" in name: #Name cannot contain \
        print("Text may not contain \"\\\"")
        
    elif len(name) > 0 and not name in arr: #Name must exist, cannot be a duplicate
        #Clear the entry and add the name
        nameField.delete(0,END)
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
