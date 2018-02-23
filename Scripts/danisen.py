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
        self.evolution = 0
    def __iter__(self):
        return iter([self.name, self.rank, self.pts, self.victory, self.defeat, self.ratio, self.evolution])

#Return index of player name or -1 if there is no ranked player with that name
def getPlayerIndex(name, ranking):
    for i, player in enumerate(ranking):
        if name == player.name:
            return i
    return -1

def computeProfit(rw, rl):
    diff = rw-rl
    if diff < 0:
        return max(0, 1 + (diff*0.25))
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

def getRankingFromHistory(file_path):
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
            for name in player_names: #Only 2 values
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
    #sort ranking based on rank then points then victory/defeat ratio
    ranking = sorted(ranking, key=lambda player: (player.rank*10-player.pts) - (player.victory/(player.victory+player.defeat) - 0.01))
    return ranking

def writeRankingCSVFromHistory(history_file):
    ranking = getRankingFromHistory(history_file)
    rankingFile = open("ranking.csv", "w")
    rankingFile.write("Joueur,Rang,Points,Victoires,Défaites,% de Victoire,Evolution\n")
    for player in ranking:
        rankingFile.write(player.name + "," + str(player.rank) + "," + str(player.pts) + "," +\
                          str(player.victory) + "," + str(player.defeat) + "," + str(player.ratio) + "," + str(player.evolution) + "\n")

def writeRankingCSVFromRanking(ranking):
    rankingFile = open("ranking.csv", "w")
    rankingFile.write("Joueur,Rang,Points,Victoires,Défaites,% de Victoire,Evolution\n")
    for player in ranking:
        rankingFile.write(player.name + "," + str(player.rank) + "," + str(player.pts) + "," +\
                          str(player.victory) + "," + str(player.defeat) + "," + str(player.ratio) + "," + str(player.evolution) + "\n")

def getRankingFromRankingCSV(ranking_path):
    csv = open(ranking_path, "r")
    ranking = []
    for i, row in enumerate(csv):
        if i!=0:
            values = row.split(",")
            player = Player(values[0])
            player.rank = int(values[1])
            player.pts = float(values[2])
            player.victory = int(values[3])
            player.defeat = int(values[4])
            player.ratio = values[5]
            player.evolution = int(values[6])
            ranking.append(player)
    csv.close()
    return ranking

def cmpDate(date1, date2):
    d1, m1, y1 = date1.split("/")
    d2, m2, y2 = date2.split("/")
    d1 = int(d1)
    d2 = int(d2)
    m1 = int(m1)
    m2 = int(m2)
    y1 = int(y1)
    y2 = int(y2)
    if y1 < y2:
        return 1
    if y1 > y2:
        return -1
    else:
        if m1 < m2:
            return -1
        if m1 > m2:
            return 1
        else:
            if d1 < d2:
                return -1
            if d1 > d2:
                return 1
    return 0

def addMatch(values, ranking):
    matchups = values[3].split("-")
    scores = values[2].split("-")
    winner = int(scores[0] < scores[1])
    player_names = (values[0] + " as " + matchups[0], values[1] + " as " + matchups[1])
    players = []
    for name in player_names: #Only 2 values
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

#ranking, all_history, [session1, session2, session3, ...]
def updateRanking(ranking_path, session_paths):
    new_ranking = getRankingFromRankingCSV(ranking_path)
    last_ranking = list(new_ranking)
    for session in session_paths:
        csv = open(session)
        min_date = ""
        max_date = ""
        for i, row in enumerate(csv):
            if i!=0:
                values = row.split(",")
                date = values[4]
                if min_date == "" and max_date == "":
                    min_date = date
                    max_date = date
                elif cmpDate(date, min_date) < 0:
                    min_date = date
                elif cmpDate(date, max_date) > 0:
                    max_date = date
                addMatch(values, new_ranking)
        #sort ranking based on rank then points then victory/defeat ratio
        new_ranking = sorted(new_ranking, key=lambda player: (player.rank*10-player.pts) - (player.victory/(player.victory+player.defeat) - 0.01))
        for players in last_ranking:
            new_ndx = new_ranking.index(players)
            old_ndx = last_ranking.index(players)
            new_ranking[new_ndx].evolution = old_ndx - new_ndx
        last_ranking = list(new_ranking)
    return new_ranking

if __name__ == "__main__":
    csvs = []
    for i, arg in enumerate(sys.argv):
        if i != 0:
            csvs.append(arg)
    ranking = updateRanking("ranking.csv", csvs)
    print(tabulate(ranking, headers=["Joueur", "Rang", "Points", "Victoires", "Défaites", "% de Victoire", "Evolution depuis la dernière session"]))
