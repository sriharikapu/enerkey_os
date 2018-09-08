#!/bin/bash




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



echo "GGG!"
