def existingWin(rankings, winner, loser):
    loser_position = rankings.index(loser)
    winner_position = rankings.index(winner)
    
    if winner_position > loser_position:
        new_rankings = []

        #produces new rankings
        for index, player in enumerate(rankings):
            if index == loser_position:
                new_rankings.append(winner)
                new_rankings.append(loser)
            elif index != winner_position:
                new_rankings.append(rankings[index])
        rankings = new_rankings
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
    
    new_rankings = []

    #produces new rankings
    for index, player in enumerate(rankings):
        if index == loser_position:
            new_rankings.append(winner)
            new_rankings.append(loser)
        else:
            new_rankings.append(rankings[index])
    rankings = new_rankings

    return rankings


def main():
    rankings = ["matt", "junaid", "mike", "james", "sandeep"]

    #rankings = existingWin(rankings, "sandeep", "james")
    #rankings = newLoser(rankings, "emily")
    #rankings = newPlayers(rankings, "emily", "ash")
    rankings = newWinner(rankings, "emily", "junaid")

    for player in rankings:
        print(player)

if __name__ == '__main__':
  main()