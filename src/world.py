import constants as c
import random

def spawnMob(numMobs):
  spawnXML = ""
  for i in range(numMobs):
    print(str(random.choice(list(c.HEIGHT_CHART))))
    spawnXML = spawnXML + "<DrawEntity x=\"10\" y=\"5\" z=\"15\" type=\"" + str(random.choice(list(c.HEIGHT_CHART))) + "\"/>"
    print(spawnXML)
  return spawnXML

def getMissionXML():
  missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://ProjectMalmo.microsoft.com Mission.xsd">  
      <About>    
        <Summary/>  
      </About>

      <ModSettings>
        <MsPerTick>
          ''' + str(c.MS_PER_TICK) + '''
        </MsPerTick>
      </ModSettings>

      <ServerSection>
        <ServerInitialConditions>
        <AllowSpawning>false</AllowSpawning>
        <AllowedMobs>Zombie</AllowedMobs>              
        <Time>                    
          <StartTime>12000</StartTime>                    
          <AllowPassageOfTime>true</AllowPassageOfTime>                
        </Time>
        <Weather>rain</Weather>
        </ServerInitialConditions>
        <ServerHandlers>
          ''' + c.WORLD_GENERATOR + '''
          <DrawingDecorator>
            <DrawCuboid x1="0" y1="4" z1="0" x2="36" y2="22" z2="36" type="barrier"/>
            <DrawCuboid x1="1" y1="5" z1="1" x2="35" y2="21" z2="35" type="air"/>
            ''' + spawnMob(1) + '''
          </DrawingDecorator>
          <ServerQuitFromTimeUp timeLimitMs="30000"/>
          <ServerQuitWhenAnyAgentFinishes/>
        </ServerHandlers>
      </ServerSection>
      
      <AgentSection mode="Survival">
        <Name> ''' + c.AGENT_NAME + ''' </Name>
        <AgentStart>
          <Inventory>
            <InventoryItem slot="0" type="diamond_sword"/>
            <InventoryItem slot="1" type="bow"/>
            <InventoryItem slot="2" type="arrow" quantity="64"/>
          </Inventory>
          ''' + c.AGENT_START + '''
        </AgentStart>
        <AgentHandlers>
          <MissionQuitCommands
            quitDescription="finished murdering">
              <ModifierList
                type='allow-list'>
                  <command>quit</command>
              </ModifierList>
          </MissionQuitCommands>
          <ObservationFromFullStats/>
          <AgentQuitFromTimeUp timeLimitMs="'''+str(30000)+'''" description="out_of_time"/>
          <ContinuousMovementCommands turnSpeedDegs="900"/>
          <InventoryCommands>
            <ModifierList type = "deny-list">
                <command>discardCurrentItem</command>
            </ModifierList>
          </InventoryCommands>
          <ObservationFromNearbyEntities>
            <Range name="entities" xrange="'''+str(35)+'''" yrange="'''+str(35)+'''" zrange="'''+str(35)+'''" />
          </ObservationFromNearbyEntities>
          <ObservationFromHotBar/>
          <ChatCommands/>
        </AgentHandlers>
      </AgentSection>
    </Mission>'''
  return missionXML