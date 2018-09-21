import os
from player.player import Player
from leaderboard.leaderboard import Leaderboard
from reader.reader import Reader
from flask import Flask, render_template, request, redirect, url_for, flash


def removePlayer(player_to_remove):
    removedPlayer = Player(player_to_remove)

    try:
        leaderboard = getCurrentLeaderboard()
        leaderboard.removePlayer(removedPlayer)
        updateLeaderboard(leaderboard)

    except:
        print("Error removing player from leaderboard")


def recordMatch(winner, loser):
    playersTable = reader.readPlayers()
    leaderboard = getCurrentLeaderboard()
    winner = Player(winner)
    loser = Player(loser)

    if winner.name == loser.name:
        return "Winner name and loser name are the same"

    elif not playersTable.playerInTable(winner) and playersTable.playerInTable(loser):
        playersTable.players.append(winner)
        playersTable.players.append(loser)

    elif winner not in playersTable.players:
        playersTable.players.append(winner)

    elif not playersTable.playerInTable(loser):
        playersTable.players.append(loser)

    updateLeaderboardAfterMatch(winner, loser, leaderboard)


def updateLeaderboardAfterMatch(winner, loser, leaderboard):
    leaderboard.updateAfterMatch(winner, loser)

    updateLeaderboard(leaderboard)
    return leaderboard


def changeLeaderboard(newCurrentLeaderboardName):
    leaderboardNames = reader.readLeaderboardNames()

    if newCurrentLeaderboardName not in leaderboardNames:
        return "This leaderboard does not exist"

    else:
        reorderLeaderboardNames(newCurrentLeaderboardName, leaderboardNames)


def createLeaderboard(newLeaderboardName):
    leaderboardNames = reader.readLeaderboardNames()

    if newLeaderboardName in leaderboardNames:
        return "This leaderboard already exists"
    elif newLeaderboardName == "leaderboardNames":
        return "This name is not permitted"
    else:
        newLeaderboard = Leaderboard(newLeaderboardName, [])
        updateLeaderboard(newLeaderboard)

        reorderLeaderboardNames(newLeaderboardName, leaderboardNames)
        print("Leaderboard added!")


def deleteLeaderboard(removedLeaderboardName):
    leaderboardNames = reader.readLeaderboardNames()
    leaderboardNames.remove(removedLeaderboardName)
    os.remove("../leaderboard/" + removedLeaderboardName + ".txt")
    updateLeaderboardNames(leaderboardNames)


def getAllLeaderboards():
    leaderboardNames = reader.readLeaderboardNames()
    allLeaderboards = []

    for name in leaderboardNames:
        leaderboard = reader.readLeaderboard(name)
        allLeaderboards.append(leaderboard)

    return allLeaderboards


def getCurrentLeaderboard():
    leaderboardNames = reader.readLeaderboardNames()
    if len(leaderboardNames) == 0:
        return "There are currently no existing leaderboards"

    currentLeaderboardName = leaderboardNames[0]
    currentLeaderboard = reader.readLeaderboard(currentLeaderboardName)

    return currentLeaderboard


def updatePlayersTable(playersTable):
    players = playersTable.getPlayers()
    playerNames = []
    for player in players:
        playerNames.append(player.getName())
    updateFile("../player/storedPlayers.txt", playerNames)


def updateLeaderboard(leaderboard):
    players = leaderboard.getRankings()
    playerNames = []
    for player in players:
        playerNames.append(player.getName())
    leaderboardName = leaderboard.getName()
    updateFile("../leaderboard/" + leaderboardName + ".txt", playerNames)


def updateLeaderboardNames(leaderboardNames):
    updateFile("../leaderboard/leaderboardNames.txt", leaderboardNames)


def reorderLeaderboardNames(newCurrentLeaderboardName, leaderboardNames):
    if newCurrentLeaderboardName in leaderboardNames:
        newCurrentLearderboardNamePosition = leaderboardNames.index(newCurrentLeaderboardName)
        reorderedLeaderboardNames = [newCurrentLeaderboardName] + leaderboardNames[:newCurrentLearderboardNamePosition] + leaderboardNames[newCurrentLearderboardNamePosition + 1:]
    else:
        reorderedLeaderboardNames = [newCurrentLeaderboardName] + leaderboardNames
    updateFile("../leaderboard/leaderboardNames.txt", reorderedLeaderboardNames)


def updateFile(filename, contents):
    myFile = open(filename, "w")
    for item in contents:
        myFile.write(item + "\n")
    myFile.close()


def getLeaderboardList():
    leaderboards = getAllLeaderboards()

    lb_list = []

    for l in leaderboards:
        player_list = []
        for p in l.rankings:
            player_list.append([p, l.rankings.index(p) + 1])
        lb_list.append([l.name, player_list])

    return lb_list


reader = Reader()
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/leaderboard')
def leaderboard():
    lb_list = getLeaderboardList()

    return render_template('lb.html', leaderboards=lb_list)


@app.route('/leaderboard', methods=['POST'])
def new_add_player():
    lb_choice = request.form.get('lb_choice')
    multiselect = request.form.getlist('player')
    changeLeaderboard(lb_choice)

    winner = multiselect[0].capitalize()
    loser = multiselect[1].capitalize()

    res = recordMatch(winner, loser)
    if res:
        flash(res)

    return redirect(url_for('leaderboard'))


@app.route('/modify-leaderboard')
def modify_leaderboard_form():
    return render_template('modify_leaderboard_form.html')


@app.route('/modify-leaderboard', methods=['POST'])
def modify_leaderboard():
    new_leaderboard_name = request.form.get('new_lb_name')
    delete_leaderboard_name = request.form.get('delete_lb_name')
    delete_player_name = request.form.get('delete_player_name')

    if new_leaderboard_name:
        createLeaderboard(new_leaderboard_name)

    if delete_leaderboard_name:
        deleteLeaderboard(delete_leaderboard_name)

    if delete_player_name:
        removePlayer(delete_player_name)

    return redirect(url_for('leaderboard'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404
