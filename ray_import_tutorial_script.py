import numpy as np

from multi_process_funcs import identiti_func, identiti_func2, SimpleEnvScript
import ray

def identiti_func3(x):
    return x
    
def identiti_func4_without_import(x):
    return identiti_func(x)
    
class SimpleEnvScript2():
    def __init__(self):
        self.init_number = None

    def reset(self):
        self.init_number = np.random.randint(0,100, size=(1,))
        return identiti_func4_without_import(identiti_func3(identiti_func2(identiti_func(self.init_number))))

    def step(self, action):
        self.init_number += action
        return self.init_number, 0, False, None 
        
        
@ray.remote
class RaySimpleEnvScript(SimpleEnvScript2):
    pass
