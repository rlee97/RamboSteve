import MalmoPython
import math
import time
import json
import pickle
import constants as c
import world
import os, sys, random
import numpy as np
from collections import defaultdict, deque

class RamboSteve():
    """
    <informative stuff here later>
    """
    def __init__(self, alpha=0.3, gamma=1, epsilon=0.3, back_steps=1, q_table=None):
        self.agent = None
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.back_steps = back_steps
        self.history = []
        self.weapon = 'sword'

        if q_table:
            p_file = open(q_table, "r")
            self.q_table = pickle.load(p_file)
            p_file.close()
        else:
            """
            # States
            DISTANCE = ['close', 'near', 'far']
            HEALTH = ['low', 'med', 'high']
            WEAPONS = ['sword', 'bow']

            # Actions
            ACTIONS = {'sword': ['move 1', 'move -1', 'strafe 1', 'strafe -1', 'attack 1', 'switch'],
                       'bow': ['move 1', 'move -1', 'strafe 1', 'strafe -1', 'use 1', 'use 0', 'switch']}
            """
            self.q_table = {(dist, health, weapon): {action: 0 for action in c.ACTIONS[weapon]} for dist in c.DISTANCE
                                                                                                for health in c.HEALTH
                                                                                                for weapon in c.WEAPONS}

    def get_curr_state(self, observation, entity):
        """
        return: Tuple -> (distance, health, weapon)
        """
        if entity['name'] not in c.HEIGHT_CHART:
            return (None, None, None)

        euclid_dist = self.calculate_distance(x=observation['XPos'], 
                                              y=observation['YPos'], 
                                              z=observation['ZPos'], 
                                              ent_x=entity['x'], 
                                              ent_y=entity['y'], 
                                              ent_z=entity['z'], 
                                              mob_type=entity['name'])

        distance = self.discretize_distance(euclid_dist)
        health = self.discretize_health(observation)

        return (distance, health, self.weapon)

    def calculate_distance(self, x, y, z, ent_x, ent_y, ent_z, mob_type):
        """
        Calculates distance from mob to agent using Euclidean Distance.
        """
        x_diff = ent_x - x
        z_diff = ent_z - z
        y_diff = (ent_y + c.HEIGHT_CHART[mob_type] / 2) - (y + 1.8)
        return np.sqrt(x_diff**2 + y_diff**2 + z_diff**2)

    def discretize_health(self, observation):
        """
        Categorizes Health into low, med, high
        """
        health = observation['Life']

        return c.HEALTH[0] if health < 3 else c.HEALTH[1] if health < 10 else c.HEALTH[2]

    def discretize_distance(self, distance):
        """
        Categorizes distance in close, near, far
        """
        return c.DISTANCE[0] if distance < 3 else c.DISTANCE[1] if distance < 10 else c.DISTANCE[2]

    def get_rewards(self, health_lost, damage_dealt):
        """
        Calculates Rewards based on health lost and damage dealt

        NOTE: Add time factor?
        """
        if not health_lost and not damage_dealt:
            return c.FAILURE_REWARD

        return health_lost * c.HEALTH_REWARD + damage_dealt * c.DAMAGE_DEALT_REWARD

    def choose_action(self, curr_state, possible_actions, eps):
        """
        LOL FIX THIS LATER
        """
        return random.choice(possible_actions) if random.random() < eps else random.choice([k for k, v in self.q_table[curr_state].items() if v == max(self.q_table[curr_state].items(), key=lambda x: (x[1], x[0]))[1] and k in possible_actions])

    def calculate_yaw_to_mob(self, observation, entity):
        """
        """
        x_diff = entity['x'] - observation['XPos']
        z_diff = entity['z'] - observation['ZPos']
        yaw = observation['Yaw']
        #y_diff = (entity['y'] + c.HEIGHT_CHART[entity['name']] / 2) - (y + 1.8) 

        yaw_to_mob = -180 * math.atan2(x_diff, z_diff) / math.pi
        delta_yaw = yaw_to_mob - yaw

        while delta_yaw < -180:
            delta_yaw += 360
        while delta_yaw > 180:
            delta_yaw -= 360
        delta_yaw /= 180.0

        return delta_yaw

    def calculate_pitch_to_mob(self, observation, entity):
        """
        """
        x_diff = entity['x'] - observation['XPos']
        z_diff = entity['z'] - observation['ZPos']
        y_diff = (entity['y'] + c.HEIGHT_CHART[entity['name']] / 2) - (observation['YPos'] + 1.8) 

        height_dist = np.sqrt(x_diff**2 + z_diff**2)

        pitch = -180 * math.atan2(y_diff, height_dist) / math.pi

        delta_pitch = pitch - observation['Pitch']
        
        while delta_pitch < -180:
            delta_pitch += 360
        while delta_pitch > 180:
            delta_pitch -= 360
        delta_pitch /= 180.0

        return delta_pitch

    def update_q_table(self, tau, S, A, R, T):
        """
        Performs relevant updates for state tau.
        """
        curr_s, curr_a = S.popleft(), A.popleft()
        R.popleft()

        G = sum([self.gamma ** i * R[i] for i in range(len(S))])

        if tau + self.back_steps < T:
            G += self.gamma ** self.back_steps * self.q_table[S[-1]][A[-1]]

        old_q = self.q_table[curr_s][curr_a]
        self.q_table[curr_s][curr_a] = old_q + self.alpha * (G - old_q)


    def run(self, agent_host):
        start_time = time.time()
        self.agent = agent_host
        world_state = self.agent.getWorldState()
        S, A, R = deque(), deque(), deque()

        while world_state.is_mission_running:
            time.sleep(0.1)
            current_time = time.time()
            world_state = agent_host.getWorldState()

            if world_state.number_of_observations_since_last_state > 0:
                obs = json.loads(world_state.observations[-1].text)

            mob = None
            if obs['entities'][-1]['name']:
                mob = obs['entities'][-1]['name']



            



if __name__ == '__main__':
    agent_host = MalmoPython.AgentHost()

    try:
        agent_host.parse(sys.argv)
    except RuntimeError as e:
        print('ERROR:', e)
        print(agent_host.getUsage())
        exit(1)
    if agent_host.receivedArgument('help'):
        print(agent_host.getUsage())
