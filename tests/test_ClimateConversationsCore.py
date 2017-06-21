from datetime import datetime
from ClimateConversationsCore import Conversation, Player

class TestConversationWithSetup:
    '''
    Test Conversation class constructor.
    '''
    def setUp(self):
        p = [Player("First player", 1980),
                   Player("Second player", 1998)]
        self.c = Conversation(n_rounds = 3, players=p,
                         events_file="tests/gdrive_frozen_20171706.xlsx") 

    def tearDown(self):
        pass

    def test_initial_n_players(self):
        assert self.c.n_players == 2

    def test_n_players_after_removal(self):
        self.c.remove_player("First player", 1980)
        assert self.c.n_players == 1

    def test_n_players_after_add(self):
        p = Player("Third player", 1990)
        self.c.add_player(p)
        assert self.c.n_players == 3

    def test_valid_players(self):
        current_year = datetime.now().year
        for p in self.c.players:
            assert len(p.name) > 0
            assert 1910 < p.birth_year < (current_year - self.c.min_q_age)

    def test_reject_duplicate_player(self):
        p = Player("First player", 1980)
        assert self.c.add_player(p) == False
        assert self.c.n_players == 2

    def test_game_is_active(self):
        assert self.c.game_is_active()
    
    def test_game_becomes_inactive(self):
        while self.c.increment_player():
            pass
        assert not self.c.game_is_active()

    # def test_restart_game(self):
    #     assert False

    # def test_increment_player(self):
    #     assert False

    # def test_check_for_image(self):
    #     assert False

    # def test_check_for_extra_info(self):
    #     assert False

    # def test_get_question_with_questions_left(self):
    #     assert False

    # def test_get_question_with_no_questions_left(self):
    #     assert False

    # def test_get_event_with_events_left(self):
    #     assert False

    # def test_get_event_player_too_young_for_all(self):
    #     # Add young player (older than min age + )
    #     assert False
    
    # def test_get_event_none_left(self):
    #     assert False

    # def test_(self):
    #     assert False


class TestConversationWithoutSetup:
    ''' Conversation does not get regenerated for every test.
    '''
    p = [Player("First player", 1980),
         Player("Second player", 1998)]
    c = Conversation(n_rounds = 3, players=p, 
        events_file="tests/gdrive_frozen_20171706.xlsx")

    def test_remove_nonexisting_player(self):
        assert not self.c.remove_player("Not a player", 1991)

    def test_remove_existing_player(self):
        assert self.c.remove_player("First player", 1980)
        for p in self.c.players:
            # Must check both since a player does not need a unique name or byear
            assert p.name is not "First player" and p.birth_year is not 1980

    def test_add_player(self):
        p = Player("Third player", 1974)
        assert self.c.add_player(p)
        new_p = self.c.players[-1]
        assert new_p.name is "Third player"
        assert new_p.birth_year is 1974

    # def test_add_player_under_min_age(self):
    #     assert False
        
    # def test_get_question_invalid_event_idx(self):
    #     assert False

    # def test_choose_general_question(self):
    #     assert False





class TestConversationWithGDrive:
    '''
    Links to live google drive version of question set. This will break if the 
    spreadsheet format is changed so that it is not compatible with the game.
    Initially loads the local file & then tests the remote file for isolation.
    '''
    def setUp(self):
        p = [Player("First player", 1980),
                   Player("Second player", 1998)]
        self.c = Conversation(n_rounds = 3, players=p,
                    events_file="tests/gdrive_frozen_20171706.xlsx")

    def test_load_gdrive(self):
        self.c.load_events_from_gdrive(gdrive_key="1fiI18O4inR-Pm7XFnFitCrbfoGjXpZX_D_On348y4j8")
