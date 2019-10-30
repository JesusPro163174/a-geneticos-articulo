import random as rdn
from prettytable import PrettyTable

POPULATION_SIZE = 9

class Data:
    
    ROOMS         = [['R1',25],['R2',45],['R3',35]]

    METTING_TIMES = [
        ['MT1','MWF 09:00 - 10:00'],
        ['MT2','MWF 10:00 - 11:00'],
        ['MT3','TTH 09:00 - 10:30'],
        ['MT4','TTH 10:30 - 12:00']
    ]

    INSTRUCTORS = [
        ['I1','DR CARLOS HDZ'],
        ['I2','ING MARIO MORENO'],
        ['I3','ING ALI ZUNUN'],
        ['I4','ING DIANA']
    ]


    def __init__(self):
        self._rooms = []; self._meetingTimes = []; self._inscructors = []
        
        #creating rooms
        for i in range(0,len(self.ROOMS)):
            self.room = Room(self.ROOMS[i][0],self.ROOMS[i][1])
            self._rooms.append(self.room)
        
        #creating mettingTimes
        for i in range(0,len(self.METTING_TIMES)):
            self.metting_time = MeetingTime(self.METTING_TIMES[i][0],self.METTING_TIMES[i][1])
            self._meetingTimes.append(self.metting_time)
        
        #creating insctructors
        for i in range(0,len(self.INSTRUCTORS)):
            self.instructor = Instructor(self.INSTRUCTORS[i][0],self.INSTRUCTORS[i][1])
            self._inscructors.append(self.instructor)
        
        #creating courses
        course1 = Course("C1",'SUB1',[self._inscructors[0],self._inscructors[1]],25)
        course2 = Course("C2",'SUB2',[self._inscructors[0],self._inscructors[1],self._inscructors[2]],35)
        course3 = Course("C3",'SUB3',[self._inscructors[0],self._inscructors[1]],25)
        course4 = Course("C4",'SUB4',[self._inscructors[2],self._inscructors[3]],30)
        course5 = Course("C5",'SUB5',[self._inscructors[3]],35)
        course6 = Course("C6",'SUB6',[self._inscructors[0],self._inscructors[2]],45)
        course7 = Course("C7",'SUB7',[self._inscructors[1],self._inscructors[3]],45)
        self._courses = [course1,course2,course3,course4,course5,course6,course7]

        #creting departaments
        dept1 = Departament("IDS",[course1,course3])
        dept2 = Departament("BIO",[course2,course4,course5])
        dept3 = Departament("MECA",[course6,course7])
        self._depts = [dept1,dept2,dept3]
        
        self._numberOfClasses = 0
        for i in range(0,len(self._depts)):
            self._numberOfClasses = self._numberOfClasses + len(self._depts[i].get_courses())

    #getter
    def get_rooms(self):           return self._rooms
    def get_instructors(self):     return self._inscructors
    def get_courses(self):         return self._courses
    def get_depts(self):           return self._depts
    def get_meetingTimes(self):    return self._meetingTimes
    def get_numberOfClasses(self): return self._numberOfClasses

class Schedule:
    
    def __init__(self):
        self._data = data
        self._classes = []
        self._numberOfConflicts = 0
        self._fitness = -1
        self._classNum = 0
        self._isFitnessChanged = True
    
    def get_classes(self):
        self._isFitnessChanged = True
        return self._classes
    
    def get_numberOfConflicts(self):
        return self._numberOfConflicts
    
    def get_fitness(self):
        if(self._isFitnessChanged == True):
            self._fitness = self.calculate_fitness()
            self._isFitnessChanged = False
        return self._fitness 

    def initialize(self):
        depts = self._data.get_depts()
        for i in range(0,len(depts)):
            courses = depts[i].get_courses()
            for j in range(0,len(courses)):
                new_class = Class(self._classNum,depts[i],courses[j])
                self._classNum = self._classNum + 1
                
                time = data.get_meetingTimes()[rdn.randrange(0,len(data.get_meetingTimes()))]
                room = data.get_rooms()[rdn.randrange(0,len(data.get_rooms()))]
                instructor = courses[j].get_instructors()[rdn.randrange(0,len(courses[j].get_instructors()))]
                
                new_class.set_meetingTime(time)
                new_class.set_room(room)
                new_class.set_instructor(instructor)

                self._classes.append(new_class)
                
        return self
    
    def calculate_fitness(self):
        self._numberOfConflicts = 0
        classes = self.get_classes()
        for i in range(0,len(classes)):
            if(classes[i].get_rooms().get_seatingCapatity() < classes[i].get_course().get_maxNumbOfStudents()):
                self._numberOfConflicts = self._numberOfConflicts + 1
            for j in range(0,len(classes)):
                if (j >= i):
                    if(classes[i].get_meetingTime() == classes[j].get_meetingTime() and classes[i].get_id() != classes[j].get_id()):
                        if(classes[i].get_rooms() == classes[j].get_rooms()):
                            self._numberOfConflicts = self._numberOfConflicts +1
                        if(classes[i].get_instructor() == classes[j].get_instructor()):
                            self._numberOfConflicts = self._numberOfConflicts + 1
            
        return 1 / ((1.0*self._numberOfConflicts + 1))

    def __str_(self):
        returnValue = ""
        for i in range(0,len(self._classes)):
            returnValue = returnValue + str(self._classes[i]) + ','
        returnValue = returnValue  +str(self._classes[len(self._classes)-1])
        return returnValue

class Population:
    
    def __init__(self,size):
        self._size = size
        self._data = data
        self._shedules = []
        for i in range(0,size):
            self._shedules.append(Schedule().initialize())
    
    def get_schedules(self):
        return self._shedules
class GeneticAlgorithm:
    pass

class Course:
    
    def __init__(self,number,name,instructors, maxNumbOfStudents):
        self._number = number
        self._name   = name
        self._maxNumbOfStudents = maxNumbOfStudents
        self._instructors = instructors
    
    def get_number(self):            return self._number
    def get_name(self):              return self._name
    def get_instructors(self):       return self._instructors
    def get_maxNumbOfStudents(self): return self._maxNumbOfStudents
    def __str__(self):               return self._name

class Instructor:
    
    def __init__(self,id,name):
        self._id = id
        self._name = name
    
    def get_id(self):   return self._id
    def get_name(self): return self._name
    def __str__(self):  return self._name

class Room:
    
    def __init__(self,number,seatigCapacity):
        self._number = number
        self._seatingCapacity = seatigCapacity
    
    def get_number(self):          return self._number
    def get_seatingCapatity(self): return self._seatingCapacity

class MeetingTime:
    
    def __init__(self,id,time):
        self._id = id
        self._time = time
    
    def get_id(self):   return self._id
    def get_time(self): return self._time

class Departament:
    
    def __init__(self,name, courses):
        self._name = name
        self._courses = courses
    
    def get_name(self):    return self._name
    def get_courses(self): return self._courses

class Class:
    
    def __init__(self,id,dept,course):
        self._id = id
        self._dept = dept
        self._course = course
        self._instructor = None
        self._meetingTime = None
        self._room = None

    #getters
    def get_id(self):          return self._id
    def get_dept(self):        return self._dept
    def get_course(self):      return self._course
    def get_instructor(self):  return self._instructor
    def get_meetingTime(self): return self._meetingTime
    def get_rooms(self):       return self._room;

    #setters 
    def set_instructor(self,instructor):   self._instructor = instructor
    def set_meetingTime(self,meetingTime): self._meetingTime = meetingTime
    def set_room(self,room): self._room = room
    
    #toString Methos
    def __str__(self):
        return str(self._dept.get_name()) + ',' + str(self._course.get_number()) + ','+\
            str(self._room.get_number()) + ',' + str(self._instructor.get_id()) + ',' + str(self._meetingTime.get_id())

class DisplayMgr:

    def print_available_data(self):
        self.print_dept()
        self.print_course()
        self.print_room()
        self.print_instructor()
        self.print_meeting_times()

    def print_dept(self):
        print("DEPARTAMENTOS")
        table = PrettyTable()
        table.field_names = ["#","name",'courses']
        depts = data.get_depts()
        for i in range(0,len(depts)):
            courses = []
            for j in range(0,len(depts[i].get_courses())):
                courses.append(str(depts[i].get_courses()[j]))
            table.add_row(
                [
                    i,
                    depts[i].get_name(),
                    courses
                ]
            )
        print(table)
    def print_instructor(self):
        print("INSTRUCTORES")
        table = PrettyTable()
        table.field_names = ["#","name"]
        instructor = data.get_instructors()
        for i in range(0,len(instructor)):
            table.add_row([i,instructor[i]])
        print(table)
    def print_course(self):
        print("CURSOS")
        table = PrettyTable()
        table.field_names = ["#","name","instructors","max # students"]
        courses = data.get_courses()
        for i in range(0,len(courses)):
            instructors = []
            for j in range(0,len(courses[i].get_instructors())):
                instructors.append(str(courses[i].get_instructors()[j]))
            table.add_row(
                [
                    courses[i].get_number(),
                    courses[i].get_name(),
                    instructors,
                    courses[i].get_maxNumbOfStudents()
                ]
            )
        print(table)
    def print_room(self):
        print("SALONES DE CLASES")
        table = PrettyTable()
        table.field_names = ["room #","max seating capacity"]
        rooms = data.get_rooms()

        for i in range(0,len(rooms)):
            table.add_row(
                [
                    str(rooms[i].get_number()),
                    str(rooms[i].get_seatingCapatity())
                ]
            )
        print(table)
    
    def print_meeting_times(self):
        print("HORARIOS DE CLASE")
        table = PrettyTable()
        table.field_names = ["id","Meeting Time"]
        meeting_times = data.get_meetingTimes()
        for i in range(0,len(meeting_times)):
            table.add_row(
                [
                    meeting_times[i].get_id(),
                    meeting_times[i].get_time()
                ]
            )
        print(table)
    
    def print_generation(self,population):
        table1 = PrettyTable()
        table1.field_names = ["schedule #", "fitness", "# de conflictos"," classes[dept,class,room,instructor,time ]"]
        schedules = population.get_schedules()
        for i in range(0, len(schedules)):
            classes = []
            for j in range(0,len(schedules[i].get_classes())):
                classes.append(str(schedules[i].get_classes()[j]))
            table1.add_row(
                [
                    str(i),
                    round(schedules[i].get_fitness(),3),
                    schedules[i].get_numberOfConflicts(),
                    classes
                    #str(schedules[i].get_classes()[0])+' '+ str(schedules[i].get_classes()[1])+' '+str(schedules[i].get_classes()[2])+' '+str(schedules[i].get_classes()[3])+' '+str(schedules[i].get_classes()[4])+' '+str(schedules[i].get_classes()[5])+' '+str(schedules[i].get_classes()[6])
                ]
            )
        print(table1)

    def print_schedul_as_table(self,schedule):
        classes = schedule.get_classes()
        table = PrettyTable()
        table.field_names = ["Class #", "Dept", "Course(number, max # of students)", " Room(capacity)","Instructor"," Meeting Time"]
        for i in range(0, len(classes)):
            table.add_row(
                [
                    i, 
                    classes[i].get_dept().get_name(), 
                    classes[i].get_course().get_name()
                                        +' ('+str(classes[i].get_course().get_number())+','
                                        +str(classes[i].get_course().get_maxNumbOfStudents())+')',
                    classes[i].get_rooms().get_number()+'('+str(classes[i].get_rooms().get_seatingCapatity())+')',
                    classes[i].get_instructor().get_name(),
                    classes[i].get_meetingTime().get_time()
                ]
            )
        print(table)

data = Data()
generationNumber = 0

population = Population(POPULATION_SIZE)
population.get_schedules().sort(key=lambda x: x.get_fitness(), reverse=True)

displayMgr = DisplayMgr()
displayMgr.print_available_data()
displayMgr.print_schedul_as_table(population.get_schedules()[0])

print("\n Generation # "+ str(generationNumber))
displayMgr.print_generation(population)