import json
from random import uniform
from datetime import datetime


class Process():

    ######################################
    # To get data via API's
    ######################################
    def __init__(self):

        ######################################
        # Recording Data
        ######################################
        now = datetime.now()
        dt_string = now.strftime("%d_%m_%Y_%H_%M_%S")
        print("date and time =", dt_string)
        dt_string = 'data/' + dt_string + '.csv'
        self.f = open(dt_string, "w")
        self.f.write('cv,sp,pv\n')
        ######################################

        # Loading sp
        with open('../config.json', 'r') as config:
            self.polynomials = json.load(config)

        # Reading values from config

        # sp - Set Point
        self.sp = int(self.polynomials['sp'])

        # cv - Controlled Value
        self.cv = int(self.polynomials['cv'])

        # pv - Process Value
        self.pv = int(self.polynomials['pv'])

        # Degree of the polynomial
        self.degree = int(self.polynomials['degree'])

        # Automatic change of sp to observe the agent behaviour
        self.sp_change_frequency = int(self.polynomials['sp_change_frequency'])
        self.counter = 0

        print('sp: ', self.sp, 'pv: ', self.pv,
              'cv: ', self.cv, 'degree: ', self.degree)

        # The change percet
        self.cv_change_percent = .5
        # The change has to be exponential proportional to the degree to avoid the drastic change in PV while changing CV

        self.cv_change_factor = len(self.polynomials[str(self.degree)])

    ######################################
    # To get modify the value of sp in run time and write to the file
    ######################################

    def modify_sp(sp):
        self.polynomials['sp'] = sp
        with open('../config.json', 'w') as config:
            json.dump(self.polynomials, config)
        print('new sp set, value : ', sp)

    ######################################
    # To get value of the function at point x
    #  y = f(x)
    ######################################
    def eq_evaluator(self, x_value):

        # SP changer
        self.counter += 1
        if self.counter > self.sp_change_frequency:
            self.counter = 0
            self.sp = self.sp * uniform(0.8, 1.2)

        # Resetting the vale
        total = 0

        # Iterating through the data
        for index, coefficient in enumerate(reversed(self.polynomials[str(self.degree)])):
            #print(index, '  ', coefficient)
            total = total + (coefficient * (x_value ** (index)))

        self.pv = total
        data = {'sp': round(self.sp, 5),
                'pv': round(self.pv, 5),
                'cv': round(self.cv, 5)}

        w_data = str(self.cv) + ',' + \
            str(self.sp) + ',' + str(self.pv) + '\n'
        self.f.write(w_data)

        return data
