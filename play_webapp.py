# encoding=utf8  
import os, sys, logging
reload(sys)  
sys.setdefaultencoding('utf8')
from flask import Flask, session, request, render_template, url_for, redirect
from wtforms import Form, FieldList, FormField, StringField, IntegerField, validators
from logging.handlers import RotatingFileHandler
sys.path.insert(0, os.getcwd())
from ClimateConversationsCore import *

app = Flask(__name__)
game_cache = {}

class PlayerEntryForm(Form):
    pname = StringField('Name') # StringField vs TextField?
    byear = IntegerField('Birth year')

class SetupForm(Form):
    """A form for one or more addresses"""
    player_records = FieldList(FormField(PlayerEntryForm), min_entries=1)

#TODO 
# Format macro like orig. template
# Add buttun to save form info & add new field
# Add function to trigger when the abv button is pushed
# Break fns into separate files
# Add more fields byear
# Get player data from dict list instead of from named attrs
@app.route("/")
def main():
    return render_template('index.html')

@app.route("/setup")
def game_setup():
    test_records = [{"pname": "", "byear": ""},
                    {"pname": "", "byear": ""}]
    # test_records = []
    form = SetupForm(player_records=test_records)
    return render_template("setup.html", form=form)
    # return render_template("setup.html")

@app.route("/setup/save", methods=['POST'])
def save_game_setup():
    global game_cache
    form_data = request.form
    n_rounds = int(form_data.get("num_rounds"))
    app.logger.debug("Saved n_rounds: %d" % n_rounds)

    app.logger.debug(form_data)

    # Retrive raw form data
    player_raw_data = []
    for k,v in form_data.iteritems():
        app.logger.debug("key: " + k + " value: " +  v)
        if "pname" in k or "byear" in k:
            p_no = int(k.split("-")[1])
            short_k = k.split("-")[2]
            app.logger.debug("Extracted player no " + str(p_no))
        else:
            continue
        if len(player_raw_data) <= p_no:
            add_slots = p_no - len(player_raw_data) + 1
            player_raw_data = player_raw_data + [{} for _ in range(add_slots)]
        if "byear" in k:
            v = int(v) # TODO proper input validation
        player_raw_data[p_no][short_k] = v

    app.logger.debug(player_raw_data)

    # Create player objects
    players = []
    for p_data in player_raw_data:
        players.append(Player(p_data.get("pname"), p_data.get("byear")))

    player_string = "\n".join([str(p) for p in players])
    app.logger.info("Added players: \n%s" % player_string)

    # Generate a key to store the session in the game cache
    user_key = os.urandom(24)
    app.logger.info("Assigned session key: %s" % user_key)
    session['user_key'] = user_key 

    # Create the conversation
    app.logger.debug("Initializing conversation object.")
    convo = Conversation(n_rounds = n_rounds, players=players,
                        events_file="tests/gdrive_frozen_20172806.xlsx")
                         # gdrive_key="1fiI18O4inR-Pm7XFnFitCrbfoGjXpZX_D_On348y4j8") 
                         #gdrive_key="183SABhCyJmVheVwu_1rWzY7jOjvtyfbmG58ow321a3g") # Original set of 70ish questions
                         #events_file="data/firstHistoricClimateEvents.xlsx") # Locally stored copy
    app.logger.debug("Storing the conversation in the game cache using the generated key.")
    game_cache[user_key] = convo
    app.logger.debug("Done; returning the play route redirect.")

    return redirect("/play", code=302)


@app.route("/play")
def play_game():
    global game_cache
    
    app.logger.info("Loading convo from cache")
    user_key = session.get('user_key')
    if user_key is None:
        app.logger.debug("User key not set (no conversation to be retrieved). Redirecting to setup. This is probably not the best to do long-term but is ok for now.")
        return render_template("setup.html", form=SetupForm(player_records=["pname:" "ln 111"]))
    else:
        try:
            convo = game_cache.get(user_key)
            app.logger.debug("Successfully retrieved conversation")
        except:
            app.logger.info("User key not in game cache (no conversation to be retrieved). Redirecting to setup. This is probably not the best to do long-term but is ok for now.")
            return render_template("setup.html", form=SetupForm(player_records=["pname:" "ln 118"]))

    # Case: The game is out of rounds and/or questions
    if not convo.game_is_active():
        app.logger.info("Game returned False for convo.game_is_active(). Ending the game.")
        return end_game(user_key) 

    player = convo.get_current_player()
    app.logger.debug("Asked the game for a player, got: %s" % str(player))

    # Case: Game returned 'None' for the player.
    #       This usually means that we ran out of rounds, so we end.
    if player is None:
        app.logger.debug("No player returned, although the game was still active. Ending the game.")
        return end_game(user_key)

    if convo.event_is_active():
        e_idx, event = convo.current_e_idx, convo.current_event
    else:
        e_idx, event = convo.get_next_event(player)

    # Case: Game returned 'None' for the event index.
    #       There are no more events left for this player.
    #       Currently choosing to just keep going without that player.
    if e_idx is None:
        app.logger.info("No more events available for this player. Removing player.")
        return end_for_player(user_key, player, keep_going=True, message="You made it through all the questions!")

    app.logger.info("Got event %d: %s" % (e_idx, event))
    question = convo.get_question(e_idx)
    app.logger.info("Got question: %s" % question)

    # Case: Game returned 'None' for the question.
    #       We can increment the player and keep going.
    if question and str(question).strip() != "":
        app.logger.debug("Asking a question.")
        app.logger.info("Player %s, event %s, question %s" % (player.name, event, question))
        return render_template("play.html", player_name=player.name, event=event, question=question, next_button_text="Next", next_button_target="/play")
    else:
        app.logger.debug("Failed to ask the question")
        incr = convo.increment_player()
        app.logger.debug("Incremented player")
        return play_game()

    return render_template("play.html", player_name=player.name, event=event, question=question, next_button_text="Next", next_button_target="/play")

def end_for_player(user_key, player, keep_going=True, message=""):
    """
    Handles game behavior for the case when a player is removed from the game.

    If `keep_going` is `True`, then the player is removed and given a thank you 
    message, and the game continues.

    If `keep_going` is `False`, then the game ends.
    """
    if keep_going:
        convo = game_cache.get(user_key)
        app.logger.debug("Successfully retrieved conversation")
        convo.remove_player(player.name, player.birth_year)
        app.logger.debug("Removed player from conversation")
        return render_template("play.html", player_name="", question='Thanks for playing, %s! %s' % (player.name, message), event="", next_button_text="Keep going with other players", next_button_target="/play")
    else:
        return end_game(user_key)

@app.route("/feedback")
def feedback():
    return render_template("feedback.html", event='We appreciate any and all feedback for the game.', next_button_text="Set up a new game", next_button_target="/setup")

def end_game(user_key):
    global game_cache
    game_cache.pop(user_key)
    return render_template("feedback.html", event='Game over! Thanks for playing :)', next_button_text="Play again?", next_button_target="/setup")


if __name__ == "__main__":
    handler = RotatingFileHandler('logs/webapp.log', maxBytes=100000, backupCount=1)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter( "%(asctime)s | %(pathname)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s ")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)
    app.secret_key = os.urandom(32)
    app.run(debug=True)