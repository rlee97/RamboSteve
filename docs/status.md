---
layout: default
title: Status
---


<p align="center">
<iframe width="560" height="315" src="https://www.youtube.com/embed/Y0poiHRE6E4" frameborder="0" allowfullscreen></iframe>
</p>

**PROJECT SUMMARY**

Project RamboSteve aims to teach an AI agent to efficiently use a sword and bow to kill  multiple mob types. Currently, the arena is an enclosed cuboid that spawns one enemy per episode. As of now, the agent is trained on a Q-table to find the optimal strategy for killing an enemy. At the beginning of each episode, the agent and enemy statically spawn facing one another. At each observation, the agent has multiple actions that it can take, such as moving forward or backward, attacking, using an inventory slot, and switching weapons. Based on the Q-table, the agent must take a chosen action and return a reward to update the Q-table for the given action. Since we use a Q-Table, our state space must be discretized. We keep track of distance, health, and weapons as our states. However it is important to note since the agent's camera angles are continuous, we simplify our discrete state space by automatically calculating the angle the agent must face prior to taking an action at each observation.

**APPROACH**

Our approach for our current implementation uses Q-Tabular learning. In short, our implementation is a table of valus for every state and action that we define in our environment. We begin by initializing all of our States, Actions, and Rewards (S, A, and R) to be uniform (all zeros). We then make our agent choose an action given an observation. As we observe the rewards that we obtain for each action, we update our table accordingly.

Currently, our action is chosen based on our Q-Table and epsilon. Given a state, our agent chooses an action in the table with the highest Q-Value with a $1 - epsilon$ chance of selecting a random action.

When an action is completed, we must get our new state and reward from the environment, along with updating our Q-Table with the knowledge that is obtained from the previous action. We update the Q-Table by adding our old Q-value (oldq) to our learning rate * (G - oldq). Our G value is calculated as follows.

        G = sum([self.gamma ** i * R[i] for i in range(len(R))])

        if tau + self.back_steps < T:
            G += self.gamma ** self.back_steps * self.q_table[S[-1]][A[-1]]

{% raw %}
$$  a^2 + b^2 = c^2 $$
{% endraw %}

**EVALUATION**

In order to evaluate our Q-Tabular learning implementation, we trained the agent through 1000 episodes on three different mob types: Witch, Zombie, and Skeleton.

In terms of qualitatative evaluation, we will measure how well our agent fights by observing the amount of damage taken and the amount of damage dealt. This will provide insight about whether the agent is learning to deal damage while avoiding as much damage as possible. Here is a plot on the overall health lost and the overall damage dealt.

![alt text](https://raw.githubusercontent.com/rlee97/RamboSteve/master/graphs/Overall_health_damage.png)

On observation, everytime more damage is dealt, less health is lost and vice versa. We believe that this is a good indication that our agent is properly avoiding damage while killing mobs. However, we also notice that the damage dealt and health lost does not converge. This may either be because we have not trained our agent enough, or because our epsilon value causes our decision-making to be too random.

We will now quantitatively measure how well our agent did against the Zombie mob type. Here is a plot showing the ratio of agent deaths to Zombie deaths while fighting zombies.

![alt text](https://raw.githubusercontent.com/rlee97/RamboSteve/master/graphs/Zombie_killed_mob.png)

As can be seen, the agent succeeds in killing Zombies most of the time. This indicates that our Q-Tabular learning algorithm is selecting the correct actions to kill a Zombie. However, upon further inspection, we see that the amount of rewards gained from killing zombies neither converges nor improves. This behavior is shown in the graph below.

![alt text](https://raw.githubusercontent.com/rlee97/RamboSteve/master/graphs/Zombie_rewards.png)

This behavior may be a result of our reward system. Currently, we only measure rewards by health and damage dealt. By adding more rewards and a more complex state space, our agent may begin to improve marginally.

Upon further thought, we plan on adding a Mission Time reward. This may help our learning algorithm improve by forcing it to find actions that yield the swiftest mission clear time. We will evaluate this feature in the future.

**REMAINING GOALS AND CHALLENGES**

**Goals**

Over the remaining course of the project, we plan to continue experimenting with our reward system. For instance, we will implement the mission time as a reward to place emphasis on how fast the agent clears a mission. Additionally, we will change the reward system to have negative rewards to further explore agent behavior. We will also calculate the reward for damage dealt as a function of percent damage to mob type. This is because there are several different mob types with differing amounts of health. By calculating the reward as a percentage we will be able to more accurately represent our agent's progress. Finally, we plan to add a neural network to better 
approximate q values that will scale our project to different arena sizes and different mob types. 

**Challenges**

The largest challenge that we currently face is that our agent highly favors usage of the bow over the sword. We will first attempt to explore possible causes of this behavior by changing our hyperparameters. In addition, the mission time reward as discussed in our goal section will likely provide further insight into why the agent may prefer the bow over the sword. This is because the sword deals more damage than the bow and increasing the reward for mission time could possibly lead to the agent choosing the sword over the bow. Some of our smaller challenges involve different mob types and their edge cases. Since our agent will train on different mob types, we must increase the pool of mobs that it can fight. However, some mob types such as the Zombie Pigman, will cause an unknown error in the XML. Also, when a Creeper explodes, the mission fails to terminate correctly because the creeper no longer exists in the entity list. We will need information on the creeper in the entity list to end the mission. As of now, when an episode completes, the timer continues to play until the end before the episode is terminated. The problem is unknown and we hope to fix the issue to save time and quickly train our agent.

**RESOURCES USED**

https://github.com/dennybritz/reinforcement-learning

https://github.com/Microsoft/malmo/blob/master/Malmo/samples/Python_examples/tabular_q_learning.py#L375

https://ststevens.github.io/TeamBabylon/

https://medium.com/emergent-future/simple-reinforcement-learning-with-tensorflow-part-0-q-learning-with-tables-and-neural-networks-d195264329d0

http://microsoft.github.io/malmo/0.30.0/Schemas/Mission.html

https://microsoft.github.io/malmo/0.30.0/Documentation/index.html

