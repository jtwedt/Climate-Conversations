import datetime
import calendar
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

    # Minimum player age we will ask events about
    minimum_age = 7

    class Event(object):
        def __init__(self, description, questions,
                     start=None, additional_info=None):
            self.description = description
            self.questions = questions
            self.start = start
            self.additional_info = additional_info

        @classmethod
        def new_from_csv_row(cls, row):
            """
            Event factory from a dict representing a row from the CSV database
            """
            description = row.get('description')
            additional_info = row.get('additional description')

            # Extract questions into a list
            keys = ['example question %d' % i for i in range(1, 4)]
            # Collect all the text non-blank questions, excluding NaN and blank
            # strings
            questions = [row.get(k) for k in keys
                         if type(row.get(k)) is unicode
                         and row.get(k).strip()]

            # Build a date object from start year and start month, assume first
            # day of month and January if no month is specified
            # Ideally we would move to using YYYY-MM-DD dates
            start_year = row.get('start year')
            start_month = row.get('start month', 'January')
            start_month_number = cls._month_name_to_number.get(start_month, 1)
            start = datetime.date(start_year, start_month_number, 1)

            return cls(description, questions,
                       start=start, additional_info=additional_info)
        # Lookup table for parsing month names
        _month_name_to_number = {v: k for k, v in
                                 enumerate(calendar.month_name)}

        def format_for_player(self, player):
            age = player.get_age_in_year(self.start.year)
            description = ("In the year {name} turned {age}, "
                           "{event}").format(name=player.name,
                                             age=age,
                                             event=self.description)

            return description

        def get_question(self, q_idx):
            return self.questions[q_idx]

    def __init__(self, events):
        self.events = events

    def pick_for_player(self, player):
        """
        Returns a event index and event tuple appropriate for the given player
        """
        cutoff_year = player.birth_year + self.minimum_age

        events = [(i, e) for i, e in enumerate(self.events)
                  if e.start.year >= cutoff_year]

        return random.choice(events)

    def get_event(self, e_idx):
        return self.events[e_idx]

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
        gdrive_url = ("https://docs.google.com/spreadsheet/ccc?key={}"
                      "&output=csv").format(gdrive_key)

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
            event_dict = {c: dataframe[c][i] for c in column_names}

            event = cls.Event.new_from_csv_row(event_dict)
            events.append(event)

        return cls(events)


class Player(object):
    def __init__(self, name, birth_year):
        self.name = name
        self.birth_year = int(birth_year)

    def __str__(self):
        return "{} (b: {!s})".format(self.name, self.birth_year)

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
        """
        Assign questions to players for all rounds
        """

        # List of 3-tuples representing player index, event index and
        # question index for each question in the game
        questions = list()

        # Set of event indexes which we have used
        used_events = set()

        player_questions = dict()

        # Assign events to players from youngest to oldest so we don't run
        # out of events for the younger players
        for p_idx, p in sorted(enumerate(players), reverse=True,
                               key=lambda p: p[1].birth_year):
            player_questions[p_idx] = list()
            retries = 0
            while len(player_questions[p_idx]) < rounds and retries < 10:
                try:
                    e_idx, e = event_store.pick_for_player(p)

                    if e_idx not in used_events:
                        p_questions = [(p_idx, e_idx, q_idx) for q_idx, q
                                       in enumerate(e.questions)]
                        player_questions[p_idx].append(p_questions)
                        used_events.add(e_idx)
                    else:
                        retries += 1
                except IndexError:
                    retries += 1

        for r_idx in range(rounds):
            for p_idx, p in enumerate(players):
                q = player_questions[p_idx].pop(0)
                questions.extend(q)

        return cls(event_store, players, questions)

    def game_is_active(self):
        return self.questions != []

    def get_next_question(self):
        if not self.questions:
            return

        q_tuple = self.questions.pop(0)
        p_idx, e_idx, q_idx = q_tuple

        player = self.players[p_idx]

        event = self.event_store.get_event(e_idx)

        # XXX(dlundquist): completely violating principle of encapsulation
        # by reaching into EventStore (above) and Event classes. This will
        # be easier to fix once events or more normalized

        # A design decision should be made on return value of this
        # function, do we return Player, Event and Question?!? objects or
        # strings of Player name, event description and question?

        return player, event, event.get_question(q_idx)
