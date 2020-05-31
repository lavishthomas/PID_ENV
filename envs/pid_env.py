import gym
import math
import numpy as np
import requests
from random import uniform
from gym import error, spaces, utils, logger
from gym.utils import seeding
from datetime import datetime

# Base url to the Process server
baseUrl = 'http://localhost:5000/'


class PidEnv(gym.Env):
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

        # Recording Data
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        print("date and time =", dt_string)
        dt_string = 'data/' + dt_string + '.csv'
        self.f = open(dt_string, "w")
        self.f.write('cv,sp,pv,ce,pe\n')

        # PID Properties
        # self.eq = [1, 2, 3, 4]  # x3 + 2x2 + 3x + 4
        # self.eq = [3, 5]  # 1x + 2
        self.eq = [7, 6, 5, 4, 3, 2, 5]  # 1x + 2
        self.sp = 10000
        self.pv = 0
        self.cv = 1
        self.cv_change_percent = .5
        self.cv_change_factor = len(self.eq)
        self.previous_error = 0
        self.current_error = 0

        self.counter = 0

        self.action_space = spaces.Discrete(5)  # 3 possible actions 0,1,2
        high = np.array([self.pv, self.sp],  dtype=np.float32)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)

        self.seed()
        self.viewer = None
        self.state = None

        self.steps_beyond_done = None

    def eq_evaluator_local(self, x_value):

        # SP changer
        self.counter += 1
        if self.counter > 200:
            self.counter = 0
            self.sp = self.sp * uniform(0.8, 1.2)

        total = 0
        for index, coefficient in enumerate(reversed(self.eq)):
            #print(index, '  ', coefficient)
            total = total + (coefficient * (x_value ** (index)))
        data = {'sp': round(self.sp, 5),
                'pv': round(total, 5),
                'cv': round(self.cv, 5)}
        return data

    def eq_evaluator(self, x_value):
        cv = x_value
        degree = 2
        pvUrlString = baseUrl + 'pv?degree=' + str(degree) + '&cv=' + str(cv)
        response = requests.get(pvUrlString)
        data = response.json()
        return data

    def step(self, action):
        # Changing the cv based on action
        if self.cv == 0:
            self.cv = 1.1
        # The rate of change is depend on the compelxity of the equation
        increment = (self.previous_error/self.sp) * self.cv * \
            (self.cv_change_percent ** self.cv_change_factor)
        print('increment : ', increment, 'change : ',
              self.cv_change_percent, ' : ',  self.cv_change_factor)
        increment = round(increment, 5)
        if action == 0:
            pass
        elif action == 1:
            self.cv += increment
        elif action == 2:
            self.cv -= increment
        elif action == 3:
            self.cv += increment*2
        elif action == 4:
            self.cv -= increment*2
        else:
            print('unidentified action')

        new_values = self.eq_evaluator_local(self.cv)
        # new sp value based on the equation
        self.sp = new_values['sp']

        # New pv value based on the equation
        self.pv = new_values['pv']

        self.current_error = abs(self.sp - self.pv)

        if self.current_error < self.previous_error:
            reward = 1
        else:
            reward = -1

        self.previous_error = self.current_error

        done = True
        self.state = [self.pv, self.sp]

        print('action : ', action)  # self.action_sample[action])
        print('cv :', self.cv, 'sp :', self.sp, 'pv :', self.pv)
        print('ce :', self.current_error, 'pe', self.previous_error)

        data = str(self.cv) + ',' + str(self.sp) + ',' + str(self.pv) + ',' + \
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
