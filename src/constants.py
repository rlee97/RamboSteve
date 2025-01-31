'''
    contains constants necessary for our environment
'''

# Agent constants
AGENT_NAME = "RamboSteve"
AGENT_START = '<Placement x="15 " y="5" z="15" yaw="90"/>'

# World Constants
WORLD_GENERATOR = '<FlatWorldGenerator generatorString="3;7,3,2,30*169;1;village"/>'

# Mission constants
MS_PER_TICK = 30
AGENT_TICK_RATE = int(2.5 * MS_PER_TICK)

# Mob Type
MOB_TYPE = 'Zombie'

# Environment Mode: Creative or Survival
ENV_MODE = 'Survival'
NUM_REPEATS = 300

# Arena 
ARENA_WIDTH = 34
ARENA_BREADTH = 34

# Heights of all the enemies that we are doing:
# HEIGHT_CHART = {'Creeper':1.7, 'Skeleton':1.95, 'Spider':1, 'Zombie':1.95,
#     'Ghast':4, 'Zombie Pigman':1.95, 'Cave Spider':1, 'Silverfish':0.3,
#     'Blaze':2, 'Witch':1.95, 'Endermite':0.3, 'Wolf': 0.85
# }
# , 'Skeleton':1.95, 'Zombie':1.95, 'Ghast':4, 'Blaze':2}

HEIGHT_CHART = {'Witch' : 1.95 }

# States
DISTANCE = ['close', 'near', 'far']
HEALTH = ['low', 'med', 'high']
WEAPONS = ['sword', 'bow']

# Actions
ACTIONS = {'sword': ['move 1', 'move -1', 'strafe 1', 'strafe -1', 'attack 1', 'switch'],
           'bow': ['move 1', 'move -1', 'strafe 1', 'strafe -1', 'use 1', 'use 0', 'switch']}

# Rewards
HEALTH_REWARD = -10
DAMAGE_DEALT_REWARD = 15
FAILURE_REWARD = -100
EPISODE_TIME_REWARD = 0
KILL_REWARD = 100
#MAX_SCORE = 0
#MIN_SCORE = 100

# MISSION CONTROL PORT
MISSION_CONTROL_PORT = 10000
