import sqlite3
import os

# Define path to data
path1 = "C:\\Users\\Messknecht\\OneDrive - tu-braunschweig.de\\Documents"
projectdata = []
designdata = []
sampledata = []
materialdata = []
printdata = []
timestamp = []
direction = []
speed = []
data = []
# Create a database in RAM
connection_data = sqlite3.connect('testdata.db')
# Create a cursor to work with
datacursor = connection_data.cursor()

#Crerate a table if it doesn't exist



Q1 = "CREATE TABLE IF NOT EXISTS datas (timestamp text PRIMARY KEY ON CONFLICT IGNORE, project int, design int, sample int, material int, print int, direction short int, speed short int)"
Q2 = "CREATE TABLE IF NOT EXISTS csvdata (timestamp text PRIMARY KEY ON CONFLICT IGNORE REFERENCES datas(timestamp), csvdata str)"
Q21 = "CREATE TABLE IF NOT EXISTS csvdatabetter (time int, step int, R1 int, R2 int)"
Q3 = "INSERT OR IGNORE INTO datas (timestamp) VALUES (?)"
Q4 = "UPDATE datas SET project = ? WHERE timestamp = ?"
Q5 = "UPDATE datas SET design = ? WHERE timestamp = ?"
Q6 = "INSERT INTO csvdata (timestamp, csvdata) VALUES (?, ?)"
Q7 = "UPDATE datas SET direction = ? WHERE timestamp = ?"
Q8 = "INSERT INTO csvdatabetter (time, step, R1, R2) VALUES (?, ?, ?, ?)"




# define function to parse a directory and return a list of files
def get_data(path):
    global data
    global otherdata
    dupcheck = False
    # get list of files in directory
    files = os.listdir(path)
    # create empty list to store data
    data = []
    otherdata = []
    # loop through files
    for file in files:
        # look for files that end with .csv
        if file.endswith('.csv'):
            # duplicate check
            for duplicate in data:
               if file[:-4] == duplicate:
                    dupcheck = True
            if dupcheck == False:
                # add file to list
                data.append("File")
                data.append(file[:-4])
                #Parse the file and add the data to the list
                with open(path + "/" + file, 'r') as f:
                    lines = f.readlines()
                    data.append("Test")
                    #append only the first line of the file
                    data.append(lines[0][:-1])
                    #bundle the rest of the lines into a string
                    data.append("".join(lines[2:]))
                    # append the rest of the lines starting from the third to data
                    for line in lines[2:]:
                        otherdata.append(line[:-1])
            else:
                #if duplicate is found, skip it
                print ("Duplicate file found, skipping")
                dupcheck = False
                continue
    return data

def getvalues(data):
    global projectdata
    global designdata
    global sampledata
    global materialdata
    global printdata
    global timestamp
    global direction
    # Parse the first object in data list up to the first underscore
    searchkey_file = "File"
    searchkey_test = "Test"
    index_file = []
    index_test = []
    #iterate through the list and find the every occurence of the searchkey
    for i in range(len(data)):
        if data[i] == searchkey_file:
            index_file.append(i+1)
        if data[i] == searchkey_test:
            index_test.append(i+1)
    for i in range(len(index_file)):
        paraList = data[index_file[i]].split("_")
        projectdata.append(paraList[0])
        designdata.append(paraList[1])
        sampledata.append(paraList[2])
        materialdata.append(paraList[3])
        printdata.append(paraList[4])
        timestamp.append(paraList[6])
    for i in range(len(index_test)):
        testList = data[index_test[i]].split(",")
        direction.append(testList[0])  


def splitdata(otherdata):
    global time
    global step
    global R1
    global R2
    time = []
    step = []
    R1 = []
    R2 = []
    for i in range(len(otherdata)):
        # get the value before the first comma
        time.append(otherdata[i].split(",")[0])
        # get the value between the first and second comma
        step.append(otherdata[i].split(",")[1])
        # get the value between the second and third comma
        R1.append(otherdata[i].split(",")[2])
        # get the value after the third comma
        R2.append(otherdata[i].split(",")[3])



data = get_data(path1)
getvalues(data)
splitdata(otherdata)


datacursor.execute(Q1)
datacursor.execute(Q2)
datacursor.execute(Q21)
for x in range(len(timestamp)):
    datacursor.execute(Q3, (timestamp[x],))
    datacursor.execute(Q4, (projectdata[x],timestamp[x]))
    datacursor.execute(Q5, (designdata[x],timestamp[x]))
    datacursor.execute(Q7, (direction[x],timestamp[x]))
    datacursor.execute(Q6, (timestamp[x], data[x+4]))
# insert into csvdatabetter the lists time, step, R1, R2
datacursor.executemany(Q8, zip(time, step, R1, R2))

connection_data.commit()

datacursor.execute("SELECT * FROM datas")
for x in datacursor:
    print(x)

#datacursor.execute("SELECT * FROM csvdatabetter")
#for x in datacursor:
#    print(x)

connection_data.close()