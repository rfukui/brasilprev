#!/usr/bin/env python
import sys
import random

qtd_simulation = 300
qtd_plays = 1000
qtd_properties = 20
start_balance = 300
min_value_property = 50
max_value_property = 500
percent_rent = 0.25
increase_balance_by_checkpoint = 100

args = {
    0: "300",
    1: "1000",
    2: "20",
    3: "300",
    4: "50",
    5: "500",
    6: "0.25",
    7: "100"
}

players = [
    {
        "id": 0,
        "type": "impulsive",
        "balance": start_balance,
        "position": 0
    },
    {
        "id": 1,
        "type": "picky",
        "balance": start_balance,
        "position": 0
    },
    {
        "id": 2,
        "type": "prudent",
        "balance": start_balance,
        "position": 0
    },
    {
        "id": 3,
        "type": "rand",
        "balance": start_balance,
        "position": 0
    }
    ]

properties = []
total_plays = 0
resume = {
    "timeouts": 0,
    "avg_plays": 0,
    "impulsive": 0,
    "picky": 0,
    "prudent": 0,
    "rand": 0,
    }


def create_properties():

    for i in range(qtd_properties):
        buy_value = random.randint(min_value_property, max_value_property)
        properties.append({
            "id": i,
            "buy_value": buy_value,
            "rent_value": int(buy_value * percent_rent),
            "owner": None,
            }
        )


def reset_total_plays():
    global total_plays
    total_plays = 0


def reset_players():
    random.shuffle(players)
    for i, p in enumerate(players, start=0):
        players[i]["id"] = i
        players[i]["balance"] = start_balance
        players[i]["position"] = 0


def reset_porperties():

    for prop in properties:
        properties[prop["id"]]["owner"] = None


def die():

    return random.randint(1, 6)


def increase_balance(player, value=increase_balance_by_checkpoint):
    players[player["id"]]["balance"] += value


def position(player):
    actual_position = (player["position"] + die()) % qtd_properties
    if actual_position < player["position"]:
        increase_balance(player)
    players[player["id"]]["position"] = actual_position


def set_property_owner(player, prop):
    if player["id"] is not None:
        increase_balance(player, -prop["buy_value"])
    properties[prop["id"]]["owner"] = player["id"]


def buy_by_type(player, prop):
    if player["type"] == "impulsive":
        set_property_owner(player, prop)
    elif player["type"] == "picky" and prop["rent_value"] > 50:
        set_property_owner(player, prop)
    elif player["type"] == "prudent" and (player["balance"] - prop["buy_value"]) > 80:
        set_property_owner(player, prop)
    elif player["type"] == "rand" and random.randint(0, 1):
        set_property_owner(player, prop)


def remove_properties(player):
    for p in properties:
        if player["id"] == p["owner"]:
            set_property_owner({"id": None}, p)


def pay_rent(player, prop):
    if player["balance"] >= prop["rent_value"]:
        increase_balance(player, -prop["rent_value"])
    else:
        increase_balance(players[prop["owner"]], player["balance"])
        remove_properties(player)
        players[player["id"]]["balance"] = -1


def check_to_buy(player, prop):
    if player["balance"] > prop["buy_value"]:
        buy_by_type(player, prop)


def buy_or_rent(player):
    prop = properties[player["position"]]
    if prop["owner"] is None:
        check_to_buy(player, prop)
    else:
        pay_rent(player, prop)


def play(player):
    if player["balance"] != -1:
        position(player)
        buy_or_rent(player)


def check_players():
    i = 0
    for player in players:
        if player["balance"] == -1:
            i += 1

    return i >= 3


def game():
    global total_plays
    for i in range(1, (qtd_plays + 1)):
        for player in players:
            play(player)

        if check_players():
            total_plays = i
            return
    resume["timeouts"] += 1
    total_plays = qtd_plays


def increment_player_resume(player):
    resume[player["type"]] += 1


def populate_resume(i):
    increment_player_resume(sorted(players, key=lambda p: p["balance"], reverse=True)[0])
    resume["avg_plays"] = resume["avg_plays"] + (total_plays - resume["avg_plays"]) / i


def reset():
    reset_porperties()
    reset_players()
    reset_total_plays()


def main():
    create_properties()
    all_games = []
    for i in range(1, (qtd_simulation + 1)):
        reset()
        game()
        populate_resume(i)

    print(resume)

if __name__ == '__main__':
    try:
        if sys.argv[1] in ("help", "?", "--help", "-help"):
            print("""
./main.py
executa o sistema para a simulação
para mudar cada um dos items a sequencia é
./main.py <qtd_simulacao> <qtd_turnos> <qtd_propriedades> <montante_inicial> <valor_minimo_propriedade> <valor_maximo_propriedade> <percentual_aluguel><qtd_ganha_por_volta>
a ordem deve ser preservada
        """)
            sys.exit()
    except IndexError as e:
        pass
    for k, arg in enumerate(sys.argv[1:]):
        args[k] = arg
    qtd_simulation = int(args[0])
    qtd_plays = int(args[1])
    qtd_properties = int(args[2])
    start_balance = int(args[3])
    min_value_property = int(args[4])
    max_value_property = int(args[5])
    percent_rent = float(args[6])
    increase_balance_by_checkpoint = int(args[7])
    main()
