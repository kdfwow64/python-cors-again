import csv

def convertCsvToArray(fileString):
        '''Converts a CSV string to an array'''
        return list(csv.reader(fileString.split('\n'), delimiter=','))

