import csv # activate library for csv support
with open('descriptionsClean.csv', mode='r') as csv_file: # open the csv file
    csv_reader = csv.DictReader(csv_file, delimiter=";") # read the contents into memory
    for row in csv_reader: # initiate an iterative reading of each row
        for key,value in row.items(): # check each dictionary
            if key == 'creator' and 'Dahlström' in value: # match/search on dictionary key and its value
                for key,value in row.items(): # do the following with each matching dictionary according to condition above
                    if key == 'title': # take title and output
                        print(value,end='')
                    if key == 'date' : # take year and output within parentheses
                        print('('+value+')')
