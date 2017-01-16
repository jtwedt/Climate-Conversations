import os
import time

from utils import *
from ClimateConversationsCore import Conversation, Player


## For now, define some raw user input functions
def get_player_info(test=0):
    if test == 1:
        n_players = 2
        n_rounds = 2
        p1 = Player("Judy", 1982)
        p2 = Player("Rachel", 1986)
    else:
        n_players = input('How many people are in the conversation? ')
        n_rounds = input('How many rounds would you like to play? ')
        players = []

        for i in range(n_players):
            name = raw_input('Please enter the ' + ordinal(i+1) + ' players name: ')
            birth_year = None

            while birth_year is None:
                year_input = raw_input('Please enter ' + name + '\'s year of birth: ')
                valid_year = validate_birth_year(year_input, min_age=10)
                if valid_year:
                    birth_year = valid_year
                else:
                    print "Please enter a valid birth year, for example, 1980."
            players.append(Player(name, birth_year))

    return [players, n_rounds]

def setup_game():
    ready_to_play = False
    while not ready_to_play:
        players, n_rounds = get_player_info()
        os.system("clear")
        print "These are the players for this game: "
        for player in players:
            print player
        print "\nYou want to play", n_rounds, "rounds\n"

        correct_input = raw_input('Is this correct? Yes/No? ')
        if correct_input not in ['Yes','yes','y', 'Y']:
            if correct_input in ['No','no', 'n', 'N']:
                print('Ok, let\'s try again')
            else:
                correct_input = raw_input('I\'m sorry, I didn\'t understand that. Is the game information correct, please enter Yes or No ')
        else:
            print "Great, let's play!"
            ready_to_play = True

    return [players, n_rounds]

def load_questions(game, players, n_rounds):
    questions = []
    for round_i in range(n_rounds):
        for player in players:
            p = game.get_current_player()
            q = game.get_next_question(p)
            if q is None:
                print "Warning: out of questions for your group and the number of rounds. Returning what we have so far!"
                return questions
            questions.append(q)
            game.increment_player()
    return questions


def main():
    print "Welcome! Lets get a little information before we start the conversation."
    test  = input('Is this a test run? 1 = yes, 0 = no ')

    if test:
        players = [Player("Judy", 1982), Player("Rachel", 1986)]
        n_rounds = 10
    else:
        players, n_rounds = setup_game()


    game = Conversation(n_rounds=n_rounds, 
                        players=players, 
                        min_age_to_play=7,
                        events_file="data/firstHistoricClimateEvents.xlsx",
                        min_q_age=10)

    questions = load_questions(game, players, n_rounds)

    delay_in_seconds = 1

    for q in questions:
        os.system('clear')
        print q
        time.sleep(delay_in_seconds)
        raw_input("\nPress enter when you are ready to move on to the next prompt.")
    
    print "\nThat's all! Thanks for playing."


if __name__ == '__main__':
    main()