# Trade game: 100 players have 100 EUR and they bet 1 EUR on the flip of a coin
#
# python3 bet_game.py


import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd


EPOCH = 1000000
NUM_PLAYERS = 100
STARTING_BUDGET = 100.0
BET_BUDGET = 1.0
LOG_FILENAME = "bet_game_log.txt"
TAX_RATE = 0.5


class Player:
    def __init__(self, id, money):
        self.id = id
        self.money = money

    def update_money(self, new_money):
        self.money = new_money


def read_players_status(status_name):
    players = []

    with open(status_name + '.csv', 'r') as input_file:
        header = input_file.readline()
        for line in input_file.readlines():
            id, money = line.split(',')
            players.append(Player(id, money))

    return players


def print_players_status(players):
    for p in players:
        print("{},{}".format(p.id, p.money))


def save_players_status(players, status_name, show_figure = False):
    with open(status_name + '.csv', 'w') as output_file:
        output_file.write("player,money\n")
        for p in players:
            output_file.write("{},{}\n".format(p.id, p.money))

    ids = []
    moneys = []

    for p in players:
        ids.append(p.id)
        moneys.append(p.money)

    plt.bar(ids, moneys)
    plt.title(status_name.capitalize())
    plt.xlabel('Players')
    plt.ylabel('Moneys')
    plt.savefig(status_name + '.png', facecolor = 'white')

    if show_figure is True:
        plt.show()
    else:
        pass

    plt.clf()
    

def do_betting(players, log_filename, log_filename_mode, start_epoch, end_epoch):
    with open(log_filename, log_filename_mode) as output_file:
        if log_filename_mode == 'w':
            output_file.write("epoch,player_1,player_2,result\n")
        else:
            pass
        
        for i in range(start_epoch, end_epoch):
            player_1 = random.randint(0, NUM_PLAYERS - 1)
            player_2 = random.randint(0, NUM_PLAYERS - 1)

            if player_1 == player_2:
                output_file.write("{},{},{},Same player. No bet\n".format(i, player_1, player_2))
            else:
                if players[player_1].money > 0:
                    if players[player_2].money > 0:
                        flip = random.randint(0, 1)

                        bet_budget = min(BET_BUDGET, players[player_1].money, players[player_2].money)

                        if flip == 0:
                            players[player_1].update_money(players[player_1].money + bet_budget)
                            players[player_2].update_money(players[player_2].money - bet_budget)

                            output_file.write("{0},{1},{2},Player {1} wins bet. Now player {1} has {3} and player {2} has {4}\n".format(i, player_1, player_2, players[player_1].money, players[player_2].money))
                        else:
                            players[player_1].update_money(players[player_1].money - bet_budget)
                            players[player_2].update_money(players[player_2].money + bet_budget)

                            output_file.write("{0},{1},{2},Player {2} wins bet. Now player {1} has {3} and player {2} has {4}\n".format(i,player_1, player_2, players[player_1].money, players[player_2].money))
                    else:
                        output_file.write("{0},{1},{2},Player {2} has {3} money. No bet\n".format(i, player_1, player_2, players[player_2].money))
                else:
                    output_file.write("{0},{1},{2},Player {1} has {3} money. No bet\n".format(i, player_1, player_2, players[player_1].money))


if __name__ == '__main__':
    print('Bet game with {} players starting with {} money'.format(NUM_PLAYERS, STARTING_BUDGET))

    players = []

    for i in range(NUM_PLAYERS):
        players.append(Player(i, STARTING_BUDGET))  

    save_players_status(players, 'starting')

    do_betting(players, LOG_FILENAME, "w", 0, EPOCH)

    save_players_status(players, 'middle')

    ids = []
    moneys = []

    for p in players:
        ids.append(p.id)
        moneys.append(p.money)

    print('Max: {}'.format(np.max(moneys)))
    print('Min: {}'.format(np.min(moneys)))
    print('Average: {}'.format(np.average(moneys)))
    print('Median: {}'.format(np.median(moneys)))
    print('Q1 quantile: {}'.format(np.quantile(moneys, 0.25)))
    print('Q2 quantile: {}'.format(np.quantile(moneys, 0.50)))
    print('Q3 quantile: {}'.format(np.quantile(moneys, 0.75)))

    taxes_threshold = np.median(moneys)
    collected_taxes = 0

    for p in players:
        if p.money > taxes_threshold:
            taxes = p.money * TAX_RATE
            p.update_money(p.money - taxes)
            collected_taxes = collected_taxes + taxes
        else:
            pass

    print('Collected taxes: {}'.format(collected_taxes))

    count_broke_players = 0

    for p in players:
        if p.money == 0:
            count_broke_players = count_broke_players + 1
        else:
            pass

    print('Broke players: {}'.format(count_broke_players))

    welfare_check = collected_taxes / count_broke_players

    print('Welfare check: {}'.format(welfare_check))

    for p in players:
        if p.money == 0:
            p.update_money(welfare_check)
        else:
            pass

    with open(LOG_FILENAME, "a") as output_file:
        output_file.write("{},,,Taxes application\n".format(EPOCH))

    save_players_status(players, 'after_taxes')

    do_betting(players, LOG_FILENAME, "a", EPOCH + 1, EPOCH * 2)

    save_players_status(players, 'ending')

    ids = []
    moneys = []

    for p in players:
        ids.append(p.id)
        moneys.append(p.money)

    print('Max: {}'.format(np.max(moneys)))
    print('Min: {}'.format(np.min(moneys)))
    print('Average: {}'.format(np.average(moneys)))
    print('Median: {}'.format(np.median(moneys)))
    print('Q1 quantile: {}'.format(np.quantile(moneys, 0.25)))
    print('Q2 quantile: {}'.format(np.quantile(moneys, 0.50)))
    print('Q3 quantile: {}'.format(np.quantile(moneys, 0.75)))

    count_broke_players = 0

    for p in players:
        if p.money == 0:
            count_broke_players = count_broke_players + 1
        else:
            pass

    print('Broke players: {}'.format(count_broke_players))

else:
    pass