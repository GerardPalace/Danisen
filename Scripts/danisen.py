#This file read the csv, run trough it and compute score for each players.

def parseCSV(file_path):
    csv = open(file_path)
    for row in csv:
        print(row)
