import gym
import retro
env = retro.make('GalagaDemonsOfDeath-Nes')
import random


observation = env.reset()
fitness = 0
for t in range(1000):
    env.render()

    action = random

    observation, reward, done, info = env.step(action)
        
    fitness += reward
    if done:
        print("Episode finished after {} timesteps".format(t+1))
        env.close()
        break

print(fitness)
