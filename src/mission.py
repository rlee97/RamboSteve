from builtins import range
import sys
import os.path
import os
import sys
import time
import constants as c
import random
import world
import json
import math

import MalmoPython

def run_mission(agent_host):
    """ Run the Agent on the world """
    agent_host.sendCommand("move 0.25")
    world_state = agent_host.getWorldState()
    is_start = True
    while world_state.is_mission_running:
        #sys.stdout.write("*")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        if world_state.number_of_observations_since_last_state > 0:
            msg = world_state.observations[-1].text
            ob = json.loads(msg)
            '''Obs has the following keys:
            ['PlayersKilled', 'TotalTime', 'Life', 'ZPos', 'IsAlive',
            'Name', 'entities', 'DamageTaken', 'Food', 'Yaw', 'TimeAlive',
            'XPos', 'WorldTime', 'Air', 'DistanceTravelled', 'Score', 'YPos',
            'Pitch', 'MobsKilled', 'XP']
            '''
            print(ob.keys())

            if is_start:
                damage_dealth = ob["DamageDealt"]
                damage_taken = ob["DamageTaken"]
                mobs_killed = ob["MobsKilled"]
                is_start = False

            dmg_dealth = ob["DamageDealt"] - damage_dealth
            dmg_taken = ob["DamageTaken"] - damage_taken
            killed = ob["MobsKilled"] - mobs_killed
            # checking if we killed the enemy or not
            entity_count = 0
            for entity in ob["entities"]:
                if entity["name"] in c.MOB_TYPE:
                    entity_count += 1
            if entity_count == 0:
                agent_host.sendCommand("quit")

            xPos = ob['XPos']
            yPos = ob['YPos']
            zPos = ob['ZPos']
            yaw = ob['Yaw']
            target = getNextTarget(ob['entities'])
            print(ob['entities'])
            if target == None or target['name'] != "Zombie": # No enemies nearby
                if target != None:
                    sys.stdout.write("Not found: "+target['name'] + "\n")
                agent_host.sendCommand("move 0") # stop moving
                agent_host.sendCommand("attack 0") # stop attacking
                agent_host.sendCommand("turn 0") # stop turning
            else:# enemy nearby, kill kill kill
                deltaYaw = calcYawPitch(target['name'], target['x'], target['y'], target['z'], yaw, xPos, yPos, zPos)
                # And turn:
                agent_host.sendCommand("turn " + str(deltaYaw))
                agent_host.sendCommand("attack 1")

        for error in world_state.errors:
            print("Error:", error.text)

def getNextTarget(entities):
    for entity in entities:
        if entity['name'] != " RamboSteve ":
            return entity

def calcYawPitch(name, ex, ey, ez, selfyaw, x, y, z): #Adapted from cart_test.py
    ''' Find the mob we are following, and calculate the yaw we need in order to face it '''
    dx = ex - x
    dz = ez - z
    dy = (ey+1.95/2) - (y+1.8) #calculate height difference between our eye level and center of mass for entity
    #-- calculate deltaYaw
    yaw = -180 * math.atan2(dx, dz) / math.pi
    deltaYaw = yaw - selfyaw
    while deltaYaw < -180:
        deltaYaw += 360
    while deltaYaw > 180:
        deltaYaw -= 360
    deltaYaw /= 180.0
    return deltaYaw

def mission():
    agent_host = MalmoPython.AgentHost()

    try:
        agent_host.parse( sys.argv )
    except RuntimeError as e:
        print('ERROR:',e)
        print(agent_host.getUsage())
        exit(1)
    if agent_host.receivedArgument("help"):
        print(agent_host.getUsage())
        exit(0)

    my_mission = MalmoPython.MissionSpec(world.missionXML, True)
    my_mission_record = MalmoPython.MissionRecordSpec()

    # Attempt to start a mission:
    max_retries = 3
    for retry in range(max_retries):
        try:
            agent_host.startMission( my_mission, my_mission_record )
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print("Error starting mission:",e)
                exit(1)
            else:
                time.sleep(2)

    # Loop until mission starts:
    print("Waiting for the mission to start ", end=' ')
    world_state = agent_host.getWorldState()
    while not world_state.has_mission_begun:
        print(".", end="")
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print("Error:",error.text)

    print()
    print("Mission running ", end=' ')

    run_mission(agent_host)

    print()
    print("Mission ended")
    time.sleep(2)
    # Mission has ended.

if __name__ == '__main__':
    for i in range(c.NUM_REPEATS):
        mission()