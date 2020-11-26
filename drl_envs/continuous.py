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


class ContinuousProcess(gym.Env):
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

        self.seed()
        self.viewer = None
        self.state = None
        self.steps_beyond_done = None
        ######################################
        self.previous_error = 0
        self.current_error = 0
        self.gl= 1
        ######################################
        
        high = np.array([self.process.pv, self.process.sp, self.gl],  dtype=np.float32)

        self.action_space = spaces.Box(
            low=1,
            high=100,
            shape=(1,),
            dtype=np.int
        )
        self.observation_space = spaces.Box(
            low=-high,
            high=high,
            dtype=np.float32
        )        
        self.seed()

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
        if self.process.cv == 0 or self.process.cv < 1.1:
            self.process.cv = 1.1
        # The rate of change is depend on the complexity of the equation 
        if isinstance(action,np.ndarray):
            action = action[0]
            
        increment = action # np.clip(action, 1, 99)
        increment = round(increment, 5)

        # Changing the cv based on action chose by the agent
        self.process.cv = (increment)/100 * self.process.cv 

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
            self.current_reward = 1
        else:
            self.current_reward = -1

        self.previous_error = self.current_error
      
        self.state = [self.process.pv, self.process.sp, self.gl]

        ######################################
        # Printing Data
        ######################################
        print('\naction : ', increment)  # self.action_sample[action])
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
