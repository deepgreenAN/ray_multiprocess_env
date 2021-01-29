import time
import pickle
import numpy as np

def square(x):
    time.sleep(5)
    return x**2
    
def read_pickle(pickle_path):
    with open(pickle_path, "rb") as f:
        df = pickle.load(f)

    return df
    
def identiti_func(x):
    return x
    
def identiti_func2(x):
    return x
    
class SimpleEnvScript():
    def __init__(self):
        self.init_number = None

    def reset(self):
        self.init_number = np.random.randint(0,100, size=(1,))
        return identiti_func2(identiti_func(self.init_number))

    def step(self, action):
        self.init_number += action
        return self.init_number, 0, False, None 