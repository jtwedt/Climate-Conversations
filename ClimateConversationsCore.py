import datetime
import math
import pandas as pd
import random
import sys


reload(sys)
sys.setdefaultencoding('utf8')


class EventStore(object):
    """
    EventStore is an immutable ordered set of Events
    Conversations refer to events by index
    """

    class Event(dict):
        # TODO(dlundquist): migrate this a more structured format
        pass

        def pick_question(self, player):
            # FIXME(dlundquist): reimplement multiple question handling
            return 0

    def __init__(self, events):
        self.events = events

    def pick_for_player(self, player):
        """
        Returns a event index appropriate for the given player
        """
        # FIXME(dlundquist): actually consider the player's birth year
        e_idx = random.randrange(0, len(self.events))
        event = self.events[e_idx]

        return (e_idx, event.pick_question(player))

    @classmethod
    def load_from_gdrive(cls, gdrive_key):
        """
        EventStore factory which loads events from Google Drive

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
        """
        gdrive_url = "https://docs.google.com/spreadsheet/ccc?key=" + \
                     gdrive_key + "&output=csv"

        # header keeps changing
        events_df = pd.read_csv(gdrive_url, encoding='utf-8', skiprows=1)

        return cls._import_pandas_dataframe(events_df)

    @classmethod
    def load_from_excel(cls, events_file):
        """
        EventStore factory which loads events from a local Excel file
        """
        xlsx = pd.ExcelFile(events_file, header=2)
        events_df = xlsx.parse(xlsx.sheet_names[0], header=1)

        return cls._import_pandas_dataframe(events_df)

    @classmethod
    def _import_pandas_dataframe(cls, dataframe):
        """
        Convert pandas data frame into a list of Event objects
        """
        column_names = list(dataframe.columns)
        events = []
        for i in range(len(dataframe[column_names[0]])):
            event_dict = {}

            for c in column_names:
                event_dict[c] = dataframe[c][i]

            event = cls.Event(event_dict)
            events.append(event)

        return cls(events)


class Player(object):
    def __init__(self, name, birth_year):
        self.name = name
        self.birth_year = birth_year

    def __str__(self):
        return self.name + " (b: " + str(self.birth_year) + ")"

    def get_age_in_year(self, year):
        return year - self.birth_year

    def get_current_age(self):
        current_year = datetime.datetime.now().year
        return math.floor(current_year - self.birth_year)


class Conversation(object):
    """
    Represents a single game instance
    Can be serialized and deserialized from session cookies
    """
    def __init__(self, event_store, players, questions):
        # The event store object
        self.event_store = event_store
        # A list of players in this game
        self.players = players
        # A list of tuples indicating the player index, event index and
        # question index of remaining questions in this game
        self.questions = questions

    def to_session_cookies(self):
        return {
            'convo_players': [(p.name, p.birth_year) for p in self.players],
            'convo_questions': self.questions
        }

    @staticmethod
    def session_cookie_keys():
        """
        Returns a list of session cookie keys used to store a
        conversation, used to logout/end current game
        """
        return ['convo_players', 'convo_questions']

    @classmethod
    def load_from_session(cls, event_store, session):
        player_tuples = session.get('convo_players')
        players = [Player(p[0], p[1]) for p in player_tuples]
        questions = session.get('convo_questions')

        return cls(event_store, players, questions)

    @classmethod
    def new_conversation(cls, event_store, players, rounds):
        # Assign questions to players for all rounds
        questions = []
        for r_idx in range(rounds):
            for p_idx, p in enumerate(players):
                e_idx, q_idx = event_store.pick_for_player(p)
                # FIXME(dlundquist): check if this is a duplicate
                # questions and multiple questions per event
                question = (p_idx, e_idx, q_idx)
                questions.append(question)

        return cls(event_store, players, questions)

    def game_is_active(self):
        return self.questions != []

    def get_next_question(self):
        if not self.questions:
            return

        q_tuple = self.questions.pop(0)
        p_idx, e_idx, q_idx = q_tuple

        player = self.players[p_idx]

        # XXX(dlundquist): we should delegate these to event store and
        # event
        event = self.event_store.events[e_idx]

        # XXX(dlundquist): completely violating principle of encapsulation
        # by reaching into EventStore (above) and Event classes. This will
        # be easier to fix once events or more normalized

        # A design decision should be made on return value of this
        # function, do we return Player, Event and Question?!? objects or
        # strings of Player name, event description and question?

        return player, event['description'], event['example question 1']
