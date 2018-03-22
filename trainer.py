from network import Network
from connect_4 import Connect_4
from itertools import combinations
import numpy as np
import copy 
import tqdm

total_generations = 100
pop_size = 20
mutation_rate = 0.1
num_surviving = 5

def find_winner(population, scoreboard):
    def run(players):
        p1, p2 = players
        game = Connect_4([population[p1], population[p2]], headless=True, printing=False)
        winner = game.run_game()
        if winner == 0:
            scoreboard[p1] += 1
        if winner == 1:
            scoreboard[p2] += 1
    return run

def rate(population):
    scoreboard = [0] * len(population)

    # All unique pairs of ai's
    indexes = combinations(range(len(population)), 2)
    list(map(find_winner(population, scoreboard), indexes))

    return scoreboard

def find_n_best(scores, population, n):
    best = []
    for i in range(n):
        best_score_idx = np.argmax(scores)
        best.append((population.pop(best_score_idx), scores.pop(best_score_idx)))
    return best

# Create a bunch of networks
population = [Network() for i in range(pop_size)]
best = []

for generation in tqdm.tqdm(range(total_generations)):
    list(map(lambda x: x.mutate(mutation_rate=mutation_rate), population))
    scores = rate(population)
    best = find_n_best(scores, population, num_surviving)

    # Create new population
    population = []
    total_score = sum([survivor[1] for survivor in best])
    for network, score in best:
        # Weigh the numbers of copies
        num_copies = pop_size * (score / total_score)
        copies = [copy.deepcopy(network) for _ in range(num_copies)]
        population.extend(copies)

for idx, (best_net, score) in enumerate(best):
    best_net.save(f'{idx}_score_{score}')

print(best)
game = Connect_4([lambda x: int(input()) - 1, best[0][0]], headless=True, printing=True)
winner = game.run_game()