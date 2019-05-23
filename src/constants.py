'''
    contains constants necessary for our environment
'''

# Agent constants
AGENT_NAME = "Rambo Steve"
AGENT_START = '<Placement x="15" y="5" z="15" yaw="90"/>'

# World Constants
WORLD_GENERATOR = '<FlatWorldGenerator generatorString="3;7,3,2,30*169;1;village"/>'

# Mission constants
MS_PER_TICK = 50
AGENT_TICK_RATE = int(2.5 * MS_PER_TICK)

# Mob Type
MOB_TYPE = 'Zombie'

# Environment Mode: Creative or Survival
ENV_MODE = 'Survival'
NUM_REPEATS = 10

# Arena
ARENA_WIDTH = 34
ARENA_BREADTH = 34
