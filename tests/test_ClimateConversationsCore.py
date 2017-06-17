from datetime import datetime
from ClimateConversationsCore import Conversation, Player

class TestConversation:
    '''
    Test Conversation class constructor.
    '''
    def setUp(self):
        p = [Player("First player", 1980),
                   Player("Second player", 1998)]
        self.c = Conversation(n_rounds = 3, players=p,
                         gdrive_key="1fiI18O4inR-Pm7XFnFitCrbfoGjXpZX_D_On348y4j8") 

    def tearDown(self):
        pass


    def test_attr_n_players(self):
        assert self.c.n_players == 2

    def test_attr_players(self):
        current_year = datetime.now().year
        for p in self.c.players:
            assert len(p.name) > 0
            assert 1910 < p.birth_year < (current_year - self.c.min_q_age)
        pass

    def test_fn_remove_player(self):
        assert not self.c.remove_player("Not a player", 1991)

    def test_remove_player(self):
        assert self.c.remove_player("First player", 1980)
        for p in self.c.players:
            # Must check both since a player does not need a unique name or byear
            assert p.name is not "First player" and p.birth_year is not 1980
        assert self.c.n_players == 1

    def test_add_player(self):
        p = Player("Third player", 1974)
        self.c.add_player(p)
        assert self.c.n_players == 3
        new_p = self.c.players[2]
        assert new_p.name is "Third player"
        assert new_p.birth_year is 1974

    def test_game_is_active(self):
        assert self.c.game_is_active()
        # p = self.c.get_current_player()
        # e_idx, e = self.c.get_next_event(p)
        # q = self.c.get_question(e_idx)
        # while p:
        #     print p, e_idx, q
        #     p = self.c.get_current_player()
        #     e_idx, e = self.c.get_next_event(p)
        #     q = self.c.get_question(e_idx)
        # assert not self.c.game_is_active()



    def test_case_3(self):
        pass