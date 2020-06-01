import gym
import math
import numpy as np
from gym import error, spaces, utils, logger
from gym.utils import seeding


class PidEnv(gym.Env):
    """
    Description:
        A PID environment

    Source:
        This is based on PID requirements 

    Observation:
        Type: Box(2)
        Num	Observation             Min          Max
        0	pv_low                  0            Inf
        1	pv_high                 0            Inf
        
    Actions:
        Type: Discrete(2)
        Num	Action
        0	no change
        1	decrease
        2   increase
        3   decrese-high
        4   increase-high


        Note: The amount the velocity that is reduced or increased is not
        fixed; it depends on the angle the pole is pointing. This is because
        the center of gravity of the pole increases the amount of energy needed
        to move the cart underneath it

    Reward:
        If the error is less than previous step, +ve reward
        If the error is higher than previous step -ve reward

    Starting State:
        Starting state sv 1000, pv = 0

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

        self.f = open("data.csv", "w")
        # PID Properties
        self.sp = 1000
        self.pv = 0
        self.mv = 1
        self.previous_error = 0
        self.current_error = 0
        # self.eq = [1, 2, 3, 4]  # x3 + 2x2 + 3x + 4
        self.eq = [3, 4]  # 1x + 2

        mu = 1  # Means
        sigma = .2
        points = 10
        s = np.random.normal(mu, sigma, points)
        self.action_sample = sorted(s)
        self.action_space = spaces.Discrete(points)

        # maximum values allowed
        #pv_high = np.array([np.finfo(np.float32).max, np.finfo( np.float32).max], dtype=np.float32)
        pv_low = np.array([0, 0], dtype=np.float32)
        pv_high = np.array([self.sp*2, self.sp*2], dtype=np.float32)
        self.observation_space = spaces.Box(pv_low, pv_high, dtype=np.float32)

        self.seed()
        self.viewer = None
        self.state = None

        self.steps_beyond_done = None

    def eq_evaluator(self, x_value):
        total = 0
        for index, coefficient in enumerate(reversed(self.eq)):
            print(index, '  ', coefficient)
            total = total + (coefficient * (x_value ** (index)))

        return round(total,2)

    def step(self, action):

        # Chaning the mv based on action
        self.mv = round(self.mv * self.action_sample[action], 2)

        # New pv value based on the equation
        self.pv = self.eq_evaluator(self.mv)

        # 
        self.current_error = round(abs(self.sp - self.pv),2)

        if self.current_error > self.previous_error:
            reward = -1
        else:
            reward = 1

        self.previous_error = self.current_error

        done = True
        self.state = [self.pv, self.sp]

        print('action')
        print(action)
        print('mv :', self.mv, 'sp :', self.sp, 'pv :', self.pv)
        print('ce :', self.current_error, 'pe', self.previous_error)
        data = str(self.mv) + ',' + str(self.sp) + ',' + str(self.pv) + ',' + \
            str(self.current_error) + ',' + str(self.previous_error) + '\n'
        print(data)
        self.f.write(data)
        return np.array(self.state), reward, done, {}
        pass

    def reset(self):
        # self.state = self.np_random.uniform(low=-0.05, high=0.05, size=(2,))
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
