import sys
from tabulate import tabulate

class Player:
    def __init__(self, name):
        self.name = name
        self.rank = 5
        self.pts = 0
        self.victory = 0
        self.defeat = 0
        self.ratio = "0%"
    def __iter__(self):
        return iter([self.name, self.rank, self.pts, self.victory, self.defeat, self.ratio])

#Return index of player name or -1 if there is no ranked player with that name
def getPlayerIndex(name, ranking):
    for i, player in enumerate(ranking):
        if name == player.name:
            return i
    return -1

def computeProfit(rw, rl):
    diff = rw-rl
    if diff < 0:
        return max(0, 1 - diff*0.25)
    else:
        return 1

def updateWinner(player, profit):
    player.pts += profit
    player.victory += 1
    player.ratio = str(round(player.victory/(player.victory+player.defeat) * 100, 1)) + "%"
    if player.pts >= 3:
        player.rank -= 1
        player.pts = 0

def updateLoser(player, profit):
    player.defeat += 1
    player.ratio = str(round(player.victory/(player.victory+player.defeat) * 100, 1)) + "%"
    if (player.rank == 10 and player.pts == 0) == False:
        player.pts -= profit
    if player.pts <= -3:
        player.pts = 0
        player.rank += 1

def computeAllRanking(file_path):
    csv = open(file_path)
    ranking = []
    for i, row in enumerate(csv):
        if i!=0:
            values = row.split(",")
            matchups = values[3].split("-")
            scores = values[2].split("-")
            winner = int(scores[0] < scores[1])
            player_names = (values[0] + " as " + matchups[0], values[1] + " as " + matchups[1])
            players = []
            for name in player_names:
                ndx = getPlayerIndex(name, ranking)
                if ndx == -1:
                    player = Player(name)
                    ranking.append(player)
                    players.append(player)
                else:
                    player = ranking[ndx]
                    players.append(player)
            profit = computeProfit(players[winner].rank, players[1 - winner].rank)
            updateWinner(players[winner], profit)
            updateLoser(players[1 - winner], profit)
    return ranking


if __name__ == "__main__":
    if len(sys.argv) >= 2:
        ranking = computeAllRanking(sys.argv[1])
        ranking = sorted(ranking, key=lambda player: (player.rank*10-player.pts) - (player.victory/(player.victory+player.defeat) - 0.01))
        print(tabulate(ranking, headers=["Joueur", "Rang", "Points", "Victoires", "Défaites", "% de Victoire"]))
