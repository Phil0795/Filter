# This function lets the user select a directory to parse


import os
from PyQt6.QtWidgets import QFileDialog

def selectDirectory():
    global iparsedthis
    # Get the directory from the user
    directory = QFileDialog.getExistingDirectory(None, "Select Directory")
    # Get the files from the directory
    files = os.listdir(directory)
    # Create a list to store the data
    iparsedthis = []
    # Loop through the files
    for i in files:
        # Check if the file is a .txt file
        if i.endswith(".csv"):
            # Add the file to the data list
            iparsedthis.append(i)
    # Print the data
    print(iparsedthis)

# find an item starting with the letter "P" in the list
x = next(item for item in iparsedthis if item.startswith("P"))

# find a list in a list starting with the letter "P"
x = [item for item in iparsedthis if item.startswith("P")]

# convert a string into a list seperated by commas
x = "1,2,3,4,5,6,7,8,9,10".split(",")

# get an element from a list without the first 3 characters
x = "1234567890"[3:]