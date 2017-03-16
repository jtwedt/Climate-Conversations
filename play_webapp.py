from flask import Flask, session, request, render_template, url_for, redirect
import sys
import os
sys.path.insert(0, os.getcwd())
sys.path.insert(0, os.getcwd() + "/resources")
sys.path.insert(0, os.getcwd() + "/ui") 
from ClimateConversationsCore import *
app = Flask(__name__)

game_cache = {}
# @app.route("/")
# def run():
#     session['testsession'] = 43
#     # return '43'

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

    convo = Conversation(n_rounds = "", players=players)
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
    user_key = session['user_key']
    convo = game_cache.get(user_key)
    print convo
    print "getting question"
    player = convo.get_current_player()
    print player
    q_idx, question = convo.get_next_event(player)
    print question
    print "returning template with question"
    return render_template("play.html", text=question)
    convo.increment_player()

if __name__ == "__main__":
    app.secret_key = os.urandom(32)
    app.run()