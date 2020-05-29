import gym
import math
import numpy as np
from gym import error, spaces, utils, logger
from gym.utils import seeding


class FooEnv(gym.Env):
    """
    Description:
        A pole is attached by an un-actuated joint to a cart, which moves along
        a frictionless track. The pendulum starts upright, and the goal is to
        prevent it from falling over by increasing and reducing the cart's
        velocity.

    Source:
        This environment corresponds to the version of the cart-pole problem
        described by Barto, Sutton, and Anderson

    Observation:
        Type: Box(4)
        Num	Observation               Min             Max
        0	Cart Position             -4.8            4.8
        1	Cart Velocity             -Inf            Inf
        2	Pole Angle                -24 deg         24 deg
        3	Pole Velocity At Tip      -Inf            Inf

    Actions:
        Type: Discrete(2)
        Num	Action
        0	increase mv
        1	decrease mv

        Note: The amount the velocity that is reduced or increased is not
        fixed; it depends on the angle the pole is pointing. This is because
        the center of gravity of the pole increases the amount of energy needed
        to move the cart underneath it

    Reward:
        If the error is less than previous step, +ve reward
        If the error is higher than previous step -ve reward

    Starting State:
        Starting state sv 100, pv = 0

    Episode Termination:
        Pole Angle is more than 12 degrees.
        Cart Position is more than 2.4 (center of the cart reaches the edge of
        the display).
        Episode length is greater than 200.
        Solved Requirements:
        Considered solved when the average reward is greater than or equal to
        195.0 over 100 consecutive trials.
    """

    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 50}

    def __init__(self):
        # PID Properties
        self.sp = 0
        self.pv = 0
        self.mv = 0
        #self.eq = [1, 2, 3, 4]  # x3 + 2x2 + 3x + 4
        self.eq = [1, 2 ]  # 1x + 2
        
        high = np.array([self.pv, self.sp],  dtype=np.float32)

        self.action_space = spaces.Discrete(2)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)

        self.seed()
        self.viewer = None
        self.state = None

        self.steps_beyond_done = None

###############
    def eq_evaluator(self, x_value):
    total = 0
    for index, coefficient in enumerate(reversed(self.eq)):
        print(index, '  ', coefficient)
        total = total + (coefficient * (x_value ** (index)))

    return total


    def step(self, action):
        done = True
        reward = 0.0
        self.state = [0, 100] 
        #self.np_random.uniform(low=-0.05, high=0.05, size=(2,))
        print(self.state)
        return np.array(self.state), reward, done, {}
        pass

    def reset(self):
        #self.state = self.np_random.uniform(low=-0.05, high=0.05, size=(2,))
        self.state = [0, 100]
        self.steps_beyond_done = None
        return np.array(self.state)

    def render(self, mode='human'):
        pass

    def close(self):
        pass

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
