import pdb
import pandas as pd
import time

# This is the stub program

# Load the events database RACHEL

xlsx = pd.ExcelFile('firstHistoricClimateEvents.xlsx')
df = xlsx.parse(xlsx.sheet_names[0])
events = df.to_dict()
#print events.keys()    # We may want to change some of the key names to be more efficient for indexing!

# Get input from user (name, birthdate, number of rounds) JUDY
print('Welcome! Lets get a little information before we start the conversation.')
nplayers  = input('How many people are in the conversation? ')
nrounds = input('How many rounds would you like to play? ')
names = []
birthyears = []

# Work out how long to delay between questions
delayinseconds = 5

indices = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th']
for i in range(nplayers):
    thisname = raw_input('Please enter the ' + indices[i] + ' players name: ')
    thisage = input('Please enter the '+ indices[i] + ' players year of birth: ')
    names.append(thisname)
    birthyears.append(thisage)

# Loop over each user
next = []
for j in range(0,nrounds):
    for k in range(0,nplayers):
        # Determine the filter and selection of events
        # display event, ask questions
        print('here is your question')

        # Have count-down time before prompting
        time.sleep(delayinseconds)
        raw_input("You've been talking about this question for " + str(delayinseconds / 60) + " minutes, press enter when you are ready to move on to the next question?")

