from Student import *
from math import trunc
from statistics import mean
#class with a name, code, dictionary of assignments and weights, and a list of students 
class MyClass:
    def __init__(self, name, code, aNames=[], aWeights=[]):
        self.name = name
        self.code = code

        #Set up the empty lists
        self.students = []
        self.assignments = {}

        #Correspond assignment names to weights
        for i in range(len(aNames)):
            self.assignments[aNames[i]]= int(aWeights[i])
            
    #Saves the class to a file
    def writeClass(self):
        f = open("Classes/" + self.name+" " + self.code+".big", mode="w")

        #First two lines are the name and code of the class
        f.write(self.name+"\n")
        f.write(self.code+"\n")

        #Third line is the assignments and weights
        for key in self.assignments:
            #Spaces replaced with "$" so .split will work correctly
            f.write(key.replace(" ", "$") + " ")
            f.write(str(self.assignments[key]) + " ")

        #Fourth line onwards will each have a student
        f.write("\n")
        for s in self.students:
            #Create a string for each student's line in the file, add their assignments
            sLine = s.name.replace(" ", "$") + " "

            for a in s.assignList:
                for part in a:
                    #Each part of the assignment will be followed by a space
                    sLine += part.replace(" ","$") + " "

            #Write the current student, add a newline
            f.write(sLine + "\n")
        #Close the file
        f.close()
        
    #Adds a student to the class
    def addStudent(self, name):
        s = Student(name)
        self.students.append(s)

    #Removes a student from the class
    def delStudent(self,stuName,path):
        #First, remove from this class's student list
        for s in self.students:
            if s.name == stuName:
                self.students.remove(s)
                break

    #Read a student given a line of text from the file
    def readStudent(self, stuLine):
        #Array of each string
        stuLine = stuLine.split()

        #First string will be the student's name, re-add spaces where necessary
        name = stuLine[0].replace("$"," ")

        #Create new student object
        s = Student(name)

        #Rest of array will be assignments
        stuLine = stuLine[1:]

        #Each assignment has 3 different parameters
        #So len(arr)/3 is the number of assignments
        for i in range(int(len(stuLine)/3)):
            #Re-add spaces where necessary
            stuLine[3*i] = stuLine[3*i].replace("$"," ")
            stuLine[3*i+1] = stuLine[3*i+1].replace("$"," ")
            stuLine[3*i+2] = stuLine[3*i+2].replace("$"," ")

            #Add an assignment
            s.addAssignment(stuLine[3*i], stuLine[3*i+1], stuLine[3*i+2])

        #Adds the student to the class
        self.students.append(s)

    #Calculates a students final grade, given the student
    def calculateGrade(self, student):

        #If there are no assignments, don't assign a grade yet
        if len(student.assignList) == 0:
            student.grade = "N/A"
            student.letterGrade = "N/A"
            return 0
        student.grade = 0

        curAssignments = set([x[0] for x in student.assignList])
        curDict = {}
        # if there aren't the same amount of assignments: i.e there is one assignmentType with no assignments
        if len(curAssignments) != len(self.assignments):
            for i in curAssignments:
                # redassigns the weighting
                curDict[i] = self.assignments[i]
            newSum = sum(curDict.values())
            # reweights without the empty assignmentType
            for i in curDict:
                curDict[i] = int((curDict[i]/newSum) * 100)
            for i in curAssignments:
                # emptys the gradeList everytime assignment is changed
                gradeList = []

                # runs through assignList
                for j in student.assignList:

                    # if equal to assignType in assignList, add the grade to the gradeList
                    if i == j[0]:
                        gradeList.append(int(j[2]))
                        
                # before the assignment type changes, add the current mean of gradeList*the weighting of that assignment
                if len(gradeList) > 0:
                    student.grade += (mean(gradeList) * curDict[i] * .01)
        else:
            for key in self.assignments:
                #Emptys the gradeList everytime assignment is changed
                gradeList = []
                #Runs through assignList
                for a in student.assignList:
                    #If equal to assignType in assignList, add the grade to the gradeList
                    if key == a[0]:
                        gradeList.append(int(a[2]))
                        
                #Before the assignment type changes, add the current mean of gradeList*the weighting of that assignment
                if len(gradeList) > 0:
                    student.grade += (mean(gradeList) * self.assignments[key] * .01)
                
        #Round to 1 decimal place
        student.grade = trunc(student.grade*10)/10
        
        # Assigns the lettergrade for the student based on their grade
        if student.grade >= 97:
            student.letterGrade = "A+"
        elif student.grade < 97 and student.grade >= 93:
            student.letterGrade = "A"
        elif student.grade < 93 and student.grade >= 90:
            student.letterGrade = "A-"
        elif student.grade < 90 and student.grade >= 87:
            student.letterGrade = "B+"
        elif student.grade < 87 and student.grade >= 83:
            student.letterGrade = "B"
        elif student.grade < 83 and student.grade >= 80:
            student.letterGrade = "B-"
        elif student.grade < 80 and student.grade >= 77:
            student.letterGrade = "C+"
        elif student.grade < 77 and student.grade >= 73:
            student.letterGrade = "C"
        elif student.grade < 73 and student.grade >= 70:
            student.letterGrade = "C-"
        elif student.grade < 70 and student.grade >= 67:
            student.letterGrade = "D+"
        elif student.grade < 67 and student.grade >= 63:
            student.letterGrade = "D"
        elif student.grade < 63 and student.grade >= 60:
            student.letterGrade = "D-"
        else:
            student.letterGrade = "F"

    #Performs the grade calculation for all students
    def calculateAllGrades(self):
        for s in self.students:
            self.calculateGrade(s)
