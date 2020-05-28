import gym
import math
import numpy as np
from gym import error, spaces, utils, logger
from gym.utils import seeding


class FooEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):        
        ### PID Properties



        # Angle at which to fail the episode
        self.theta_threshold_radians = 12 * 2 * math.pi / 360
        self.x_threshold = 2.4

        # Angle limit set to 2 * theta_threshold_radians so failing observation
        # is still within bounds.
        high = np.array([self.x_threshold * 2,
                         np.finfo(np.float32).max,
                         self.theta_threshold_radians * 2,
                         np.finfo(np.float32).max],
                        dtype=np.float32)

        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)

        self.seed()
        self.viewer = None
        self.state = None

        self.steps_beyond_done = None

###############

    def step(self, action):

        done = True
        reward = 0.0
        self.state = self.np_random.uniform(low=-0.05, high=0.05, size=(4,))
        return np.array(self.state), reward, done, {}
        pass

    def reset(self):
        self.state = self.np_random.uniform(low=-0.05, high=0.05, size=(4,))
        self.steps_beyond_done = None
        return np.array(self.state)

    def render(self, mode='human'):
        pass

    def close(self):
        pass

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
