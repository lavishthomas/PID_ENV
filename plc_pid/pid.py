# Custom Library
from process.process import Process
import time


from simple_pid import PID

######################################
# Intializing Process
######################################
process = Process()

# New PV is calculated by the process
new_values = process.eq_evaluator(process.cv)
# New sp value based on the equation
process.sp = new_values['sp']
# New pv value based on the equation
process.pv = new_values['pv']

pid = PID(.005, 1, .0005, setpoint=process.sp, sample_time=0.01)

# assume we have a system we want to control in controlled_system
v = process.pv

for i in range(0, 10000):
    process.cv = pid(process.pv)
    process.cv = round(process.cv, 5)
    new_values = process.eq_evaluator(process.cv)
    process.pv = new_values['pv']
    pid.setpoint = process.sp
    print('cv', process.cv, 'pv', process.pv)
    time.sleep(.01)
