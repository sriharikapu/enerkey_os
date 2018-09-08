#!/bin/bash
cd ~/workspace/enerkey_os/volttron

#accontrolapp1
volttron-pkg package Applications/code/AITest1Agent
volttron-pkg configure ~/.volttron/packaged/aitest1agent-3.2-py2-none-any.whl ~/workspace/enerkey_os/volttron/Applications/code/AITest1Agent/aitest1agent.launch.json
volttron-ctl install ~/.volttron/packaged/aitest1agent-3.2-py2-none-any.whl --tag accontrol
volttron-ctl enable --tag accontrol

#air

volttron-pkg package Agents/01DAI_ACAgent
volttron-pkg configure ~/.volttron/packaged/acagent-0.1-py2-none-any.whl ~/workspace/enerkey_os/volttron/Agents/01DAI_ACAgent/03WSP1234567.config.json
volttron-ctl install ~/.volttron/packaged/acagent-0.1-py2-none-any.whl --tag aircon
volttron-ctl enable --tag aircon


#mqtt
volttron-pkg package Agents/mqttsubAgent
volttron-pkg configure ~/.volttron/packaged/mqttsubagent-0.1-py2-none-any.whl ~/workspace/enerkey_os/volttron/Agents/mqttsubAgent/mqttsub.config
volttron-ctl install ~/.volttron/packaged/mqttsubagent-0.1-py2-none-any.whl --tag mqtt
volttron-ctl enable --tag mqtt

