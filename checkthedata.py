import sqlite3


connection_data = sqlite3.connect('testproject.db')
datacursor = connection_data.cursor()

list = ['P1', 'P2']
datacursor.execute("Select timestamp, project, design, sample, material, print, orientation, apara, bpara, fpara, gpara, direction, speed, cycles, steps, contacts, samplerate, downsample, reference from database")
for x in datacursor:
    print(x)

def checkthedata(wanted_param, database, given_param, listofvalues):
    sqlcommand = "SELECT " + wanted_param + " FROM " + database + " WHERE " + given_param + " = "
    for value in listofvalues :
        sqlcommand = sqlcommand + "'" + value + "' OR " + given_param + " = "
    length = 3+4+len(given_param)
    sqlcommand = sqlcommand[:-length]
    return sqlcommand

print('"' + checkthedata("timestamp", "database", "project", list) + "IN (" + checkthedata("timestamp", "database", "material", list) + ')"')



checkboxes_design = []
checkboxes_sample = []
checkboxes_material = []
checkboxes_print = []
checkboxes_orientation = []
checkboxes_A = []
checkboxes_B = []
checkboxes_F = []
checkboxes_G = []
checkboxes_speed = []
checkboxes_cycles = []
checkboxes_steps = []
def checkthedata():
    notthefirst = False
    sqlcommand = ""
    if checkboxes_design:
        for value in checkboxes_design:
            sqlcommand = sqlcommand + "design = " + "'" + str(value) + "'" + " OR "
        sqlcommand = sqlcommand[:-4]
        notthefirst = True
    if checkboxes_sample:
        if notthefirst:
            sqlcommand = sqlcommand + " AND "
        for value in checkboxes_sample:
            sqlcommand = sqlcommand + "sample = " + "'" + str(value) + "'" + " OR "
        sqlcommand = sqlcommand[:-4]
        notthefirst = True
    if checkboxes_material:
        if notthefirst:
            sqlcommand = sqlcommand + " AND "
        for value in checkboxes_material:
            sqlcommand = sqlcommand + "material = " + "'" + str(value) + "'" + " OR "
        sqlcommand = sqlcommand[:-4]
        notthefirst = True
    if checkboxes_print:
        if notthefirst:
            sqlcommand = sqlcommand + " AND "
        for value in checkboxes_print:
            sqlcommand = sqlcommand + "print = " + "'" + str(value) + "'" + " OR "
        sqlcommand = sqlcommand[:-4]
        notthefirst = True
    if checkboxes_orientation:
        if notthefirst:
            sqlcommand = sqlcommand + " AND "
        for value in checkboxes_orientation:
            sqlcommand = sqlcommand + "orientation = " + "'" + str(value) + "'" + " OR "
        sqlcommand = sqlcommand[:-4]
        notthefirst = True
    if checkboxes_A:
        if notthefirst:
            sqlcommand = sqlcommand + " AND "
        for value in checkboxes_A:
            sqlcommand = sqlcommand + "A = " + "'" + str(value) + "'" + " OR "
        sqlcommand = sqlcommand[:-4]
        notthefirst = True
    if checkboxes_B:
        if notthefirst:
            sqlcommand = sqlcommand + " AND "
        for value in checkboxes_B:
            sqlcommand = sqlcommand + "B = " + "'" + str(value) + "'" + " OR "
        sqlcommand = sqlcommand[:-4]
        notthefirst = True
    if checkboxes_F:
        if notthefirst:
            sqlcommand = sqlcommand + " AND "
        for value in checkboxes_F:
            sqlcommand = sqlcommand + "F = " + "'" + str(value) + "'" + " OR "
        sqlcommand = sqlcommand[:-4]
        notthefirst = True
    if checkboxes_G:
        if notthefirst:
            sqlcommand = sqlcommand + " AND "
        for value in checkboxes_G:
            sqlcommand = sqlcommand + "G = " + "'" + str(value) + "'" + " OR "
        sqlcommand = sqlcommand[:-4]
        notthefirst = True
    if checkboxes_speed:
        if notthefirst:
            sqlcommand = sqlcommand + " AND "
        for value in checkboxes_speed:
            sqlcommand = sqlcommand + "speed = " + "'" + str(value) + "'" + " OR "
        sqlcommand = sqlcommand[:-4]
        notthefirst = True
    if checkboxes_cycles:
        if notthefirst:
            sqlcommand = sqlcommand + " AND "
        for value in checkboxes_cycles:
            sqlcommand = sqlcommand + "cycles = " + "'" + str(value) + "'" + " OR "
        sqlcommand = sqlcommand[:-4]
        notthefirst = True
    if checkboxes_steps:
        if notthefirst:
            sqlcommand = sqlcommand + " AND "
        for value in checkboxes_steps:
            sqlcommand = sqlcommand + "steps = " + "'" + str(value) + "'" + " OR "
        sqlcommand = sqlcommand[:-4]
        notthefirst = True
    return sqlcommand