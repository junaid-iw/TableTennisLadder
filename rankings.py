import sys

def existingWin(rankings, winner, loser):
    loser_position = rankings.index(loser)
    winner_position = rankings.index(winner)

    if winner_position > loser_position:
        rankings = rankings[:loser_position] + [winner] + rankings[loser_position:winner_position] + rankings[winner_position + 1:]

    return rankings

def newLoser(rankings, loser):
    rankings.append(loser)
    
    return rankings

def newPlayers(rankings, winner, loser):
    rankings.append(winner)
    rankings.append(loser)
    
    return rankings

def newWinner(rankings, winner, loser):
    loser_position = rankings.index(loser)
    rankings = rankings[:loser_position] + [winner] + rankings[loser_position:]
    
    return rankings

# def main():
#     if len(sys.argv) != 3:
#         print 'usage: ./rankings.py {winner | loser} file'
#         sys.exit(1)

#     rankings = ["matt", "junaid", "mike", "james", "sandeep"]
    
#     winner = sys.argv[1]
#     loser = sys.argv[2]

#     if winner in rankings and loser in rankings:
#         rankings = existingWin(rankings, winner, loser)
#     elif winner in rankings:
#         rankings = newLoser(rankings, loser)
#     elif loser in rankings:
#         rankings = newWinner(rankings, winner, loser)
#     else:
#         rankings = newPlayers(rankings, winner, loser)
#     #rankings = existingWin(rankings, "james", "matt")
#     #rankings = newLoser(rankings, "emily")
#     #rankings = newPlayers(rankings, "emily", "ash")
#     #rankings = newWinner(rankings, "emily", "junaid")

#     for player in rankings:
#         print(player)

def addPlayers(players):
    finished = False

    while (not finished):
        print("Please enter the name of the new player: \n")
        newPlayer = raw_input()
        print("")

        if (newPlayer in players):
            print("This player already exists.")
            finished = anotherPlayerQuery(finished)
        else:
            players.append(newPlayer)
            print("Player added! ")
            finished = anotherPlayerQuery(finished)
            

    return players

def anotherPlayerQuery(finished):
    finished2 = False
    while (not finished2):
        print("Would you like to add another player? (y/n) \n")
        choice = raw_input()
        print("")
        if choice == "y":
            finished2 = True
        elif choice == "n":
            finished = True
            finished2 = True
        else:
            print("Invalid input.")
    return finished

def recordMatch(players, rankings):
    winner = ""
    loser = ""
    
    finished = False
    while(not finished):
        print("Please enter the name of the match winner: \n")
        winner = raw_input()
        print("")

        if (winner not in players):
            print("This player is not in the league.")
        else:
            finished = True
    
    finished = False
    while(not finished):
        print("Please enter the name of the match loser: \n")
        loser = raw_input()
        print("")

        if (loser not in players):
            print("This player is not in the league.")
        else:
            finished = True

    if winner in rankings and loser in rankings:
        rankings = existingWin(rankings, winner, loser)
    elif winner in rankings:
        rankings = newLoser(rankings, loser)
    elif loser in rankings:
        rankings = newWinner(rankings, winner, loser)
    else:
        rankings = newPlayers(rankings, winner, loser)

    print("Rankings updated!")
    return rankings

def seeRankings(rankings):
    print("The current rankings are as follows: \n")

    position = 1
    for player in rankings:
        print(str(position) + ". " + player)
        position += 1

def main():
    players = ["matt", "junaid", "mike", "james", "sandeep"]
    rankings = ["matt", "junaid", "mike", "james", "sandeep"]
    print("Welcome to TZ Table Tennis (Copyright 2018. All rights reserved) \n")
    
    finished = False

    while (not finished):
        print("Please choose from one of the following options:")
        print("1) Add players")
        print("2) Record match")
        print("3) See rankings \n")


        choice = raw_input()
        print("")

        if choice == "1":
            players = addPlayers(players)
        elif choice == "2":
            rankings = recordMatch(players, rankings)
        elif choice == "3":
            seeRankings(rankings)
        else:
            print("Invalid input. \n")
        



if __name__ == '__main__':
  main()