import pandas as pd
import os
from random import randint
import datetime
import time
from utils import *

class Conversation():
    events = {}
    min_age_to_play = 0 # Overall minimum age to play the game
    min_q_age = 0 # Don't ask Q's about events happening before the player is this old
    n_rounds = 0
    n_events = 0
    players = []
    rounds_left = 0
    current_player_idx = 0
    max_checks = 100
    asked_events = []

    def __init__(self, 
                 n_rounds=5,
                 events_file="data/firstHistoricClimateEvents.xlsx",
                 min_age_to_play=7,
                 players=None,
                 min_q_age=10):
        self.n_rounds = n_rounds
        self.rounds_left = n_rounds
        self.min_age_to_play = min_age_to_play
        self.events = self.load_events_from_excel(events_file)
        self.n_events = len(self.events['description'])
        if players is not None:
            self.players = players
            self.n_players = len(self.players)
        self.max_checks = self.n_events*2
        self.min_q_age = min_q_age

    '''
    Load event spreadsheet from an excel file. 
    #TODO write format this should be in here
    Input: filename of excel spreadsheet
    Output: dictionary of events (keys: ___, values: ___)
    '''
    def load_events_from_excel(self, events_file):
        xlsx = pd.ExcelFile(events_file)
        df = xlsx.parse(xlsx.sheet_names[0])
        events = df.to_dict()
        return events

    def add_player(self, player):
        self.players.append(player)
        self.n_players += 1

    def get_current_player(self):
        if self.rounds_left > 0:
            if self.current_player_idx >= self.n_players:
                self.current_player_idx = 0
                self.rounds_left -= 1
            return self.players[self.current_player_idx]
        else:
            return None

    # TODO: This should be optimized as there are more and more questions
    # TODO: As more question types are added, split this into multiple functions
    #         Ideally, this would randomly choose the question type and question,
    #         and then maybe something else would format it.
    def get_next_question(self, player):
        # Figure out which player to ask
        # p = self.get_current_player()
        # print self.min_q_age
        # if p is None:
        #     return None

        # Randomly choose a Q, but make sure:
        #   a) we haven't already asked the question in this game
        #   b) the date of the event makes sense given their age
        q_idx = randint(0, self.n_events-1)
        n_checks = 1
        while (q_idx in self.asked_events \
           or int(self.events['start year'][q_idx]) - player.birth_year < self.min_q_age) \
           and n_checks < self.max_checks:
            q_idx = randint(0, self.n_events-1)
            n_checks += 1

        if n_checks >= self.max_checks:
            return None

        player.asked_events.append(q_idx)
        self.asked_events.append(q_idx)

        q_desc = self.events['description'][q_idx]
        #print "DEBUG: ", q_idx, q_desc
        q_desc = q_desc.encode('utf-8').strip()
        q_age = player.get_age_in_year(int(self.events['start year'][q_idx]))

        # Return the question
        q = "In the year " + player.name + " turned " + str(q_age) + ", " + q_desc
        return q_idx, q

    def check_for_extra_information(self, event_num):
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
