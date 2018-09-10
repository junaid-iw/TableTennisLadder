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



def main():
    if len(sys.argv) != 3:
        print 'usage: ./rankings.py {winner | loser} file'
        sys.exit(1)

    rankings = ["matt", "junaid", "mike", "james", "sandeep"]
    
    winner = sys.argv[1]
    loser = sys.argv[2]

    if winner in rankings and loser in rankings:
        rankings = existingWin(rankings, winner, loser)
    elif winner in rankings:
        rankings = newLoser(rankings, loser)
    elif loser in rankings:
        rankings = newWinner(rankings, winner, loser)
    else:
        rankings = newPlayers(rankings, winner, loser)
    #rankings = existingWin(rankings, "james", "matt")
    #rankings = newLoser(rankings, "emily")
    #rankings = newPlayers(rankings, "emily", "ash")
    #rankings = newWinner(rankings, "emily", "junaid")

    for player in rankings:
        print(player)

if __name__ == '__main__':
  main()