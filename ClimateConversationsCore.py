import pandas as pd
import os
from random import randint
import datetime
import time
from utils import *
import math

class Conversation():
    min_age_to_play = 0 # Overall minimum age to play the game
    min_q_age = 0 # Don't ask Q's about events happening before the player is this old 

    def __init__(self, 
                 n_rounds=5,
                 events_file=None,
                 gdrive_key=None,
                 general_q_file="data/general_questions.txt",
                 min_age_to_play=7,
                 players=None,
                 min_q_age=10):
        self.n_rounds = n_rounds
        self.rounds_left = n_rounds
        self.min_age_to_play = min_age_to_play
        self.asked_events = []
        self.current_player_idx = 0

        if gdrive_key:
            self.events = self.load_events_from_gdrive(gdrive_key)
        elif events_file:
            self.events = self.load_events_from_excel(events_file)
        else:
            raise ValueError("Error: need to specify an events file (google drive or local spreadsheet).")

        self.n_events = len(self.events['description'])
        if players is not None:
            self.players = players
            self.n_players = len(self.players)
        self.max_checks = self.n_events**2
        self.min_q_age = min_q_age

        self.gen_questions = list(pd.read_table(general_q_file, comment="#", header=None)[0])
        self.q_colnames = self.find_question_cols()

    '''
    Load event spreadsheet from an excel file. 
    #TODO write format this should be in here
    Input: filename of excel spreadsheet
    Output: dictionary of events (keys: event id, values: event information)
    '''
    def load_events_from_excel(self, events_file):
        xlsx = pd.ExcelFile(events_file)
        df = xlsx.parse(xlsx.sheet_names[0])
        events = df.to_dict()
        return events

    '''
    Load event spreadsheet directly from google drive.
    Input: gdrive key
    Output: dictionary of events (keys: event id, values: event information)
      The gdrive_key is the code in the URL after ../spreadsheets/d/
      Example: https://docs.google.com/spreadsheets/d/1sjO-EcVfFZR8aJIT7br3UxYSmsVpoPAjPzmdNHToaXg/edit#gid=630120060
      The key for the above url would be "1sjO-EcVfFZR8aJIT7br3UxYSmsVpoPAjPzmdNHToaXg"
      You can get this via the "Share" button -> "get shareable link"
    '''
    def load_events_from_gdrive(self, gdrive_key):
        gdrive_url = "https://docs.google.com/spreadsheet/ccc?key=" + gdrive_key + "&output=csv"
        df = pd.read_csv(gdrive_url, encoding='utf-8', skiprows=1) # header keeps changing
        events = df.to_dict()
        return events

    def find_question_cols(self):
        assert self.events is not None
        columns = self.events.keys()
        q_cols = [c for c in columns if "question" in c]
        if len(q_cols) == 0:
            q_cols = None
        return q_cols

    def add_player(self, player):
        self.players.append(player)
        self.n_players += 1

    def remove_player(self, player_name, player_birthyear):
        for player in self.players:
            if player_name == player.name and player_birthyear == player.birth_year:
                self.players.remove(player)
                self.n_players -= 1
                self.current_player_idx -= 1
                return True
        return False

    def get_current_player(self):
        if self.n_players == 0:
            return None
        if self.rounds_left > 0:
            if self.current_player_idx >= self.n_players:
                self.current_player_idx = 0
                self.rounds_left -= 1
            return self.players[self.current_player_idx]
        else:
            return None

    # TODO: This should be optimized as there are more and more events
    # TODO: As more event types are added, split this into multiple functions
    #         Ideally, this would randomly choose the event type and event,
    #         and then maybe something else would format it.

    def get_next_event(self, player):
        # Figure out which player to ask

        # Randomly choose an event, but make sure:
        #   a) we haven't already discussed the event in this game
        #   b) the date of the event makes sense given their age
        e_idx = randint(0, self.n_events-1)
        n_checks = 1
        while (e_idx in self.asked_events \
           or int(self.events['start year'][e_idx]) - player.birth_year < self.min_q_age) \
           and n_checks < self.max_checks:
            e_idx = randint(0, self.n_events-1)
            n_checks += 1

        if n_checks >= self.max_checks:
            return None, None

        player.asked_events.append(e_idx)
        self.asked_events.append(e_idx)

        e_desc = self.events['description'][e_idx]
        e_desc = e_desc.encode('utf-8').strip()
        e_age = player.get_age_in_year(int(self.events['start year'][e_idx]))

        # Return question
        e = "In the year " + player.name + " turned " + str(e_age) + ", " + e_desc
        return e_idx, e

    ''' Randomly select a general question from the list.
    Input: e_year [None, year]
        if e_year is None: get any random string that does NOT require a year
    Output: str
        The string question, possibly containing the input year.
    '''
    def choose_general_question(self, e_year=None):
        if e_year is None:
            raise NotImplementedError
        else:
            q_idx = randint(0, len(self.gen_questions)-1)
            q = self.gen_questions[q_idx]
            if "%d" in q:
                q = q % e_year
            return q

    def get_question(self, e_idx):
        assert type(e_idx) is int

        e_year = self.events['start year'][e_idx]

        # If we have just one question column, assume it's the old db
        # aka get a random question
        if len(self.q_colnames) == 1:
            q = self.choose_general_question(e_year)

        # Otherwise, if we have more than 1 question column, assume it's the 
        # database with 3 questions.
        # For now, format it into one big long string with line breaks.
        else:
            q1 = self.events["example question 1"][e_idx]
            q2 = self.events["example question 2"][e_idx]
            q3 = self.events["example question 3"][e_idx]
            q = "%s\n\n%s\n\n%s" % (q1, q2, q3)

        return q  
        
    def check_for_extra_info(self, event_num):
        try:
            q_info = self.events['additional description'][event_num]
        except: 
            return None
        if q_info == "": 
            return None
        else: 
            return q_info

    def check_for_image(self, event_num):
        img_file = self.events['image'][event_num]

        if os.path.isfile(img_file):
            return img_file
        else:
            return None
       
    def increment_player(self):
        p_idx = self.current_player_idx + 1
        # If we have not reached the end of the round, move to the next player index
        if p_idx < self.n_players: 
            self.current_player_idx = p_idx
            return True
        # If we have reached the end of the round, check if there are more rounds
        elif p_idx >= self.n_players:
            # If there are more rounds to play, start from 1st player & decrement the rounds left 
            if self.rounds_left:
                self.rounds_left -= 1
                self.current_player_idx = 0
                return True
            # If there are no more rounds to play, we cannot increment the player
            else:
                print self.rounds_left
                return False

    def restart_game(self, repeats_allowed=True):
        # Reset number of rounds and possibly Q's that have already been asked
        self.rounds_left = self.n_rounds
        if repeats_allowed:
            for player in self.players:
                player.asked_events = []


class Player():
    name = ""
    birth_year = ""
    asked_events = []

    def __init__(self, name, birth_year):
        self.name = name
        self.birth_year = birth_year

    def get_current_age(self):
        current_year = datetime.datetime.now().year
        return floor(current_year - self.birth_year)

    def get_age_in_year(self, year):
        return year - self.birth_year

    def already_asked(self, event_i):
        return event_i in asked_events

    def __str__(self):
        return self.name + " was born in " + str(self.birth_year)
