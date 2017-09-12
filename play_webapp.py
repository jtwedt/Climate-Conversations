# encoding=utf8
import sys
from flask import Flask, session, request, render_template, redirect
import os
import logging
from logging.handlers import RotatingFileHandler
from ClimateConversationsCore import Conversation, EventStore, Player


reload(sys)
sys.setdefaultencoding('utf8')
sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.getcwd() + "/resources")
sys.path.insert(0, os.getcwd() + "/ui")

app = Flask(__name__)
app.config['DEBUG'] = True

# This is just random data no hidden meaning
app.secret_key = 'vqo0sFOyRMyEwXuTjD7REsZk6ytI'

event_store = EventStore.load_from_gdrive("1fiI18O4inR-Pm7XFnFitCrbfoGjXpZX_"
                                          "D_On348y4j8")


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/setup")
def game_setup():
    return render_template("setup.html")


@app.route("/setup", methods=['POST'])
def save_game_setup():
    global event_store

    form_data = request.form

    n_rounds = int(form_data.get("num_rounds"))
    app.logger.info("Saved n_rounds: %d" % n_rounds)

    # By using multiple form input fields with the same name we can use
    # getlist() to load a list of names and birth years. This allows processing
    # a form with an arbirary number of player.
    names_and_birthyears = zip(form_data.getlist('player_name'),
                               form_data.getlist('player_birthyear'))
    # TODO(dlundquist): handle bad player data
    players = [Player(n, y) for n, y in names_and_birthyears]

    app.logger.info("Added players: %s" % [str(p) for p in players])

    convo = Conversation.new_conversation(event_store, players, n_rounds)
    # Save conversation to session
    for k, v in convo.to_session_cookies().iteritems():
        session[k] = v

    return redirect("/play", code=302)


@app.route("/play")
def play_game():
    global events_store

    # Load conversation
    convo = Conversation.load_from_session(event_store, session)

    if convo.game_is_active():
        player, event, question = convo.get_next_question()
        description = event.format_for_player(player)
        app.logger.info("Asking a question.")
        app.logger.info("Player %s, event %s, question %s" % (
                player.name, description, question))

        # Save conversation to session -- to advance to next question
        for k, v in convo.to_session_cookies().iteritems():
            session[k] = v

        return render_template("play.html", player_name=player.name,
                               event=description, question=question,
                               next_button_text="Next",
                               next_button_target="/play")
    else:
        return end_game()


@app.route("/feedback")
def feedback():
    return render_template("feedback.html",
                           event='We appreciate any and all feedback '
                                 'for the game.',
                           next_button_text="Set up a new game",
                           next_button_target="/setup")


def end_game():
    # Clear out game state from session
    for k in Conversation.session_cookie_keys():
        session.pop(k)

    return render_template("feedback.html",
                           event='Game over! Thanks for playing :)',
                           next_button_text="Play again?",
                           next_button_target="/setup")


if __name__ == "__main__":
    handler = RotatingFileHandler('logs/webapp.log', maxBytes=100000,
                                  backupCount=1)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(pathname)s:%(lineno)d | "
                                  "%(funcName)s | %(levelname)s | "
                                  "%(message)s ")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.secret_key = os.urandom(32)
    app.run(debug=True)
