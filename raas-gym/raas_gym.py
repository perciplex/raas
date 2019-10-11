import Pendulum

"""

Simply just a calling wrapper for different environment classes at the
moment. Eventually will be more similar to:

https://github.com/openai/gym/blob/master/gym/envs/registration.py

"""

envs_dict = {"Pendulum-v0": Pendulum.Pendulum}

valid_envs = list(envs_dict.keys())


def make(env_name):
    """

    Gets an env_name (using the same format as OpenAI gym), does basic checks,
    creates env object, returns it.

    """

    assert (env_name in valid_envs), f'Env {env_name} not valid env! Must be in: {valid_envs}'

    env = envs_dict[env_name]()
    return env


#
