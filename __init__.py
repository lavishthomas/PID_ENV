from gym.envs.registration import register

register(
    id='dqn-pid-v0',
    entry_point='pid_env.drl_envs:DQNPidEnv',
)
register(
    id='ddpg-pid-v0',
    entry_point='pid_env.drl_envs:DDPGPidEnv',
)
