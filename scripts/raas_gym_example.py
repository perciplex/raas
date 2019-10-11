import path_utils
import raas_gym

print('Creating gym object...')
# Creates and returns Pendulum env object
env_pend = raas_gym.make('Pendulum-v0')


for i in range(N_steps):
    print(f'Step {i}')
    s_next, r, done, _ = env.step(0)



print('\nDone!')


#
