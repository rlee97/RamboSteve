---
layout: default
title: Proposal
---

## Project Rambo Steve

## Summary
Project Rambo Steve aims to create an agent that can efficiently kill an enemy within the given time frame. The agent will have a choice between a sword and a bow. 

## AI/ML Algorithms
This project will deploy reinforcement learning algorithms such as Q-learning to train the agent to maximize rewards when fighting enemies and clearing the maze.

## Evaluation Plan
Quantitative Evaluation:
Our model will mainly be evaluated on mission clear time by an agent that starts by taking random actions. However, we are considering the amount of damage taken and time spent fighting enemies. We will begin our baseline on the time it takes for the agent to clear the maze for the first time. Initially, our rewards will be somewhat uniform. As we progress, rewards will change based on how the agent reacts to different reward factors. For example, we may start by giving the agent a -5 reward for each time it takes damage and a +5 reward killing enemy, but later only give it a -1 reward for damage taken and +10 reward for killing the enemy . Because we are using reinforcement learning, we will evaluate on data from previous missions and update our agent’s actions accordingly. Our hope is that by using our reinforcement learning algorithms, our agent will improve by at least 50% from the base clear time.

Qualitative Evaluation:
Our performance will be measured on plots that visualize mission clear time per mission, rewards per mission and possibly mission clear time vs. time spent fighting enemies. Along with giving us data on how much our agent is improving, these plots will provide insight on how well our agent is fighting the enemies. Our sanity checks will test if our agent can at least kill a single enemy without dying and clear the maze. Our moonshot is to expand on our project by creating weaknesses for each enemy, having our agent clear the maze while killing multiple enemies attacking at once, and adding speed and slow potions to either quicken the clear time or obstruct the agent.

## Appointment With Instructor:
April 24th, 2019 10:30 AM
