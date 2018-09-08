#!/bin/bash
#Inwall Agent

volttron-pkg package Agents/02ORV_InwallLightingAgent
# Set the agent's configuration file
volttron-pkg configure ~/.volttron/packaged/lightingagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/02ORV_InwallLightingAgent/02ORV0017886.config.json
volttron-ctl install ~/.volttron/packaged/lightingagent-0.1-py2-none-any.whl --tag Inwalllighting
volttron-pkg configure ~/.volttron/packaged/lightingagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/02ORV_InwallLightingAgent/02HUE1234569.config.json
volttron-ctl install ~/.volttron/packaged/lightingagent-0.1-py2-none-any.whl --tag livingroom
volttron-ctl enable --tag Inwalllighting
volttron-ctl enable --tag livingroom

#Fibaro Agent
volttron-pkg package Agents/20FIB_FibaroAgent
volttron-pkg configure ~/.volttron/packaged/fibaroagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/20FIB_FibaroAgent/20FIB87654321.config.json
volttron-ctl install ~/.volttron/packaged/fibaroagent-0.1-py2-none-any.whl --tag fibaro
volttron-ctl enable --tag fibaro

#Netatmo Agent
volttron-pkg package Agents/12NET_NetatmoAgent
volttron-pkg configure ~/.volttron/packaged/netatmoagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/12NET_NetatmoAgent/12NET123451231.config.json
volttron-ctl install ~/.volttron/packaged/netatmoagent-0.1-py2-none-any.whl --tag netatmo
volttron-ctl enable --tag netatmo

#Yale Agent
volttron-pkg package Agents/09YAL_YaleAgent
volttron-pkg configure ~/.volttron/packaged/yaleagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/09YAL_YaleAgent/09YAL1234567.config.json
volttron-ctl install ~/.volttron/packaged/yaleagent-0.1-py2-none-any.whl --tag yale
volttron-ctl enable --tag yale

#OpenClose Agent
volttron-pkg package Agents/18ORC_OpenCloseAgent
volttron-pkg configure ~/.volttron/packaged/opencloseagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/18ORC_OpenCloseAgent/18OPC23451237.config.json
volttron-ctl install ~/.volttron/packaged/opencloseagent-0.1-py2-none-any.whl --tag openclose
volttron-ctl enable --tag openclose

#Curtain Agent
volttron-pkg package Agents/08SOM_CurtainAgent
volttron-pkg configure ~/.volttron/packaged/certainagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/08SOM_CurtainAgent/08SOM123457.config.json
volttron-ctl install ~/.volttron/packaged/certainagent-0.1-py2-none-any.whl --tag curtain
volttron-ctl enable --tag curtain


#Motion Agent
volttron-pkg package Agents/21ORV_MotionAgent
volttron-pkg configure ~/.volttron/packaged/motionagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/21ORV_MotionAgent/21ORV23451231.config.json
volttron-ctl install ~/.volttron/packaged/motionagent-0.1-py2-none-any.whl --tag motion
volttron-ctl enable --tag motion


#Plug Agent
volttron-pkg package Agents/03WSP_PlugAgent
volttron-pkg configure ~/.volttron/packaged/plugagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/03WSP_PlugAgent/03WSP123456.config.json
volttron-ctl install ~/.volttron/packaged/plugagent-0.1-py2-none-any.whl --tag Plug
volttron-ctl enable --tag Plug


#HUE Agent
volttron-pkg package Agents/02HUE_HueAgent
volttron-pkg configure ~/.volttron/packaged/lightingagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/02HUE_HueAgent/02HUE1234561.config.json
volttron-ctl install ~/.volttron/packaged/lightingagent-0.1-py2-none-any.whl --tag Hue
volttron-ctl enable --tag Hue

#mqtt
volttron-pkg package Agents/mqttsubAgent
volttron-pkg configure ~/.volttron/packaged/mqttsubagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/mqttsubAgent/mqttsub.config
volttron-ctl install ~/.volttron/packaged/mqttsubagent-0.1-py2-none-any.whl --tag mqtt
volttron-ctl enable --tag mqtt


#powermeter1
volttron-pkg package Agents/05CRE_PowerMeterAgent
volttron-pkg configure ~/.volttron/packaged/powermeteragent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/05CRE_PowerMeterAgent/05CRE0250883397.config.json
volttron-ctl install ~/.volttron/packaged/powermeteragent-0.1-py2-none-any.whl --tag powermeter1
volttron-ctl enable --tag powermeter1

#automation
volttron-pkg package Agents/AutomationManagerAgent
volttron-pkg configure ~/.volttron/packaged/automation_manageragent-3.2-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/AutomationManagerAgent/automationmanageragent.launch.json
volttron-ctl install ~/.volttron/packaged/automation_manageragent-3.2-py2-none-any.whl --tag automationmanager
volttron-ctl enable --tag automationmanager

#Scenesetup
volttron-pkg package Agents/ScenesetupAgent
volttron-pkg configure ~/.volttron/packaged/setupsceneagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/ScenesetupAgent/1KR221445K1200138.config.json
volttron-ctl install ~/.volttron/packaged/setupsceneagent-0.1-py2-none-any.whl --tag scenesetup
volttron-ctl enable --tag scenesetup


#Scene
volttron-pkg package Agents/SceneAgent
volttron-pkg configure ~/.volttron/packaged/sceneagentagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/SceneAgent/sceneconfig.json
volttron-ctl install ~/.volttron/packaged/sceneagentagent-0.1-py2-none-any.whl --tag scene
volttron-ctl enable --tag scene


#air
volttron-pkg package Agents/01DAI_ACAgent
volttron-pkg configure ~/.volttron/packaged/acagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/01DAI_ACAgent/01DAI1200101.config.json
volttron-ctl install ~/.volttron/packaged/acagent-0.1-py2-none-any.whl --tag saijo

volttron-pkg configure ~/.volttron/packaged/acagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/01DAI_ACAgent/01DAI1200100.config.json
volttron-ctl install ~/.volttron/packaged/acagent-0.1-py2-none-any.whl --tag daikin

#TPlink
volttron-pkg package Agents/03WSP_TplinkPlugAgent
volttron-pkg configure ~/.volttron/packaged/acagent-0.1-py2-none-any.whl ~/workspace/hive_os/volttron/Agents/03WSP_TplinkPlugAgent/03WSP123491.config.json
volttron-ctl install ~/.volttron/packaged/acagent-0.1-py2-none-any.whl --tag tplink
volttron-ctl enable --tag tplink

echo "GGG!"
