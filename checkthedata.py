import sqlite3


connection_data = sqlite3.connect('testproject.db')
datacursor = connection_data.cursor()


datacursor.execute("Select timestamp, project, design, sample, material, print, orientation, apara, bpara, fpara, gpara, direction, speed, cycles, steps, contacts, samplerate, downsample, reference from database")
for x in datacursor:
    print(x)