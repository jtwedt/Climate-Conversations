# encoding=utf8  
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
from flask import Flask, session, request, render_template, url_for, redirect
import os
import logging
from logging.handlers import RotatingFileHandler
sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.getcwd() + "/resources")
sys.path.insert(0, os.getcwd() + "/ui") 
from ClimateConversationsCore import *

app = Flask(__name__)

game_cache = {}

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/setup")#, methods=['POST'])
def game_setup():
    # if request.method == "POST":
        # session['testsession'] = request.form['testsession']
    return render_template("setup.html")

@app.route("/setup/save", methods=['POST'])
def save_game_setup():
    global game_cache
    form_data = request.form
    n_rounds = int(form_data.get("num_rounds"))
    players = []

    # TODO remove this hardcoding!!
    p1_name = form_data.get("name-p1")
    p1_byear = int(form_data.get("birthyear-p1"))
    p1 = Player(p1_name, p1_byear)
    players.append(p1)

    while True:
        p2_name = form_data.get("name-p2")
        p2_byear = int(form_data.get("birthyear-p2"))
        if p2_name:
            p2 = Player(p2_name, p2_byear)
            players.append(p2)
        else:
            break
        break
    # for key,val in request.form.iteritems():
    #     print key, ":", val
    #     if val == "":
    #         print "no value"
    # print request.form
    # print request.values
    # print request.method
    # session['']
    try:
        user_key = session['user_key']
    except:
        user_key = os.urandom(24)
        session['user_key'] = user_key  # players

    convo = Conversation(n_rounds = n_rounds, players=players)
    game_cache[user_key] = convo #{"conversation":None, "players":None}
    # game_cache[user_key]["players"] = players

    # game_cache.setdefault(user_key, default={"conversation":None, "players":None})
    # print "setting players"
    # game_cache[user_key]["players"] = players
    print "game cache here:"
    print game_cache

    return redirect("/play", code=302)
    # return render_template("play.html")


@app.route("/play")
def play_game():
    global game_cache
    app.logger.info("Loading convo from cache")
    user_key = session['user_key']
    convo = game_cache.get(user_key)
    app.logger.info("Got conversation")
    player = convo.get_current_player()
    app.logger.info("Got player")
    if player is None:
        app.logger.info("No player returned (probably no more rounds). Serving up 'OUT OF QUESTIONS.'")
        # redirect to landing page
        return render_template("play.html", player_name="", event='OUT OF QUESTIONS', question="")
    incr = convo.increment_player()
    app.logger.info("Incremented player")
    e_idx, event = convo.get_next_event(player) ### figure out why this crashes at the end
    app.logger.debug("Got event %d: %s" % (e_idx, event))
    question = convo.get_question(e_idx)
    app.logger.debug("Got question: %s" % question)
    # print event
    # print question
    
    return render_template("play.html", player_name=player.name, event=event, question=question)
    

if __name__ == "__main__":
    handler = RotatingFileHandler('logs/webapp.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    # formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    formatter = logging.Formatter( "%(asctime)s | %(pathname)s:%(lineno)d | %(funcName)s | %(levelname)s | %(message)s ")
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.secret_key = os.urandom(32)
    app.run()