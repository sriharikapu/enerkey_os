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

#sleep 2
volttron-ctl start --tag lighting
sleep 2
volttron-ctl start --tag fibaro

sleep 2
volttron-ctl start --tag netatmo
sleep 2

volttron-ctl start --tag weather
sleep 2

volttron-ctl start --tag powermeter
sleep 2
volttron-ctl start --tag yale
sleep 2
volttron-ctl start --tag openclose
sleep 2
vokttron-ctl start --tag curtain
