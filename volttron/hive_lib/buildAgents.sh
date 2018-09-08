#!/bin/bash

#
#__author__ = "Teerapong Ponmat"
#__credits__ = ""
#__version__ = "5.0"
#__maintainer__ = "HiVE Team"
#__email__ = "peahive@gmail.com"
#__website__ = "www.peahive.github.io"
#__created__ = "2018-04-4 12:04:50"
#__lastUpdated__ = "2018-04-4 11:23:33"

cd ~/workspace/hive_os/volttron/
. env/bin/activate
volttron -vv 2>&1 | tee ~/workspace/hive_os/volttron/log/volttron.log &

sudo chmod 777 -R /.volttron/agents/
sudo rm -rf ~/.volttron/agents/*
cd ~/workspace/hive_os/


#Inwall Agent

volttron-pkg package Agents/02ORV_InwallLightingAgent
# Set the agent's configuration file
volttron-pkg configure ~/.volttron/packaged/lightingagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/02ORV_InwallLightingAgent/02ORV0017886.config.json

volttron-pkg configure ~/.volttron/packaged/lightingagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/02ORV_InwallLightingAgent/02HUE1234569.config.json
# Install the agent (volttron must be running):
volttron-ctl install ~/.volttron/packaged/lightingagent-0.1-py2-none-any.whl --tag Inwalllighting



#Fibaro Agent

volttron-pkg package Agents/20FIB_FibaroAgent

volttron-pkg configure ~/.volttron/packaged/fibaroagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/20FIB_FibaroAgent/20FIB87654321.config.json


volttron-ctl install ~/.volttron/packaged/fibaroagent-0.1-py2-none-any.whl --tag fibaro

#Netatmo Agent

volttron-pkg package Agents/12NET_NetatmoAgent

volttron-pkg configure ~/.volttron/packaged/netatmoagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/12NET_NetatmoAgent/12NET123451231.config.json


volttron-ctl install ~/.volttron/packaged/netatmoagent-0.1-py2-none-any.whl --tag netatmo



#Yale Agent

volttron-pkg package Agents/09YAL_YaleAgent

volttron-pkg configure ~/.volttron/packaged/yaleagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/09YAL_YaleAgent/09YAL1234567.config.json


volttron-ctl install ~/.volttron/packaged/yaleagent-0.1-py2-none-any.whl --tag yale

#OpenClose Agent

volttron-pkg package Agents/18ORC_OpenCloseAgent

volttron-pkg configure ~/.volttron/packaged/opencloseagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/18ORC_OpenCloseAgent/18OPC23451231.config.json


volttron-ctl install ~/.volttron/packaged/opencloseagent-0.1-py2-none-any.whl --tag openclose


#Curtain Agent

volttron-pkg package Agents/08SOM_CurtainAgent

volttron-pkg configure ~/.volttron/packaged/certainagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/08SOM_CurtainAgent/08SOM221445K.config.json

volttron-ctl install ~/.volttron/packaged/certainagent-0.1-py2-none-any.whl --tag curtain

#Motion Agent



volttron-pkg package Agents/21ORV_MotionAgent

volttron-pkg configure ~/.volttron/packaged/motionagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/21ORV_MotionAgent/21ORV23451231.config.json

volttron-ctl install ~/.volttron/packaged/motionagent-0.1-py2-none-any.whl --tag motion
volttron-ctl enable --tag motion


#Daikin Agent

volttron-pkg package Agents/01DAI_ACAgent

volttron-pkg configure ~/.volttron/packaged/acagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/01DAI_ACAgent/01DAI1200100.config.json

volttron-ctl install ~/.volttron/packaged/acagent-0.1-py2-none-any.whl --tag Daikin

#Plug Agent

volttron-pkg package Agents/03WSP_PlugAgent

volttron-pkg configure ~/.volttron/packaged/plugagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/03WSP_PlugAgent/03WSP123456.config.json

volttron-ctl install ~/.volttron/packaged/plugagent-0.1-py2-none-any.whl --tag Plug

#HUE Agent

volttron-pkg package Agents/02HUE_HueAgent

volttron-pkg configure ~/.volttron/packaged/lightingagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/02HUE_HueAgent/02HUE1234561.config.json

volttron-ctl install ~/.volttron/packaged/lightingagent-0.1-py2-none-any.whl --tag Hue

#mqtt
volttron-pkg package Agents/mqttsubAgent

volttron-pkg configure ~/.volttron/packaged/mqttsubagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/mqttsubAgent/mqttsub.config


volttron-ctl install ~/.volttron/packaged/mqttsubagent-0.1-py2-none-any.whl --tag mqtt


#powermeter1
volttron-pkg package Agents/05CRE_PowerMeterAgent

volttron-pkg configure ~/.volttron/packaged/powermeteragent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/05CRE_PowerMeterAgent/05CRE0250883398.config.json

volttron-ctl install ~/.volttron/packaged/powermeteragent-0.1-py2-none-any.whl --tag powermeter1


#air

volttron-pkg package Agents/01DAI_ACAgent

volttron-pkg configure ~/.volttron/packaged/acagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/01DAI_ACAgent/01DAI1200101.config.json

volttron-ctl install ~/.volttron/packaged/acagent-0.1-py2-none-any.whl --tag aircon

#scene setup

volttron-pkg package Agents/ScenesetupAgent

volttron-pkg configure ~/.volttron/packaged/setupsceneagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/ScenesetupAgent/1KR221445K1200138.config.json

volttron-ctl install ~/.volttron/packaged/setupsceneagent-0.1-py2-none-any.whl --tag scenesetup

#scene

volttron-pkg package Agents/SceneAgent

volttron-pkg configure ~/.volttron/packaged/sceneagentagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/SceneAgent/sceneconfig.json


volttron-ctl install ~/.volttron/packaged/sceneagentagent-0.1-py2-none-any.whl --tag scene

#automation

volttron-pkg package Agents/AutomationManagerAgent

volttron-pkg configure ~/.volttron/packaged/automation_manageragent-3.2-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/AutomationManagerAgent/automationmanageragent.launch.json


volttron-ctl install ~/.volttron/packaged/automation_manageragent-3.2-py2-none-any.whl --tag auto

#powermeter2
volttron-pkg package Agents/05CRE_PowerMeterAgent

volttron-pkg configure ~/.volttron/packaged/powermeteragent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/05CRE_PowerMeterAgent/05CRE0699639095.config.json

volttron-ctl install ~/.volttron/packaged/powermeteragent-0.1-py2-none-any.whl --tag powermeter2


volttron-pkg package Agents/AutomationControlAgent





## RUN Lighting Agent
#volttron-pkg package ~/workspace/bemoss_os/Agents/MultiBuilding/
#volttron-pkg configure /tmp/volttron_wheels/multibuildingagent-0.1-py2-none-any.whl ~/workspace/bemoss_os/Agents/MultiBuilding/multibuildingagent.launch.json
#volttron-ctl install multibuildingagent=/tmp/volttron_wheels/multibuildingagent-0.1-py2-none-any.whl
#
## Run network agent
#volttron-pkg package ~/workspace/bemoss_os/Agents/NetworkAgent/
#volttron-pkg configure /tmp/volttron_wheels/networkagent-0.1-py2-none-any.whl ~/workspace/bemoss_os/Agents/NetworkAgent/networkagent.launch.json
#volttron-ctl install networkagent=/tmp/volttron_wheels/networkagent-0.1-py2-none-any.whl



echo "HiVE OS installation complete!"
