import numpy as np
from random import uniform, random
import pickle

class Layer(object):
    def __init__(self, num_in, num_out):
        self.weights = np.zeros((num_out, num_in))
        self.bias = np.zeros(num_out)
        self.mutate(mutation_rate=1)

    def forward(self, x):
        '''
        Forward pass
        '''
        x = np.matmul(self.weights, x)
        x = self.bias + x
        x = 1 / (1 + np.exp(-x))
        return x

    def mutate(self, mutation_rate=0.1):
        '''
        Mutate the weights
        '''
        for row in range(self.weights.shape[0]):
            for col in range(self.weights.shape[1]):
                # Add a random amount to each weight
                self.weights[row, col] += mutation_rate * uniform(-1, 1)
        for i in range(self.bias.shape[0]):
            # Add a random amount to each bias
            self.bias[i] += mutation_rate * uniform(-1, 1)
        
    

class Network(object):
    def __init__(self):
        # The layers of the MLP
        self.layers = [Layer(42, 32), Layer(32, 22), Layer(22, 7)]
    
    def forward(self, x):
        '''
        Forward pass
        '''
        x = x.reshape(-1)
        for layer in self.layers:
            x = layer.forward(x)
        return x

    def __call__(self, x):
        '''
        The callback for showing board
        '''
        x = self.forward(x)
        return int(np.argmax(x))

    def mutate(self, mutation_rate=0.1):
        '''
        Mutate all layers
        '''
        for layer in self.layers:
            layer.mutate(mutation_rate=mutation_rate)
        
    def save(self, location):
        '''
        Save to file
        '''
        pickle.dump(self, open(location, 'wb'))

    @staticmethod
    def load(location):
        '''
        Load layers from files
        '''
        return pickle.load(open(location, 'rb'))
