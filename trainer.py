from network import Network
from connect_4 import Connect_4

import os
from itertools import combinations
import numpy as np
import copy 
import tqdm

total_generations = 10
pop_size = 50
mutation_rate = 2
num_surviving = 10

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
    '''
    Find the scores of all the models
    '''
    scoreboard = [0] * len(population)

    # All unique pairs of ai's
    indexes = combinations(range(len(population)), 2)
    list(map(find_winner(population, scoreboard), indexes))

    return scoreboard

def find_n_best(scores, population, n):
    '''
    Get the best n models of the population
    '''
    best = []
    for i in range(n):
        best_score_idx = np.argmax(scores)
        best.append((population.pop(best_score_idx), scores.pop(best_score_idx)))
    return best

# Create a bunch of networks
population = [Network() for i in range(pop_size)]
best = []

# Iterate over all generations
for generation in tqdm.tqdm(range(total_generations)):
    
    # Reduce mutation rate after 500 iterations
    if generation == total_generations / 2:
        mutation_rate = mutation_rate / 2
    
    # Mutate all models
    list(map(lambda x: x.mutate(mutation_rate=mutation_rate), population))

    # Score best models
    scores = rate(population)
    best = find_n_best(scores, population, num_surviving)

    # Create new population
    population = []
    total_score = sum([survivor[1] for survivor in best])
    for network, score in best:
        # Weigh the numbers of copies
        num_copies = pop_size // num_surviving
        copies = [copy.deepcopy(network) for _ in range(num_copies)]
        population.extend(copies)

# Save the best models
if not os.path.exists("log"):
    os.mkdir("log")
for idx, (best_net, score) in enumerate(best):
    best_net.save(f'log/{idx}_score_{score}')

# Play a game against it
game = Connect_4([None, best[0][0]], headless=True, printing=True)
winner = game.run_game()
