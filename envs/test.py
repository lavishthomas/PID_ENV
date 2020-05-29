import gym
import math
import numpy as np
from gym import error, spaces, utils, logger
from gym.utils import seeding


a = spaces.Discrete(2)



gravity = 9.8
masscart = 1.0
masspole = 0.1
total_mass = (masspole + masscart)
length = 0.5  # actually half the pole's length
polemass_length = (masspole * length)
force_mag = 10.0
tau = 0.02  # seconds between state updates
kinematics_integrator = 'euler'

# Angle at which to fail the episode
theta_threshold_radians = 12 * 2 * math.pi / 360
x_threshold = 2.4

# Angle limit set to 2 * theta_threshold_radians so failing observation
# is still within bounds.
high = np.array([x_threshold * 2, np.finfo(np.float32).max,
                 theta_threshold_radians * 2, np.finfo(np.float32).max], dtype=np.float32)
action_space = spaces.Discrete(2)
observation_space = spaces.Box(-high, high, dtype=np.float32)

seed = None
np_random, seed = seeding.np_random(seed)
state = np_random.uniform(low=-0.05, high=0.05, size=(4,))

print('------------------------------')
print(high.shape)

print(high)
print(-high)
print('------------------------------')
print(state)
print('------------------------------')
print('action_space')
print(action_space)
print(action_space.shape)
print('------------------------------')

print('observation_space')
print(observation_space)
print(observation_space.shape)