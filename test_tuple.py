
import numpy as np

n_prime_state = (2,2,4)
state_below = np.subtract(n_prime_state, (0,0,1))
print(tuple(state_below))