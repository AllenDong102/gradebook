#Student with a name, grade, letter grade, and a 2D list of assignments
class Student:
  
  def __init__(self, name):
    self.name = name
    self.grade = 0
    self.letterGrade = ""
    self.assignList = []

  #Ddds an assignment
  def addAssignment(self, assignType, assignName, grade):
    self.assignList.append([assignType, assignName, grade])

  #Deletes a specific assignment given its type, name, and grade
  def delAssignment(self, assignType, assignName, grade):

    for i in range(len(assignList)):
      if assignList[i][2] == assignName:
        assignList.pop(i)
