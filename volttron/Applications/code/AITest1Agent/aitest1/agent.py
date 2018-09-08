# -*- coding: utf-8 -*- {{{
# vim: set fenc=utf-8 ft=python sw=4 ts=4 sts=4 et:
#
# Copyright 2017, Battelle Memorial Institute.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# This material was prepared as an account of work sponsored by an agency of
# the United States Government. Neither the United States Government nor the
# United States Department of Energy, nor Battelle, nor any of their
# employees, nor any jurisdiction or organization that has cooperated in the
# development of these materials, makes any warranty, express or
# implied, or assumes any legal liability or responsibility for the accuracy,
# completeness, or usefulness or any information, apparatus, product,
# software, or process disclosed, or represents that its use would not infringe
# privately owned rights. Reference herein to any specific commercial product,
# process, or service by trade name, trademark, manufacturer, or otherwise
# does not necessarily constitute or imply its endorsement, recommendation, or
# favoring by the United States Government or any agency thereof, or
# Battelle Memorial Institute. The views and opinions of authors expressed
# herein do not necessarily state or reflect those of the
# United States Government or any agency thereof.
#
# PACIFIC NORTHWEST NATIONAL LABORATORY operated by
# BATTELLE for the UNITED STATES DEPARTMENT OF ENERGY
# under Contract DE-AC05-76RL01830
# }}}

from __future__ import absolute_import
import datetime
from datetime import datetime
from dateutil.relativedelta import relativedelta
import logging
import sys
import settings
import os
import json
from pprint import pformat
import subprocess as sp
from volttron.platform.messaging.health import STATUS_GOOD
from volttron.platform.vip.agent import Agent, Core, PubSub, compat
from volttron.platform.agent import utils
from volttron.platform.messaging import headers as headers_mod
import psycopg2
from os.path import expanduser


utils.setup_logging()
_log = logging.getLogger(__name__)
__version__ = '3.2'
DEFAULT_MESSAGE = 'AITest1'
DEFAULT_AGENTID = "aitest1"
DEFAULT_HEARTBEAT_PERIOD = 30


def aitest1_agent(config_path, **kwargs):
    config = utils.load_config(config_path)

    def get_config(name):
        try:
            kwargs.pop(name)
        except KeyError:
            return config.get(name, '')

    agent_id = get_config('agent_id')
    message = get_config('message')
    heartbeat_period = get_config('heartbeat_period')
    netatmo_device_id = get_config('weather_device_id')
    print(netatmo_device_id)
    ac_device_id = get_config('ac_device_id')
    topic_netatmo = '/agent/zmq/update/hive/999/' + netatmo_device_id
    topic_ac = '/ui/agent/update/hive/999/' + ac_device_id

    # DATABASES
    db_host = settings.DATABASES['default']['HOST']
    db_port = settings.DATABASES['default']['PORT']
    db_database = settings.DATABASES['default']['NAME']
    db_user = settings.DATABASES['default']['USER']
    db_password = settings.DATABASES['default']['PASSWORD']

    class AITest1Agent(Agent):

        def __init__(self, config_path, **kwargs):
            super(AITest1Agent, self).__init__(**kwargs)
            self.config = utils.load_config(config_path)
            self._agent_id = self.config.get('agentid', DEFAULT_AGENTID)
            self._message = self.config.get('message', DEFAULT_MESSAGE)
            self._heartbeat_period = self.config.get('heartbeat_period',
                                                     DEFAULT_HEARTBEAT_PERIOD)
            self.conn = None
            self.cur = None
            # self.automation_control_path = None

        @Core.receiver('onsetup')
        def onsetup(self, sender, **kwargs):
            # Demonstrate accessing a value from the config file
            print('Set up CBE Data')
            self.CBE =   {100:{21.0:24, 22.0:24, 23.0:25, 24.0:26, 25.0:27, 26.0:28},
                      90:{22.0:24, 23.0:24.5, 24.0:25.5, 25.0:26, 26.0:27, 27.0:27.5},
                      80:{22.0:23.5, 23.0:24.5, 24.0:25, 25.0:25.5, 26.0:26.5, 27.0:27},
                      70:{22.0:23.5, 23.0:24, 24.0:24.5, 25.0:25, 26.0:26, 27.0:26.5, 28.0:27},
                      60:{22.0:23.5, 23.0:24, 24.0:24.5, 25.0:25, 26.0:25.5, 27.0:26, 28.0:26.5},
                      50:{23.0:23.5, 24.0:24, 25.0:24.5, 26.0:25, 27.0:25.5, 28.0:26, 29.0:26.5},
                      40:{23.0:23.5, 24.0:24, 25.0:24.5, 26.0:25, 27.0:25, 28.0:25.5, 29.0:26},
                      30:{23.0:23.5, 24.0:24, 25.0:24, 26.0:24.5, 27.0:25, 28.0:25.5, 29.0:26, 30.0:26},
                      20:{24.0:23.5, 25.0:24, 26.0:24.5, 27.0:24.5, 28.0:25, 29.0:25, 30.0:26},
                      10:{24.0:23.5, 25.0:24, 26.0:24, 27.0:24.5, 28.0:25, 29.0:25, 30.0:25.5, 31.0:26},
                       0:{25.0:24, 26.0:24, 27.0:24.5, 28.0:24.5, 29.0:25, 30.0:25, 31.0:25.5, 32.0:26}}
            print(self.CBE)

        @Core.receiver('onstart')
        def onstart(self, sender, **kwargs):
            print("On Start")
            # self.build_automation_agent(55)

        @PubSub.subscribe('pubsub', topic_netatmo)  # control AC temp
        def match_topic_create(self, peer, sender, bus,  topic, headers, message):
            print("----- Read Humidity + Air Temp from Netatmo -----")
            msg = json.loads(message)
            print(msg)

            # humidity
            print(msg['humidity'])
            self.humidity = int(round(msg['humidity'],-1))
            print("Humidity = {}".format(self.humidity))

            # # air temp
            # print(msg['temperature'])
            # self.air_temp = int(round(msg['temperature']))
            # print("Air Temp = {}".format(self.air_temp))

            try:
                if (self.humidity > 0):
                    self.ac_temp = str(self.CBE[self.humidity][self.CBE[self.humidity].keys()[-1]])
                print("OK")

            except Exception as e:
                print('error = {}'.format(e))

            # except:
            #     if self.air_temp < self.CBE[self.humidity][self.CBE[self.humidity].keys()[0]]:
            #         print('low temp')
            #         self.ac_temp = str(self.CBE[self.humidity][self.CBE[self.humidity].keys()[0]])
            #     elif self.air_temp > self.CBE[self.humidity][self.CBE[self.humidity].keys()[-1]]:
            #         print('high temp')
            #         self.ac_temp = str(self.CBE[self.humidity][self.CBE[self.humidity].keys()[-1]])
            #     else:
            #         print('Error: Set Temp AC')

            print("AC Temp = {}".format(self.ac_temp))

        @Core.periodic(heartbeat_period)
        def StatusPublish(self):
            print ""
            # TODO this is example how to write an app to control AC
            topic = topic_ac
            try:
                # message = json.dumps({'stemp': str(24.5)})
                message = json.dumps({'stemp': self.ac_temp})

            except Exception as err1:
                print('Error: Control AC = {}'.format(err1))

            print ("topic {}".format(topic))
            print ("message {}".format(message))

            self.vip.pubsub.publish(
                'pubsub', topic,
                {'Type': 'pub device status to ZMQ'}, message)

        # Update to firebase
        # self.publish_firebase()

        # Update to Azure IoT hub
        # self.publish_azure_iot_hub()

        # Update to Local
        # self.update_local()


        print("--------------------")

    Agent.__name__ = 'aitest1'
    return AITest1Agent(config_path, **kwargs)


def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''

    try:
        utils.vip_main(aitest1_agent, version=__version__)

    except Exception as e:
        _log.exception('unhandled exception')

if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
