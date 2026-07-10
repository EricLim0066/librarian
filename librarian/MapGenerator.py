import os
import json
# import openpyxl

import random


BARRIER = 0         #To set parameters where players cannot walk to
WALKABLESPACE = 1   #To set the space where players can walk to
ENTRANCE = 2        #The spawnpoint
BLANK = 3           #No interactions
COUNTER = 4         #Where customers buy, borrow or return books
BOOKSHELF = 5       #Where books are restocked and bought/borrowed
READINGAREA = 6     #Where customers read
STORAGEAREA = 7     #Where supplies are stored
SUPPLYDROPOFF = 8   #Where you get supplies
# The current map will require 12 bookshelves, 1-2 4-6units worth of reading area (mid-back zone), 2 entrance points, 1 counter, 1 storage area (displaced behind the counter) and one supplydropoff (at the back zone)

WIDTH = 7
HEIGHT = 12
#Map size


def BASEPLATEGENERATOR(): 
    LIBRARY = []

    for rowloop in range(HEIGHT): 
        row = []

        for column in range(WIDTH): 
            if  rowloop == 0  or  rowloop == HEIGHT - 1  or  column == 0  or  column == WIDTH - 1 : 
                row.append(BARRIER) #Add a barrier
            else: 
                row.append(WALKABLESPACE) #Add walkable space

        LIBRARY.append(row) #Add a row
    
    return LIBRARY

LIBRARY = BASEPLATEGENERATOR()                    #Call to generate the map


#Entrance points
LIBRARY[10][1] = ENTRANCE
LIBRARY[10][2] = ENTRANCE

#Counter
CounterGrid = {}

def CounterGrouper(counter_name, coordinates):
    CounterGrid[counter_name] = coordinates

    for row, col in coordinates:
        LIBRARY[row][col] = COUNTER

CounterGrouper("THECounter", [(9,4), (10,4)])

#Bookshelves
LIBRARY[4][1] = BOOKSHELF
LIBRARY[4][2] = BOOKSHELF
LIBRARY[4][3] = BOOKSHELF
LIBRARY[4][4] = BOOKSHELF
LIBRARY[5][1] = BOOKSHELF
LIBRARY[5][2] = BOOKSHELF
LIBRARY[5][3] = BOOKSHELF
LIBRARY[5][4] = BOOKSHELF
LIBRARY[6][1] = BOOKSHELF
LIBRARY[6][2] = BOOKSHELF
LIBRARY[6][3] = BOOKSHELF
LIBRARY[6][4] = BOOKSHELF
LIBRARY[7][1] = BOOKSHELF
LIBRARY[7][2] = BOOKSHELF
LIBRARY[7][3] = BOOKSHELF
LIBRARY[7][4] = BOOKSHELF


#Reading area generation [By presets]
RA_PRESETS = [
    # Preset Missing Bottom Right Corner Cell Square
    [(1,1), (1,2), (1,3), (2,1), (2,2), (2,3), (3,1), (3,2)],
    # Preset Rectangle
    [(1,1), (1,2), (1,3), (1,4), (2,1), (2,2), (2,3), (2,4)],
    # Preset Rotated S
    [(1,1), (1,2), (2,1), (2,2), (2,3), (2,4), (3,3), (3,4)],
    # Preset Missing Top Left Corner Cell Square
    [(1,3), (1,4), (2,2), (2,3), (2,4),(3,2), (3,3), (3,4)],
    # Preset Parallel Lines [Least amount of cells]
    [(1,2), (2,2), (3,2), (1,4), (2,4), (3,4), (1,3)],
    # Preset Absolute Edges
    [(1,1), (2,1), (3,1), (1,4), (2,4), (3,4), (1,2), (1,3)]
]

RNGChoser = random.choice(RA_PRESETS)

for row, col in RNGChoser:
    LIBRARY[row][col] = READINGAREA


#Barrier patch up
LIBRARY[1][5] = BARRIER
LIBRARY[2][5] = BARRIER
LIBRARY[3][5] = BARRIER
LIBRARY[4][5] = BARRIER
LIBRARY[5][5] = BARRIER
LIBRARY[6][5] = BARRIER
LIBRARY[9][5] = BARRIER
LIBRARY[10][5] = BARRIER


#Storage and delivery point
LIBRARY[7][5] = SUPPLYDROPOFF
LIBRARY[8][5] = STORAGEAREA

# workbook = openpyxl.Workbook()                           #Open an Excel sheet
# sheet = workbook.active                                  #Use active sheet
# sheet.title = "Library Map"                              #Name the sheet title
# for row_index, row in enumerate(LIBRARY, start=1):   #Loop of 26 rows [Python starts at 0. Use start=1 to change starting point at 1]
#     for col_index, value in enumerate(row, start=1):       #Loop of 26 columns in a row [Python starts at 0. Use start=1 to change starting point at 1]
#         sheet.cell(row=row_index, column=col_index, value=value) #Generate the values of the list to the excel sheet according to the positions
     
# workbook.save("MAP.xlsx") #Save everything into a new excel sheet named MAP.xlsx