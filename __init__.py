from gym.envs.registration import register

register(
    id='pid-v0',
    entry_point='pid_env.envs:PidEnv',
)