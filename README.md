# PID_ENV

### Purpose

The Motivation behind this research is to demonstrate the implementation of AI technology in the field of industrial automation. Currently, all control systems are programmed explicitly using various mathematical functions which have to be fine-tuned after iterations of testing (Shang et al. 2013). Implementation of a reinforcement learning agent will reduce the time-lapse by auto-adjusting to the requirement. Integration of deep learning framework has increased the reinforcement learning agent’s performance (Qin et al. 2018). Therefore, this project will be an attempt to create a deep reinforcement learning agent (DL + RL) which can imitate the behaviour of a PID controller. 

### Modules

<ol>
<li>Environments</li>
<li>Agents</li>
<li>Process Library</li>
<li>Simple-PID implmentation</li>
<li>Data Plot</li>
<ol>
------------

### Pre requiste

pip install gym
https://github.com/openai/gym#installation

pip install keras-rl
https://github.com/keras-rl/keras-rl

### Steps to run 

checkout the library to 
"C:\Users\lavis\AppData\Local\Programs\Python\Python38\Lib\site-packages\"
navigate to the folder location and install using pip

pip install -e .

### Process library

This library controls the behaviour of the process systems.
The equations can be edited using the config.json file.

### DRL environments

This library introduces to new environments to the OpenAI gym

1) Discrete
2) Continous 

### DRL agents

This library tests three agents provided by the keras-rl library to run optimization problem for PID controller.
