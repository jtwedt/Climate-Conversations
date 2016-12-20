import pdb
import pandas as pd
import time
import numpy as np
import os
from random import randint
import datetime


# Load the events database RACHEL

xlsx = pd.ExcelFile('firstHistoricClimateEvents.xlsx')
df = xlsx.parse(xlsx.sheet_names[0])
events = df.to_dict()
nevents = len(events['start year'])
earliestAge = 7
#print events.keys()    # We may want to change some of the key names to be more efficient for indexing!


#load temperature and sea ice datasets
temperatureFile = 'GLB.Ts+dSST.csv' # from  http://data.giss.nasa.gov/gistemp/
iceFile  = 'N_09_seaicearea_v2.txt' # from https://nsidc.org/data/seaice_index/archives.html
#process the temperature timeseries
yrTemp, AnnMeanT = np.genfromtxt(temperatureFile, unpack = True, skiprows = 3, delimiter = ',', usecols = (0,13), skip_footer = 1)
#compute the decadal average for temperature:
decadalT = np.reshape(AnnMeanT[:130], [13,10])
decadalT  = np.nanmean(decadalT, axis = 1)
decadalT = [float("{0:2f}".format(decadalT[i])) for i in range(len(decadalT))]
decadalT = np.asarray(decadalT)
#compute the 1881-1901 average
tempClimo = np.mean(AnnMeanT[:20])

#process the sea ice time series
yrIce, extent, area = np.genfromtxt(iceFile, unpack = True, usecols = (0,4,5), skip_footer = 14, skip_header = 1)
iceExtentClimo = np.mean(extent[:20]) #1979-1999 average
iceAreaClimo  = np.mean(area[:20]) 



delayinseconds = 1

# set up lists and global variables
names = []
birthyears = []

# set up functions
def is_number(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def getplayerinfo():
    # Get input from user (name, birthdate, number of rounds) JUDY
    if test == 1:
        nplayers = 2
        nrounds = 2
        names.append('Judy')
        names.append('Rachel')
        birthyears.append(1982)
        birthyears.append(1986)

    else:
        nplayers  = input('How many people are in the conversation? ')
        nrounds = input('How many rounds would you like to play? ')

        # Work out how long to delay between questions
        delayinseconds = 1

        indices = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th']
        for i in range(nplayers):
            thisname = raw_input('Please enter the ' + indices[i] + ' players name: ')
            names.append(thisname)
            

            needage = True
            while needage:
                thisage = raw_input('Please enter ' + thisname + '\'s year of birth: ')

                if is_number(thisage):
                    while (int(thisage) < 1880 or int(thisage) > datetime.datetime.now().year):
                        thisage = input('You are either over 130 years old, or haven\'t been born yet. Please re-enter ' + thisname + '\'s players year of birth: ')
                    birthyears.append(int(thisage))
                    needage = False
                else:
                    print('Please enter a number, for example, 1980')   
                
    return(nplayers,nrounds,names,birthyears)   # return these variables so they are globally known

# Main program
print('Welcome! Lets get a little information before we start the conversation.')
test  = input('Is this a test run? 1= yes, 0 = no ')

needinfo = True
while needinfo:
    nplayers,nrounds,names,birthyears = getplayerinfo()
    # Print out a summary of players and dates of birth
    os.system('clear')
    print('These are the players for this game:')
    for i in range(nplayers):
        print(names[i] + ', born in ' + str(birthyears[i]))
    print(' ')
    print('You want to play ' + str(nrounds) + ' rounds')
    print(' ')
    correctinput = raw_input('Is this correct? Yes/No? ')

    while correctinput not in ['Yes','yes']:
        if correctinput in ['No','no']:
            names = []
            birthyears = [] 
            print('Ok, let\'s try again')
            break
        else:
            correctinput = raw_input('I\'m sorry, I didn\'t understand that. Is the game information correct, please enter Yes or No ')
    else:
        needinfo=False


# Each user gets a set of indices for the events
ievents = []

os.system('clear')

maxchecks = nevents*2

#let's try adding the climate indices before entering the loop!
# if there's not at least a 20 year gap in age, then use an historical reference point to associate to the first date. 
#  i.e. Washington statehood, Gold Rush, Railroads, Hindenberg, women's suffrage, Spruce Goose, World's fair in Seattle, issaquah mining boom
# add closing of washington mines

# Loop over each user
next = []
for j in range(0,nrounds):
    for k in range(0,nplayers):
        # Determine the filter and selection of events
        check = True
        itcheck = 0
        while check:
            ind = randint(0,nevents-1)
            #check that the date is appropriate and index is unused
            if birthyears[k] + earliestAge < events['start year'][ind]:
                if ind not in ievents:
                    check = False
                    ievents.append(ind)
            itcheck += 1
            if itcheck > maxchecks:
                exit('I\'m sorry, we\'ve run out of events for your group!')

        # display event, ask questions
        iyear = events['start year'][ind] - birthyears[k]
        print('In the year ' + names[k] + ' turned ' + str(iyear) + ' ' + events['description'][ind])
        print(' ')
        # Have count-down time before prompting
        time.sleep(delayinseconds)
        raw_input('Press enter when you are ready to move on to the next question?')
        os.system('clear')

# At the end, talk about the growth in renerable energy
# add the time series of CFC's to discuss the success of the montreal protocol
# add time series of sulfate particles so discuss the success of the clean air act


