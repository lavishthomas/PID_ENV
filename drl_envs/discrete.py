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


class DiscreteProcess(gym.Env):
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
        Type: Discrete(5)
        Num	Action
        0	no change
        1	decrease
        2   increase
        3   decrese-high
        4   increase-high       

    Reward:
        If the error is less than previous step, +ve reward
        If the error is higher than previous step -ve reward

    Starting State:
        Starting state sv 1000, pv = 0, gl = 0 

    Episode Termination:
        need to fix
    """

    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 50}

    def __init__(self):

        ######################################
        # Initializing Process
        ######################################
        self.process = Process()
        ######################################
        self.seed()
        self.viewer = None
        self.state = None

        self.steps_beyond_done = None
        self.max_steps = 0
        ######################################
        self.previous_error = 0
        self.current_error = 0
        self.current_reward =0
        ######################################
        self.gl= 1
        self.action_space = spaces.Discrete(4)  # 5 possible actions 0 to 4
        high = np.array([self.process.pv, self.process.sp, self.gl],  dtype=np.float32)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32)
        

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
        if self.process.cv == 0 or self.process.cv < 1:
            self.process.cv = 1.1
        # The rate of change is depend on the complexity of the equation
        increment = self.process.cv * \
                    (self.previous_error/self.process.sp) * \
                    (self.process.cv_change_percent ** \
                    self.process.cv_change_factor)

        increment = round(increment, 5)
        # min_increment = self.process.cv * .01
        # max_increment = self.process.cv * .05
        # increment = max(increment, min_increment)
        # increment = min(increment, max_increment)
        print('increment : ', increment, 'change : ',
              self.process.cv_change_percent, ' | degree: ',
              self.process.cv_change_factor)

        if isinstance(action, np.ndarray):
            action = action[0]

        # Changing the cv based on action chose by the agent
        
        if action == 0:
            self.process.cv += increment
            print('increment action')
        elif action == 1:
            self.process.cv -= increment
            print('decrement action')
        elif action == 2:
            self.process.cv += increment*2
            print('increment high action')
        elif action == 3:
            self.process.cv -= increment*2
        else:
            print('unidentified action')

        self.process.cv = round(self.process.cv, 5)

        # New PV is calculated by the process
        new_values = self.process.eq_evaluator(self.process.cv)

        # New sp value based on the equation
        self.process.sp = new_values['sp']

        # New pv value based on the equation
        self.process.pv = new_values['pv']

        # Calculating error
        self.current_error = self.process.sp - self.process.pv

        if self.current_error > 0:
            self.gl = 1
        else:
            self.gl = -1 

        # Reward calculator
        if abs(self.current_error) < self.previous_error:
            self.current_reward += 1
        else:
            self.current_reward -= 1

        self.previous_error = self.current_error

        self.state = [self.process.pv, self.process.sp, self.gl]

        ######################################
        # Printing Data
        ######################################
        print('\naction : ', action)  # self.action_sample[action])
        print('cv : ', self.process.cv, 'sp : ',
              self.process.sp, 'pv :', self.process.pv)
        print('ce : ', self.current_error, 'pe : ', self.previous_error)

        ######################################

        return np.array(self.state), self.current_reward, True, {}
        pass

    ######################################
    # To get data via API's
    ######################################
    def reset(self):
        self.cv = self.process.cv
        self.process.change_sp()
        self.current_reward = 0
        self.state = [self.process.pv, self.process.sp, self.gl]
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
