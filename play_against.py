from network import Network
from connect_4 import Connect_4

net_to_load = input()
while not net_to_load == "":
    net = Network.load("log/" + net_to_load)
    game = Connect_4([None, net], headless=True, printing=True)
    winner = game.run_game()
    net_to_load = input()