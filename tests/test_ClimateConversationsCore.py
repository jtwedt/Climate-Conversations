from ClimateConversationsCore import Conversation, EventStore, Player

'''
Missing tests according to coverage calculation:

* No events file specified
* Data has no question columns
* No valid events in Data
* General question with %d in it
* General question not specifying year
* Dataset w/ just 1 question col
* Increment player w/ no active game
* Get player's current age
* Already asked player q's
'''


class TestEventStore(object):
    def test_empty_event_store(self):
        events = []
        es = EventStore(events)
        assert es.events == []

    def test_new_from_excel(self):
        es = EventStore.load_from_excel("tests/gdrive_frozen_20172806.xlsx")
        assert es.events


class TestConversationWithSetup:
    '''
    Test Conversation class constructor.
    '''
    def setUp(self):
        es = EventStore.load_from_excel("tests/gdrive_frozen_20172806.xlsx")
        p = [Player("First player", 1980),
             Player("Second player", 1998)]
        self.c = Conversation(es, p, 3)

    def tearDown(self):
        pass

#    def test_initial_n_players(self):
#        assert self.c.n_players == 2

#    def test_n_players_after_removal(self):
#        self.c.remove_player("First player", 1980)
#        assert self.c.n_players == 1

#    def test_n_players_after_add(self):
#        p = Player("Third player", 1990)
#        self.c.add_player(p)
#        assert self.c.n_players == 3

#    def test_valid_players(self):
#        current_year = datetime.now().year
#        for p in self.c.players:
#            assert len(p.name) > 0
#            assert 1910 < p.birth_year < (current_year - self.c.min_q_age)

#    def test_reject_duplicate_player(self):
#        p = Player("First player", 1980)
#        assert self.c.add_player(p) is False
#        assert self.c.n_players == 2

    def test_game_is_active(self):
        assert self.c.game_is_active()

#    def test_game_becomes_inactive(self):
#        while self.c.increment_player():
#            pass
#        assert not self.c.game_is_active()

#    def test_restart_game(self):
#        # TODO make this play some rounds and then make sure the q's are still
#        # there
#        while self.c.game_is_active():
#            self.c.increment_player()
#            p = self.c.get_current_player()
#            self.c.get_next_event(p)
#        assert not self.c.game_is_active()
#        self.c.restart_game(repeats_allowed=False)
#        assert self.c.game_is_active()
#        assert self.c.rounds_left == 3
#        assert len(self.c.asked_events) > 0
#
#        self.c.restart_game()
#        assert self.c.game_is_active()
#        assert self.c.rounds_left == 3
#        assert len(self.c.asked_events) == 0

#    def test_initial_current_player(self):
#        assert self.c.current_player_idx == 0

#    def test_increment_player_once(self):
#        assert self.c.current_player_idx == 0
#        self.c.increment_player()
#        assert self.c.current_player_idx == 1

#    def test_increment_player(self):
#        # 3 rounds, 2 players
#        for round_no in range(self.c.n_rounds):
#            for p_no in range(self.c.n_players):
#                assert self.c.current_player_idx == p_no
#                self.c.increment_player()
#        assert self.c.current_player_idx is None

#    def test_get_question_with_questions_left(self):
#        p = self.c.get_current_player()
#        e_idx, e = self.c.get_next_event(p)
#        q = self.c.get_question(e_idx)
#        assert q is not None

#    def test_get_three_questions_individually(self):
#        p = self.c.get_current_player()
#        e_idx, e = self.c.get_next_event(p)
#        for _ in range(3):
#            q = self.c.get_question(e_idx)
#            assert q is not None
#
#        q = self.c.get_question(e_idx)
#        assert q is None

#    def test_get_question_with_no_questions_left(self):
#        # Run through all players so we have no questions left
#        for round_no in range(self.c.n_rounds):
#            for p_no in range(self.c.n_players):
#                self.c.increment_player()
#
#        p = self.c.get_current_player()
#        e_idx, e = self.c.get_next_event(p)
#        q = self.c.get_question(e_idx)
#        assert q is None

#    def test_get_event_with_events_left(self):
#        p = self.c.get_current_player()
#        e_idx, e = self.c.get_next_event(p)
#        assert e_idx is not None
#        assert e is not None

    # def test_get_event_player_too_young_for_all(self):
    #     # Add young player (older than min age + )
    #     assert False

#    def test_get_event_none_left(self):
#        for round_no in range(self.c.n_rounds):
#            for p_no in range(self.c.n_players):
#                self.c.increment_player()
#
#        p = self.c.get_current_player()
#        e_idx, e = self.c.get_next_event(p)
#        assert e_idx is None
#        assert e is None

    # def test_(self):
    #     assert False


class TestConversationWithoutSetup(object):
    ''' Conversation does not get regenerated for every test.
    '''
    es = EventStore.load_from_excel("tests/gdrive_frozen_20172806.xlsx")
    p = [Player("First player", 1980),
         Player("Second player", 1998)]
    c = Conversation(es, p, 3)

#    def test_add_player(self):
#        p = Player("Third player", 1974)
#        assert self.c.add_player(p)
#        new_p = self.c.players[-1]
#        assert new_p.name is "Third player"
#        assert new_p.birth_year is 1974

#    def test_check_for_image(self):
#        assert self.c.check_for_image(1) is not None
#        assert self.c.check_for_image(2) is None

#    def test_check_for_extra_info(self):
#        assert self.c.check_for_extra_info(6) is not None
#        assert self.c.check_for_extra_info(5) is None

    # def test_add_player_under_min_age(self):
    #     assert False

#    def test_get_question_invalid_event_idx(self):
#        assert self.c.get_question(-1) is None
#        assert self.c.get_question(999) is None

#    def test_choose_general_question(self):
#        assert self.c.choose_general_question(e_year=1950) is not None
#        assert self.c.choose_general_question(e_year=2000) is not None


class TestConversationWithGDrive:
    '''
    Links to live google drive version of question set. This will break if the
    spreadsheet format is changed so that it is not compatible with the game.
    Initially loads the local file & then tests the remote file for isolation.
    '''
    def setUp(self):
        es = EventStore.load_from_excel("tests/gdrive_frozen_20172806.xlsx")
        p = [Player("First player", 1980),
             Player("Second player", 1998)]
        self.c = Conversation(es, p, 3)

#    def test_load_gdrive(self):
#        self.c.load_events_from_gdrive(
#                gdrive_key="1fiI18O4inR-Pm7XFnFitCrbfoGjXpZX_D_On348y4j8")
