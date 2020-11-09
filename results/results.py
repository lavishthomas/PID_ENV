
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd   
import glob
import os

import numpy as np
mu = 1  # Means
sigma = .2
points = 10
s = np.random.normal(mu, sigma, points)
##############################################################################################################
path = 'C:/Users/lavisht/AppData/Local/Programs/Python/Python38/Lib/site-packages/pid_env/drl_pid/dsc/dqn/*'
list_of_files = glob.glob(path) # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)

a = pd.read_csv(latest_file)
b = [x for x in range(len(a))]


plt.figure(figsize=(15,10))
plt.plot(b, a['sp'], c='g')
plt.plot(b, a['pv'], c='r')
plt.plot(b, a['cv'], c='b')
plt.savefig('dqn_full.png')
##############################################################################################################
path = 'C:/Users/lavisht/AppData/Local/Programs/Python/Python38/Lib/site-packages/pid_env/drl_pid/dsc/sarsa/*'
list_of_files = glob.glob(path) # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)

a = pd.read_csv(latest_file)
b = [x for x in range(len(a))]


plt.figure(figsize=(15,10))
plt.plot(b, a['sp'], c='g')
plt.plot(b, a['pv'], c='r')
plt.plot(b, a['cv'], c='b')
plt.savefig('sarsa_full.png')
##############################################################################################################
path = 'C:/Users/lavisht/AppData/Local/Programs/Python/Python38/Lib/site-packages/pid_env/drl_pid/dsc/sarsa/*'
list_of_files = glob.glob(path) # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)

a = pd.read_csv(latest_file)
b = [x for x in range(len(a))]


plt.figure(figsize=(15,10))
plt.plot(b, a['sp'], c='g')
plt.plot(b, a['pv'], c='r')
plt.plot(b, a['cv'], c='b')
plt.savefig('sarsa_full.png')
##############################################################################################################
path = 'C:/Users/lavisht/AppData/Local/Programs/Python/Python38/Lib/site-packages/pid_env/drl_pid/dsc/cem/*'
list_of_files = glob.glob(path) # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)

a = pd.read_csv(latest_file)
b = [x for x in range(len(a))]

plt.figure(figsize=(15,10))
plt.plot(b, a['sp'], c='g')
plt.plot(b, a['pv'], c='r')
plt.plot(b, a['cv'], c='b')
plt.savefig('cem_full.png')
##############################################################################################################
path = 'C:/Users/lavisht/AppData/Local/Programs/Python/Python38/Lib/site-packages/pid_env/plc_pid/data/*'
list_of_files = glob.glob(path) # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)

a = pd.read_csv(latest_file)
b = [x for x in range(len(a))]

plt.figure(figsize=(15,10))
plt.plot(b, a['sp'], c='g')
plt.plot(b, a['pv'], c='r')
plt.plot(b, a['cv'], c='b')
plt.savefig('plc_full.png')
##############################################################################################################
path = 'C:/Users/lavisht/AppData/Local/Programs/Python/Python38/Lib/site-packages/pid_env/drl_pid/dsc/dqn/*'
list_of_files = glob.glob(path) # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)

a = pd.read_csv(latest_file)

a['error'] = abs(a['sp'] - a['pv'])

first_transition = a.head(1500).tail(1000)
mean = first_transition["error"].mean()
print("first transition mean : " , mean)

last_transition = a.tail(1000)
mean = last_transition["error"].mean()
print("last transition mean : " , mean)
b = [x for x in range(len(first_transition))]

plt.figure(figsize=(10,6))
plt.plot(b, first_transition['error'], c='r')
plt.savefig('dqn_first_transition.png')
b = [x for x in range(len(first_transition))]

plt.figure(figsize=(10,6))
plt.plot(b, last_transition['error'], c='r')
plt.savefig('dqn_last_transition.png')
##############################################################################################################
path = 'C:/Users/lavisht/AppData/Local/Programs/Python/Python38/Lib/site-packages/pid_env/drl_pid/dsc/sarsa/*'
list_of_files = glob.glob(path) # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)

a = pd.read_csv(latest_file)

a['error'] = abs(a['sp'] - a['pv'])

first_transition = a.head(1500).tail(1000)
mean = first_transition["error"].mean()
print("first transition mean : " , mean)

last_transition = a.tail(1000)
mean = last_transition["error"].mean()
print("last transition mean : " , mean)
b = [x for x in range(len(first_transition))]

plt.figure(figsize=(10,6))
plt.plot(b, first_transition['error'], c='r')
plt.savefig('sarsa_first_transition.png')
b = [x for x in range(len(first_transition))]

plt.figure(figsize=(10,6))
plt.plot(b, last_transition['error'], c='r')
plt.savefig('sarsa_last_transition.png')

##############################################################################################################
path = 'C:/Users/lavisht/AppData/Local/Programs/Python/Python38/Lib/site-packages/pid_env/drl_pid/dsc/cem/*'
list_of_files = glob.glob(path) # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getctime)
print(latest_file)

a = pd.read_csv(latest_file)

a['error'] = abs(a['sp'] - a['pv'])

first_transition = a.head(1500).tail(1000)
mean = first_transition["error"].mean()
print("first transition mean : " , mean)

last_transition = a.tail(1000)
mean = last_transition["error"].mean()
print("last transition mean : " , mean)
b = [x for x in range(len(first_transition))]

plt.figure(figsize=(10,6))
plt.plot(b, first_transition['error'], c='r')
plt.savefig('cem_first_transition.png')

b = [x for x in range(len(first_transition))]

plt.figure(figsize=(10,6))
plt.plot(b, last_transition['error'], c='r')
plt.savefig('cem_last_transition.png')