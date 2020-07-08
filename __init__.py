from gym.envs.registration import register

register(
    id='discrete-pid-v0',
    entry_point='pid_env.drl_envs:DiscreteProcess',
)
register(
    id='continuous-pid-v0',
    entry_point='pid_env.drl_envs:ContinuousProcess',
)

