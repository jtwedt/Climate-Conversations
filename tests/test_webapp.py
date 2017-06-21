import play_webapp as cc
from flask import Flask
from flask_testing import TestCase, LiveServerTestCase
import urllib2

class TestApp(TestCase):

    render_templates = False

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()

    def create_app(self):
        app = cc.app
        app.config['TESTING'] = True
        app.secret_key = 'test key'
        return app

    def tearDown(self):
        cc.game_cache = {}

    def test_assert_main_template_used(self):
        response = self.client.get("/")
        self.assert_template_used('index.html')
        assert response.status_code == 200
        assert len(cc.game_cache) == 0

    def test_assert_setup_template_used(self):
        response = self.client.get("/setup")
        self.assert_template_used('setup.html')
        assert response.status_code == 200
        assert len(cc.game_cache) == 0

    def post_setup_form(self):
        response = self.client.post("/setup/save", data=dict(
            name_p1="Test user",
            birthyear_p1=1980,
            num_rounds=1,
            ), follow_redirects=True)
        return response

    def test_assert_setup_save_redirect(self):
        response = self.post_setup_form()
        self.assert_template_used('play.html')
        assert response.status_code == 200
        assert len(cc.game_cache) == 1

    def test_assert_play_game_uninitiated(self):
        response = self.client.get("/play")
        self.assert_template_used('setup.html')
        assert response.status_code == 200
        assert len(cc.game_cache) == 0
        
    def test_assert_play_game_initial_response(self):
        _ = self.post_setup_form()
        response = self.client.get("/play")
        self.assert_template_used('play.html')
        assert response.status_code == 200
        assert len(cc.game_cache) == 1

    def test_assert_end_template_used(self):
        response = self.client.get("/feedback")
        self.assert_template_used('feedback.html')
        assert response.status_code == 200


class MyTest(LiveServerTestCase):

    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()

    def create_app(self):
        app = cc.app
        app.config['TESTING'] = True
        app.config['LIVESERVER_PORT'] = 0 # Set port to 0 to let flask choose
        app.config['LIVESERVER_TIMEOUT'] = 10
        app.secret_key = 'test key'
        return app

    def test_server_is_up_and_running(self):
        response = urllib2.urlopen(self.get_server_url())
        self.assertEqual(response.code, 200)

