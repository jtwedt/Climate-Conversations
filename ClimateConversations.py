import pdb
# THis is the stub program

# Load the events database RACHEL

# Get input from user (name, birthdate, number of rounds) JUDY
print('Welcome! Lets get a little information before we start the conversation.')
nplayers  = input('How many people are in the conversation? ')
nrounds = input('How many rounds would you like to play? ')
names = []
birthyears = []

indices = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th']
for i in range(nplayers):
    thisname = raw_input('Please enter the ' + indices[i] + ' players name: ')
    thisage = input('Please enter the '+ indices[i] + ' players year of birth: ')
    names.append(thisname)
    birthyears.append(thisage)

# Loop over each user
for j in nrounds:
    for k in nplayers:
        # Determine the filter and selection of events
        # display event, ask questions
