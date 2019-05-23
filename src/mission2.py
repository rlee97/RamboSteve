import time
import os
import sys
import time
import json
import constants as c
import random
import tkinter as tk
#import canvas as cnv
import environment 
from action_space import ActionSpace

try:
    import MalmoPython
except ImportError:
    import malmo.MalmoPython as MalmoPython



def getPlayerState(observed):
    is_alive = observed['IsAlive']
    life = observed['Life']
    xpos = observed['XPos']
    ypos = observed['YPos']
    zpos = observed['ZPos']
    pitch = observed['Pitch']
    yaw = observed['Yaw']

    return (is_alive, life, xpos, ypos, zpos, pitch, yaw)


def getState(observed):
    damage_dealth = observed['DamageDealt']
    damage_taken = observed['DamageTaken']
    mobs_killed = observed['MobsKilled']

    return (mobs_killed, damage_dealth, damage_taken)

def mission():
    agent = MalmoPython.AgentHost()

    try:
        agent.parse( sys.argv )
    except RuntimeError as e:
        print('ERROR:',e)
        print(agent.getUsage())
        exit(1)
    if agent.receivedArgument('help'):
        print(agent.getUsage())
        exit(0)

    my_mission = MalmoPython.MissionSpec(environment.getMissionXML(), True)
    my_mission_record = MalmoPython.MissionRecordSpec()

    # Attempt to start a mission:
    MAX_RETRIES = 10
    for retry in range(MAX_RETRIES):
        try:
            agent.startMission(my_mission, my_mission_record)
            break
        except RuntimeError as e:
            if retry == MAX_RETRIES - 1:
                print('Error starting mission: {}'.format(e))
                exit(1)
            else:
                time.sleep(2)

     # Loop until mission starts:
    print('Waiting for the mission to start ', end=' ')
    world_state = agent.getWorldState()
    while not world_state.has_mission_begun:
        print('.', end='')
        time.sleep(0.1)
        world_state = agent.getWorldState()
        for error in world_state.errors:
            print('Error: {}'.format(error.text))

    print('Mission running!')

    moves = []
    action_space = ActionSpace(moves)

    agent.sendCommand('chat /give @p diamond_sword 1 0 {ench:[{id:16,lvl:1000}]}')
    #agent.sendCommand('hotbar.1 1')
    #agent.sendCommand('hotbar.1 0')
    agent.sendCommand('moveMouse 0 -75')

    while world_state.is_mission_running:
        time.sleep(c.AGENT_TICK_RATE / 1000)
        world_state = agent.getWorldState()

        action = action_space.sample()
        agent.sendCommand('attack 1')
        
        #print(world_state.number_of_observations_since_last_state)
        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            ob = json.loads(msg)
            print(ob)

        

if __name__ == '__main__':
    NUM_REPEATS = 100

    for iRepeat in range(NUM_REPEATS):
        print('Running episode {}:'.format(iRepeat))
        mission()
        print()
        # Mission has ended.
        print('Mission {} has ended.'.format(iRepeat))