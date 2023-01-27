# Trade game: 100 players have 100 EUR and they bet 1 EUR on the flip of a coin
#
# python3 old_bet_game.py


import numpy as np
import random
import matplotlib.pyplot as plt


EPOCH = 1000000
NUM_PLAYERS = 100
STARTING_BUDGET = 100
BET_BUDGET = 1

players = np.arange(0, NUM_PLAYERS)
players_money = np.ones(NUM_PLAYERS, dtype = np.int32) * STARTING_BUDGET

print(len(players))
print(len(players_money))
print(players_money)
plt.bar(players, players_money)
plt.show()

with open("trade_game_log.txt","w") as output_file:
    output_file.write("epoch,player_1,player_2,result\n")
    for i in range(EPOCH):
        player_1 = random.randint(0, NUM_PLAYERS - 1)
        player_2 = random.randint(0, NUM_PLAYERS - 1)

        if player_1 == player_2:
            output_file.write("{},{},{},Same player. No bet\n".format(i,player_1,player_2))
        else:
            if players_money[player_1] >= 1:
                if players_money[player_2] >= 1:
                    flip = random.randint(0, 1)

                    if flip == 0:
                        players_money[player_1] = players_money[player_1] + BET_BUDGET
                        players_money[player_2] = players_money[player_2] - BET_BUDGET

                        output_file.write("{0},{1},{2},Player {1} wins bet. Now player {1} has {3} and player {2} has {4}\n".format(i,player_1,player_2,players_money[player_1],players_money[player_2]))
                    else:
                        players_money[player_1] = players_money[player_1] - BET_BUDGET
                        players_money[player_2] = players_money[player_2] + BET_BUDGET

                        output_file.write("{0},{1},{2},Player {2} wins bet. Now player {1} has {3} and player {2} has {4}\n".format(i,player_1,player_2,players_money[player_1],players_money[player_2]))
                else:
                    output_file.write("{0},{1},{2},Player {2} has {3} money. No bet\n".format(i,player_1,player_2,players_money[player_2]))
            else:
                output_file.write("{0},{1},{2},Player {1} has {3} money. No bet\n".format(i,player_1,player_2,players_money[player_1]))

print(len(players))
print(len(players_money))
print(players_money)
plt.bar(players, players_money)
plt.show()
