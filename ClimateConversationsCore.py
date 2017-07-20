import sys
import pandas as pd
import os
import numpy as np
from random import randint
import datetime
import math


reload(sys)
sys.setdefaultencoding('utf8')


class Conversation():

    def __init__(self,
                 n_rounds=5,
                 events_file=None,
                 gdrive_key=None,
                 general_q_file="data/general_questions.txt",
                 players=None,
                 min_q_age=10):
        self.n_rounds = n_rounds
        """Total number of rounds to be played during the game. This should not
        typically be changed during the game (see `rounds_left` instead)."""
        self.rounds_left = n_rounds
        """Number of rounds remaining in the game. Initially equal to
        `n_rounds`; depletes to 0 as the game goes on."""
        self.asked_events = []
        """List of indices of events that have already been played."""
        self.current_player_idx = 0
        """Index of the current player in the game. Note that this index is
        specific to the list of players, not the players themselves, so if a
        player is removed from the game, the indices will change relative to
        that removal."""

        if gdrive_key:
            self.events = self.load_events_from_gdrive(gdrive_key)
        elif events_file:
            self.events = self.load_events_from_excel(events_file)
        else:
            raise ValueError("Error: need to specify an events file "
                             "(google drive or local spreadsheet).")
        self.remaining_events = list(self.events.index)
        """List of indices of remaining events. Intially populated with all
        indices in the events database."""

        self.n_events = len(self.events['description'])
        """Total number of events in the original events database."""
        if players is not None:
            self.players = players
            """List of Player objects representing people playing the game."""
            self.n_players = len(self.players)
            """Number of players currently in the game."""

        self.min_q_age = min_q_age
        """\"You must be this tall to ride this ride.\" -- Players won't be
        asked questions about events that happened before they are this old."""
        self.gen_questions = list(pd.read_table(general_q_file, comment="#",
                                                header=None)[0])
        """List of general questions that could be asked in the context of any
        event."""
        self.q_colnames = self._find_question_cols()
        """List of column names that contain questions,
        e.g. \"example question 1\"."""
        self.active_game = True
        """Value is False when there are no more valid questions for the
        players or there are no more rounds."""
        self.current_e_idx = None

    def load_events_from_excel(self, events_file):
        '''
        Load event spreadsheet from an excel file.

        ## TODO write expected format here

        **Input**: filename of excel spreadsheet

        **Output**: dataframe of events
        '''
        xlsx = pd.ExcelFile(events_file, header=2)
        events = xlsx.parse(xlsx.sheet_names[0], header=1)
        events['asked'] = ""
        return events

    def load_events_from_gdrive(self, gdrive_key):
        '''
        Load event spreadsheet directly from google drive.

        ## TODO document expected format here

        **Input**: gdrive key

        **Output**: dataframe of events

          The `gdrive_key` is the code in the URL after `../spreadsheets/d/`
          Example: `https://docs.google.com/spreadsheets/d/
                    1sjO-EcVfFZR8aJIT7br3UxYSmsVpoPAjPzmdNHToaXg/edit#gid=630120060`

          The key for the above url would be
            "`1sjO-EcVfFZR8aJIT7br3UxYSmsVpoPAjPzmdNHToaXg`"

          You can get this via the "Share" button -> "get shareable link"
            in Google sheets.
        '''
        gdrive_url = "https://docs.google.com/spreadsheet/ccc?key=" + \
                     gdrive_key + "&output=csv"

        # header keeps changing
        events = pd.read_csv(gdrive_url, encoding='utf-8', skiprows=1)
        events['asked'] = ""
        return events

    def _find_question_cols(self):
        """
        Search the events database column names for the question columns.
        This function will change as the events database evolves.

        **Returns:** list of column names of questions in `self.events`
        """
        assert self.events is not None
        columns = self.events.columns
        q_cols = [c for c in columns if "question" in c]
        if len(q_cols) == 0:
            q_cols = None
        return q_cols

    def game_is_active(self):
        """
        Call this function to check if the game can still be played.

        The variable `game_is_active` will be set to False when there are no
        more valid questions for the players or there are no more rounds.
        """
        return self.active_game

    def event_is_active(self):
        """
        Call this function to check if the current player has an active event.
        This will return True as long as the last call to get a question
        actually returned a question.

        This does not guarantee that another question exists. This just tells
        us that it is okay to ask the game for a question, otherwise, we need
        to get a new player and a new event.
        """
        return self.current_e_idx is not None

    def add_player(self, player):
        for p in self.players:
            if p.name == player.name and p.birth_year == player.birth_year:
                return False
        self.players.append(player)
        self.n_players += 1
        return True

    def remove_player(self, player_name, player_birthyear):
        for player in self.players:
            if player_name == player.name and \
                    player_birthyear == player.birth_year:
                self.players.remove(player)
                self.n_players -= 1
                self.current_player_idx -= 1
                return True
        return False

    def get_current_player(self):
        if self.n_players == 0 or self.rounds_left <= 0 or \
                self.current_player_idx >= self.n_players:
            return None
        else:
            return self.players[self.current_player_idx]

    def get_next_event(self, player):
        if player is None:
            return None, None

        # Randomly choose an event, but make sure:
        #   a) we haven't already discussed the event in this game
        #   b) the date of the event makes sense given their age
        e_idx = randint(0, self.n_events-1)
        min_year = player.birth_year + self.min_q_age

        valid_events_by_birthyear = self.events[self.events['start year'] >
                                                min_year].index
        valid_events = valid_events_by_birthyear.intersection(
                self.remaining_events)

        if len(valid_events) == 0:
            return None, None

        e_idx = int(np.random.choice(valid_events))

        player.asked_events.append(e_idx)
        self.asked_events.append(e_idx)
        self.remaining_events.remove(e_idx)

        e_desc = self.events['description'][e_idx]
        e_desc = e_desc.encode('utf-8').strip()
        e_age = player.get_age_in_year(int(self.events['start year'][e_idx]))

        # Return formatted string
        e = "In the year %s turned %d, %s" % (player.name, e_age, e_desc)
        self.current_e_idx = e_idx
        self.current_event = e
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
        """
        Retrieve the next question for the specified event, or return None if
        no question exists or is left. If no questions are left, then this
        function also sets the `current_e_idx` to None so we know that we need
        to choose a new event.

        **Input:** `e_idx`, the index of the desired event

        **Output:** The question formatted as a string.

        Note that question formatting (i.e. with a year/age) is currently not
        supported.  """
        if type(e_idx) is not int or e_idx < 0 or e_idx > self.n_events:
            return None

        e_year = self.events['start year'][e_idx]

        # If we have just one question column, assume it's the old db
        # aka get a random question
        if len(self.q_colnames) == 1:
            q = self.choose_general_question(e_year)
            return q

        # Otherwise, if we have more than 1 question column, assume it's the
        # database with 3 questions.
        else:
            for colname in self.q_colnames:
                q = self.events[colname][e_idx]
                if colname in list(self.events['asked'])[e_idx]:
                    continue
                else:
                    self.events.loc[e_idx, 'asked'] = \
                        self.events.loc[e_idx, 'asked'] + colname
                    return q

            self.current_e_idx = None
            return None

            # q1 = self.events["example question 1"][e_idx]
            # q2 = self.events["example question 2"][e_idx]
            # q3 = self.events["example question 3"][e_idx]

            # if q1.contains("asked"):
            #     #
            # else:
            #     self.events["example question 1"][e_idx] = "asked"
            #     q = q1

            # q = "<p>%s</p><br/><p>%s</p><br/><p>%s</p>" % (q1, q2, q3)

        # return q

    def check_for_extra_info(self, e_idx):
        try:
            q_info = self.events['additional description'][e_idx]
            if len(q_info) > 0:
                return q_info
            else:
                return None
        except:
            return None

    def check_for_image(self, e_idx):
        try:
            img_file = self.events['image filename'][e_idx]
            if os.path.isfile(img_file):
                return img_file
            else:
                return None
        except:
            return None

    def increment_player(self):
        """
        Updates `self.current_player_idx` if there are players left in the
        current round or there are more rounds to play.

        If there are no more rounds, set the `game_is_active` variable to False
        indicating that the game is over and return False.
        """
        p_idx = self.current_player_idx + 1
        # If we have not reached the end of the round, move to the next player
        # index
        if p_idx < self.n_players:
            self.current_player_idx = p_idx
            p = self.get_current_player()
        # If we have reached the end of the round, check if there are more
        # rounds
        elif p_idx >= self.n_players:
            # If there are more rounds to play, start from 1st player &
            # decrement the rounds left
            if self.rounds_left:
                self.rounds_left -= 1
                self.current_player_idx = 0
                p = self.get_current_player()
            # If there are no more rounds to play, we cannot increment the
            # player
            else:
                self.active_game = False
                self.current_player_idx = None
                return None
        if p:
            return p
        else:
            self.active_game = False
            self.current_player_idx = None
            return None

    def restart_game(self, repeats_allowed=True):
        """
        Reset the game
        **Input**:
        """
        # Reset number of rounds and possibly Q's that have already been asked
        self.rounds_left = self.n_rounds
        self.active_game = True
        if repeats_allowed:
            self.asked_events = []
            self.remaining_events = list(self.events.index)
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
        return math.floor(current_year - self.birth_year)

    def get_age_in_year(self, year):
        return year - self.birth_year

    def already_asked(self, event_i):
        return event_i in self.asked_events

    def __str__(self):
        return self.name + " (b: " + str(self.birth_year) + ")"
