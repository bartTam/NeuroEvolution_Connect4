import numpy as np
from random import uniform, random
import pickle

class Layer(object):
    def __init__(self, num_in, num_out):
        self.weights = np.zeros((num_out, num_in))
        self.bias = np.zeros(num_out)
        self.mutate(mutation_rate=1)

    def forward(self, x):
        x = np.matmul(self.weights, x)
        x = self.bias + x
        x = 1 / (1 + np.exp(-x))
        return x

    def __call__(self, x):
        return self.forward(x)

    def mutate(self, mutation_rate=0.1):
        for row in range(self.weights.shape[0]):
            for col in range(self.weights.shape[1]):
                self.weights[row, col] += mutation_rate * uniform(-1, 1)
        for i in range(self.bias.shape[0]):
            self.bias[i] += mutation_rate * uniform(-1, 1)
        
    

class Network(object):
    def __init__(self):
        self.layers = [Layer(42, 20), Layer(20, 7)]
    
    def forward(self, x):
        x = x.reshape(-1)
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def __call__(self, x):
        x = self.forward(x)
        return int(np.argmax(x))

    def mutate(self, mutation_rate=0.1):
        for layer in self.layers:
            layer.mutate(mutation_rate=mutation_rate)
        
    def save(self, location):
        pickle.dump(self, open(location, 'wb'))

    @staticmethod
    def load(location):
        return pickle.load(open(location, 'rb'))
