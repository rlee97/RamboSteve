import MalmoPython
import malmoutils
import math
import time
import json
import pickle
import constants as c
import world
import os, sys, random
import numpy as np
import pandas as pd
from collections import defaultdict, deque

# recorded_file_name = os.getcwd() + "test.tgz"
here = os.path.dirname(os.path.abspath(__file__))


class RamboSteve():
    """
    Args
            alpha:  <float>  learning rate
            gamma:  <float>  value decay rate
            n:      <int>    number of back steps to update
            epsilon: <float> chance of taking a random action
    """
    def __init__(self, alpha=0.3, gamma=1, epsilon=0.25 , back_steps=25, q_table=None):
        self.agent = None
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.back_steps = back_steps
        self.history = pd.DataFrame(columns=['episode', 'mob_type', 'total_damage_dealt', 'total_health_lost', 'total_time', 'min_reward', 'max_reward','killed_mob', 'episode_time'])
        self.weapon = 'sword'
        self.qtable_fname = 'q_table_a{}_g{}_eps{}_n{}.p'.format(self.alpha, self.gamma, self.epsilon, self.back_steps)
        self.results_fname = 'results_a{}_g{}_eps{}_n{}'.format(self.alpha, self.gamma, self.epsilon, self.back_steps)

        if q_table:
            with open(q_table, 'rb') as f:
                self.q_table = pickle.load(f)
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
            self.q_table = {(dist, health, weapon, mob): {action: 0 for action in c.ACTIONS[weapon]} for dist in c.DISTANCE
                                                                                                     for health in c.HEALTH
                                                                                                     for weapon in c.WEAPONS
                                                                                                     for mob in list(c.HEIGHT_CHART)}

    def get_curr_state(self, observation, entity):
        """
        return: Tuple -> (distance, health, weapon)
        """
        if entity['name'] not in c.HEIGHT_CHART:
            print(entity['name'])
            return ('finished', )

        euclid_dist = self.calculate_distance(x=observation['XPos'], 
                                              y=observation['YPos'], 
                                              z=observation['ZPos'], 
                                              ent_x=entity['x'], 
                                              ent_y=entity['y'], 
                                              ent_z=entity['z'], 
                                              mob_type=entity['name'])

        distance = self.discretize_distance(euclid_dist)
        health = self.discretize_health(observation)

        return (distance, health, self.weapon, entity['name'])

    def calculate_distance(self, x, y, z, ent_x, ent_y, ent_z, mob_type):
        """
        Calculates distance from mob to agent using Euclidean Distance.
        """
        x_diff = ent_x - x
        z_diff = ent_z - z
        y_diff = (ent_y + c.HEIGHT_CHART[mob_type] / 2) - (y + 1.8)
        print('distance from mob: {}'.format(np.sqrt(x_diff**2 + y_diff**2 + z_diff**2)))
        return np.sqrt(x_diff**2 + y_diff**2 + z_diff**2)

    def discretize_health(self, observation):
        """
        Categorizes Health into low, med, high
        """
        health = observation['Life']

        return c.HEALTH[0] if health < 1.5 else c.HEALTH[1] if health < 7 else c.HEALTH[2]

    def discretize_distance(self, distance):
        """
        Categorizes distance in close, near, far
        """
        return c.DISTANCE[0] if distance < 3 else c.DISTANCE[1] if distance < 10 else c.DISTANCE[2]

    def get_rewards(self, health_lost, damage_dealt, episode_time, mob_health):
        """
        Calculates Rewards based on health lost and damage dealt

        NOTE: Add time factor?
        """
        # Possibly increase reward the lower the episode time is, so + 1/episode_time * EPISODE_TIME_REWARD
        reward = health_lost * c.HEALTH_REWARD + damage_dealt * c.DAMAGE_DEALT_REWARD

        if mob_health == 0:
            reward += c.KILL_REWARD

        return reward

    def choose_action(self, curr_state, possible_actions, eps):
        """
        LOL FIX THIS LATER
        tried to do a 1 liner and it didn't work :(
        """
        # return random.choice(possible_actions) if random.random() < eps else random.choice([k for k, v in self.q_table[curr_state].items() if v == max(self.q_table[curr_state].items(), key=lambda x: (x[1], x[0]))[1] and k in possible_actions])
        q_actions = [a for a in self.q_table[curr_state].items() if a[0] in possible_actions]
        max_state = max([i[1] for i in self.q_table[curr_state].items()])
        max_states = [action[0] for action in q_actions if action[1] == max_state]
        rnd = random.random()
        if rnd < eps:
            return random.choice(possible_actions)
            # a = random.randint(0, len(possible_actions) - 1)
            # return possible_actions[a]
        return random.choice(max_states)

    def calculate_yaw_to_mob(self, observation, entity):
        """
        Turns agent to face mob
        """
        x_diff = entity['x'] - observation['XPos']
        z_diff = entity['z'] - observation['ZPos']
        yaw = observation['Yaw']
        # y_diff = (entity['y'] + c.HEIGHT_CHART[entity['name']] / 2) - (y + 1.8) 

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
        Changes pitch to look at mob.
        """
        x_diff = entity['x'] - observation['XPos']
        z_diff = entity['z'] - observation['ZPos']
        if self.weapon == 'sword':
            y_diff = (entity['y'] + c.HEIGHT_CHART[entity['name']] / 2) - (observation['YPos'] + 1.8)
        else:
            y_diff = (entity['y'] + c.HEIGHT_CHART[entity['name']]) - (observation['YPos'] + 1.8)

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

        G = sum([self.gamma ** i * R[i] for i in range(len(R))])

        if tau + self.back_steps < T:
            G += self.gamma ** self.back_steps * self.q_table[S[-1]][A[-1]]

        old_q = self.q_table[curr_s][curr_a]
        self.q_table[curr_s][curr_a] = old_q + self.alpha * (G - old_q)

    def track_target(self, observation, entity):
        """
        Calculates yaw and pitch to face mob.
        """
        if not self.agent:
            return
        
        if entity['name'] in c.HEIGHT_CHART.keys():
            delta_yaw = self.calculate_yaw_to_mob(observation, entity)
            delta_pitch = self.calculate_pitch_to_mob(observation, entity)
            self.agent.sendCommand('turn {}'.format(delta_yaw))
            # time.sleep(0.1)
            # self.agent.sendCommand("turn 0")
            self.agent.sendCommand('pitch {}'.format(delta_pitch))
        else:
            self.agent.sendCommand('turn 0')
            self.agent.sendCommand('pitch 0')
            self.agent.sendCommand('move 0')
            self.agent.sendCommand('attack 0')

    def perform_action(self, action):
        """
        Performs action (mainly to target switch commands).
        """
        if action == 'switch' and self.weapon == 'sword':
            self.agent.sendCommand('hotbar.2 1')
            self.agent.sendCommand('hotbar.2 0')
            self.weapon = 'bow'
            self.agent.sendCommand('use 0')
        elif action == 'switch' and self.weapon == 'bow':
            self.agent.sendCommand('hotbar.1 1')
            self.agent.sendCommand('hotbar.1 0')
            self.weapon = 'sword'
            self.agent.sendCommand('use 0')
        else:
            self.agent.sendCommand(action)

    def clear_action(self, action):
        """
        Send a command to negate the given action
        """
        print("action being cleared:", action)

        if 'attack' in action:
            self.agent.sendCommand("attack 0")
        if 'use' in action:
            self.agent.sendCommand("use 0")
        elif 'switch' in action:
            self.agent.sendCommand("use 0")
        elif 'strafe' in action:
            self.agent.sendCommand("strafe 0")
        elif 'move' in action:
            self.agent.sendCommand("move 0")

    def clear_all_actions(self):
        """
        Clear all actions when a mission is completed.
        """
        self.agent.sendCommand("attack 0")
        self.agent.sendCommand("use 0")
        self.agent.sendCommand("strafe 0")
        self.agent.sendCommand("move 0")
        self.agent.sendCommand("turn 0")
        self.agent.sendCommand("pitch 0")

    def run(self, agent_host, episode):
        """
        Runs an episode.
        """
        start_time = time.time()
        self.agent = agent_host
        world_state = self.agent.getWorldState()
        S, A, R = deque(), deque(), deque()
        time_step = 0
        last_action_time = 0
        first_loop = True
        max_score = 0
        min_score = 1000
        state = ('', )
        action = ''
        mob_dead = False

        self.agent.sendCommand('chat EPISODE #{}'.format(episode))

        while world_state.is_mission_running and not mob_dead:
            # time.sleep(0.1)
            current_time = time.time()
            world_state = agent_host.getWorldState()

            if world_state.number_of_observations_since_last_state > 0:
                obs = json.loads(world_state.observations[-1].text)
            else:
                continue

            if 'Name' not in obs:
                continue 

            mob = None
            for ent in obs['entities']:
                if ent['name'] in c.HEIGHT_CHART:
                    mob = ent['name']
                    entity = ent

            if not mob:
                # state = ('last check', )
                continue

            self.track_target(obs, entity)

            if current_time - last_action_time >= 300:
                state = self.get_curr_state(obs, entity)

                possible_actions = c.ACTIONS[self.weapon]
                action = self.choose_action(state, possible_actions, self.epsilon)

                damage_dealt = 0
                health_lost = 0
                episode_time = 1

                if first_loop:
                    total_agent_health = obs['Life']
                    total_mob_health = entity['life']
                    agent_health = obs['Life'] 
                    mob_health = entity['life']
                    total_time = obs['TotalTime']
                    
                else:
                    total_health_lost = total_agent_health - obs['Life']
                    total_damage_dealt = total_mob_health - entity['life']
                    damage_dealt = mob_health - entity['life']
                    health_lost = agent_health - obs['Life']
                    agent_health = obs['Life'] 
                    mob_health = entity['life']
                    episode_time = obs['TotalTime'] - total_time + 1

                check_entities = json.loads(world_state.observations[-1].text)['entities']
                print(set(ent['name'] for ent in check_entities))
                
                # Calculate the score
                score = self.get_rewards(health_lost, damage_dealt, episode_time, mob_health)
                print("Score at current time:", score)
                max_score = max(score, max_score)
                min_score = min(score, min_score)

                R.append(score)
                T = time_step - self.back_steps + 1
                if T > 0:
                    self.update_q_table(time_step, S, A, R, T)

                S.append(state)
                A.append(action)
                time_step += 1
                print('Time Step: {}, Action: {}'.format(time_step, action))
                self.perform_action(action)

                # If the mob is dead, clear actions
                if entity['life'] == 0:
                        print('{} IS MURDERED'.format(mob))
                        mob_dead = True
                        self.clear_all_actions()

                first_loop = False

                if state == ('finished',):
                    break

        total_time = time.time() - start_time
        print('max_score: {}, min_score: {}'.format(max_score, min_score))
        print('mob: {}, damage_dealt: {}, health_lost: {}, total_time: {}'.format(mob, damage_dealt, health_lost, total_time))

        # 'episode', 'mob_type', 'total_damage_dealt', 'total_health_lost', 'total_time', 'min_reward', 'max_reward','killed_mob', 'episode_time'
        self.history = self.history.append({'episode': episode, 
                                            'mob_type': mob, 
                                            'total_damage_dealt': total_damage_dealt, 
                                            'total_health_lost': total_health_lost, 
                                            'total_time': total_time, 
                                            'min_reward': min_score, 
                                            'max_reward': max_score, 
                                            'killed_mob': mob_dead,
                                            'episode_time': episode_time}, ignore_index=True)


    def save_q_table(self):
        try:
            with open(os.path.join(here, self.qtable_fname), 'wb+') as f:
                print('Saving qtable into {}'.format(self.qtable_fname))
                pickle.dump(dict(self.q_table), f)

        except Exception as e:
            print(e)

    def save_results(self):
        print('Saving results into {}'.format(self.results_fname))
        self.history.to_csv('{}.csv'.format(self.results_fname), index=False)

    """
    def save_results(self, append=False):
        try:
            f = open(self.results_fname, 'a+' if append else 'w+')
            for result in self.history:
                f.write(str(result[0]) + ',')
                f.write(str(result[1]) + ',')
                f.write('{:5.3f},'.format(result[2]))
                f.write('{}'.format(result[3]))
                f.write('\n')
            f.close()
        except Exception as e:
            print(e)
    """
def run_mission(rambo_steve, episode):
    agent_host = MalmoPython.AgentHost()

    try:
        agent_host.parse(sys.argv)
    except RuntimeError as e:
        print('ERROR:', e)
        print(agent_host.getUsage())
        exit(1)
    if agent_host.receivedArgument('help'):
        print(agent_host.getUsage())

    my_mission = MalmoPython.MissionSpec(world.getMissionXML(), True)
    # adding the recordedFileName into MissionRecordSpec
    my_mission_record = MalmoPython.MissionRecordSpec()
    # my_mission = malmoutils.get_default_recording_object(agent_host, "Mission")
    # adding the spec for adding the recording of the video
    # my_mission.requestVideo(1280, 720)
    # my_mission_record.recordMP4(30, 2000000)

    # set up client to connect:
    my_clients = MalmoPython.ClientPool()
    for i in range(5):
        my_clients.add(MalmoPython.ClientInfo('127.0.0.1', c.MISSION_CONTROL_PORT + i))

    # Attempt to start a mission:
    print('Attempting to start mission...')
    max_retries = 5
    for retry in range(max_retries):
        try:
            agent_host.startMission( my_mission, my_clients, my_mission_record, 0, "RamboSteve" )
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print('Error starting mission:',e)
                exit(1)
            else:
                time.sleep(2)

    # Loop until mission starts:
    print('Waiting for the mission to start ', end=' ')
    world_state = agent_host.getWorldState()
    while not world_state.has_mission_begun:
        print('.', end='')
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            print('Error:',error.text)

    print()
    print('Mission running ', end=' ')

    rambo_steve.run(agent_host, episode)

    print()
    print('Mission ended')
    time.sleep(2)

if __name__ == '__main__':
    rambo_steve = RamboSteve()

    for episode in range(c.NUM_REPEATS):
        run_mission(rambo_steve, episode + 1)

    rambo_steve.save_q_table()
    rambo_steve.save_results()