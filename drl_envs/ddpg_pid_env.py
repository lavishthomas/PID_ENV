import gym
import math
import numpy as np
import requests
from gym import error, spaces, utils, logger
from gym.utils import seeding


# Custom Library
from process.process import Process

# Base url to the Process server
baseUrl = 'http://localhost:5000/'


class DDPGPidEnv(gym.Env):
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

        ######################################
        # Intializing Process
        ######################################
        self.process = Process()

        ######################################

        self.action_space = spaces.Discrete(5)  # 5 possible actions 0 to 4
        high = np.array([self.process.pv, self.process.sp],  dtype=np.float32)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)

        ######################################
        self.seed()
        self.viewer = None
        self.state = None

        self.steps_beyond_done = None
        ######################################
        self.previous_error = 0
        self.current_error = 0

    ######################################
    # To get data via API's
    ######################################
    def eq_evaluator(self, x_value):
        cv = x_value
        degree = 2
        pvUrlString = baseUrl + 'pv?degree=' + str(degree) + '&cv=' + str(cv)
        response = requests.get(pvUrlString)
        data = response.json()
        return data

    ######################################
    # To get data via API's
    ######################################
    def step(self, action):
        # Changing the cv based on action
        if self.process.cv == 0:
            self.process.cv = 1.1
        # The rate of change is depend on the compelxity of the equation
        increment = (self.previous_error/self.process.sp) * self.process.cv * \
            (self.process.cv_change_percent ** self.process.cv_change_factor)
        increment = round(increment, 5)
        print('increment : ', increment, 'change : ',
              self.process.cv_change_percent, ' : ',  self.process.cv_change_factor)

        # Changing the cv based on action chose by the agent
        if action == 0:
            pass
        elif action == 1:
            self.process.cv += increment
            print('increment action')
        elif action == 2:
            self.process.cv -= increment
            print('decrement action')
        elif action == 3:
            self.process.cv += increment*2
            print('increment high action')
        elif action == 4:

            self.process.cv -= increment*2
        else:
            print('unidentified action')

        # New PV is calculated by the process
        new_values = self.process.eq_evaluator(self.process.cv)

        # New sp value based on the equation
        self.process.sp = new_values['sp']

        # New pv value based on the equation
        self.process.pv = new_values['pv']

        # Calculating error
        self.current_error = abs(self.process.sp - self.process.pv)

        # Reward calculator
        if self.current_error < self.previous_error:
            reward = 1
        else:
            reward = -1

        self.previous_error = self.current_error

        ### Episode ends when 
        ### the pv is almost equal to sp.
        ### pv goes -ve 
        ### pv goes double the sp
        if (self.current_error < 0.01 * self.process.sp) or (self.process.pv < 0) or (self.process.pv > (2.0 * self.process.sp)):
            done = True
        else:
            done = False
        done = True
        self.state = [self.process.pv, self.process.sp]

        ######################################
        # Recording Data
        ######################################
        print('action : ', action)  # self.action_sample[action])
        print('cv : ', self.process.cv, 'sp : ',
              self.process.sp, 'pv :', self.process.pv)
        print('ce : ', self.current_error, 'pe : ', self.previous_error)

        ######################################

        return np.array(self.state), reward, done, {}
        pass

    ######################################
    # To get data via API's
    ######################################
    def reset(self):
        # self.state = self.np_random.uniform(low=-0.05, high=0.05, size=(2,))
        self.state = [0, 100]
        self.steps_beyond_done = None
        return np.array(self.state)

    ######################################
    # To get data via API's
    ######################################
    def render(self, mode='human'):
        pass

    ######################################
    # To get data via API's
    ######################################
    def close(self):
        pass

    ######################################
    # To get data via API's
    ######################################
    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]
