#### IMPORTS ####
import event_manager as EM


#### CONSTANTS ####
CURRENT_YEAR = 2020
MIN_AGE = 16
MAX_AGE = 120
MIN_SEMESTER = 1
ID_LEN = 8
ID = 0
NAME = 1
AGE = 2
BIRTH_YEAR = 3
SEMESTER = 4
INVALID_ID_FIRST = '0'
TEMP_OUT_FILE = 'temp_out'

#### PART 1 ####
# Filters a file of students' subscription to specific event:
#   orig_file_path: The path to the unfiltered subscription file
#   filtered_file_path: The path to the new filtered file
def fileCorrect(orig_file_path: str, filtered_file_path: str):
    filtered_file = open(filtered_file_path, 'w')
    line_list = fileToList(orig_file_path)
    line_list.sort(key=returnIdFromLine)

    valid_list = getValidLinesFromList(line_list)

    i = 0
    while i < len(valid_list) - 1:
        if valid_list[i][ID] == valid_list[i+1][ID]:
            del valid_list[i+1]
        i += 1
    
    for line in valid_list:                       
        filtered_file.write(getStringFromLine(line))
        filtered_file.write('\n')

    filtered_file.close()
    
def getValidLinesFromList(line_list: list):
    valid_list = []
    for line in line_list:
        if lineIsLegal(line):
            valid_list.append(line)

    return valid_list

def returnIdFromLine(line: list):
    return line[ID]

def returnAgeFromLine(line: list):
    return int(line[AGE])

def fileToList(orig_file_path: str):
    orig_file = open(orig_file_path, 'r')
    raw_line_list = []
    for line in orig_file:
        raw_line_list.append(line.split(','))
    orig_file.close()

    line_list = []
    for line in raw_line_list:
        new_line = [item.strip(' ') for item in line]
        line_list.append(new_line)

    line_list.reverse()
    return line_list

def lineIsLegal(line: str):
    if line[ID].isdigit() == False or line[ID][0] == INVALID_ID_FIRST or len(line[ID]) != ID_LEN:
        return False
    elif line[SEMESTER][0].isdigit() == False or int(line[SEMESTER][0]) < MIN_SEMESTER:
        return False
    elif line[AGE].isdigit() == False or int(line[AGE]) > MAX_AGE or int(line[AGE]) < MIN_AGE:
        return False
    elif CURRENT_YEAR - int(line[BIRTH_YEAR]) != int(line[AGE]):
        return False
    elif isInvalidName(line[NAME]):
        return False

    return True

def isInvalidName(name: str):
    full_name = name.split()
    for word in full_name:
        if word.isalpha() == False:
            return True
    
    return False

def getStringFromLine(line: list):
    fixed_name = line[NAME].split()
    temp_semester = line[SEMESTER].split() 
    line[SEMESTER] = temp_semester[0]
    line[NAME] = ' '.join(fixed_name)
    legal_line = ', '.join(line)
    return legal_line

    
    
# Writes the names of the K youngest students which subscribed 
# to the event correctly.
#   in_file_path: The path to the unfiltered subscription file
#   out_file_path: file path of the output file
def printYoungestStudents(in_file_path: str, out_file_path: str, k: int) -> int:
    if k <= 0:
        return -1

    new_file = open(out_file_path, 'w')

    fileCorrect(in_file_path, TEMP_OUT_FILE)
    line_list = fileToList(TEMP_OUT_FILE)
    line_list.reverse()
    line_list.sort(key=returnAgeFromLine)
    i = 0
    for line in line_list:
        if i >= k:
            break
        else:
            new_file.write(line[NAME])
            new_file.write('\n')
            i += 1

    new_file.close()
    return i

    
    
# Calculates the avg age for a given semester
#   in_file_path: The path to the unfiltered subscription file
#   retuns the avg, else error codes defined.
def correctAgeAvg(in_file_path: str, semester: int) -> float:
    if semester < MIN_SEMESTER:
        return -1
    fileCorrect(in_file_path, TEMP_OUT_FILE)
    line_list = fileToList(TEMP_OUT_FILE)
    num_of_students = 0
    sum = 0.0
    for line in line_list:
        if int(line[SEMESTER]) == semester:
            sum += int(line[AGE])
            num_of_students += 1

    if num_of_students == 0:
        return 0
    
    return sum/num_of_students

    

#### PART 2 ####
# Use SWIG :)
# print the events in the list "events" using the functions from hw1
#   events: list of dictionaries
#   file_path: file path of the output file
def printEventsList(events :list,file_path :str): #em, event_names: list, event_id_list: list, day: int, month: int, year: int):
    init_date = getFirstDate(events)
    em = EM.createEventManager(init_date)
    for event in events:
        EM.emAddEventByDate(em, event['name'], event['date'], event['id'])

    EM.emPrintAllEvents(em, file_path)
    return em

def getFirstDate(events: list):
    date = events[0]['date']
    for event in events:
        temp_date = event['date']
        if EM.dateCompare(date, temp_date) > 0:
            date = new_date


    return date

    
def testPrintEventsList(file_path :str):
    events_lists=[{"name":"New Year's Eve","id":1,"date": EM.dateCreate(30, 12, 2020)},\
                    {"name" : "annual Rock & Metal party","id":2,"date":  EM.dateCreate(21, 4, 2021)}, \
                                 {"name" : "Improv","id":3,"date": EM.dateCreate(13, 3, 2021)}, \
                                     {"name" : "Student Festival","id":4,"date": EM.dateCreate(13, 5, 2021)},    ]
    em = printEventsList(events_lists,file_path)
    for event in events_lists:
        EM.dateDestroy(event["date"])
    EM.destroyEventManager(em)

#### Main #### 
# feel free to add more tests and change that section. 
# sys.argv - list of the arguments passed to the python script
if __name__ == "__main__":
    import sys
    if len(sys.argv)>1:
        testPrintEventsList(sys.argv[1])
