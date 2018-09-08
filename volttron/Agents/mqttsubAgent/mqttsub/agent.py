# -*- coding: utf-8 -*-
from __future__ import absolute_import
from azure.servicebus import ServiceBusService, Message, Topic, Rule, DEFAULT_RULE_NAME
from datetime import datetime
import logging
import sys
import settings
from pprint import pformat
from volttron.platform.messaging.health import STATUS_GOOD
from volttron.platform.messaging.health import STATUS_GOOD
from volttron.platform.vip.agent import Agent, Core, PubSub, compat
from volttron.platform.agent import utils
from volttron.platform.messaging import headers as headers_mod
import importlib
import random

# from zmqhelper.ZMQHelper.zmq_pub import ZMQ_PUB
import requests
import json
import time
import logging
import os
from volttron.platform.agent import utils, matching
from uuid import getnode as get_mac
import fcntl, socket, struct
import settings
from os.path import expanduser
import psycopg2.extras
import psycopg2

import json
from os.path import expanduser


utils.setup_logging()
_log = logging.getLogger(__name__)
__version__ = '3.2'
DEFAULT_MESSAGE = 'HELLO'

# Step1: Agent Initialization
def mqttsub_agent(config_path, **kwargs):
    config = utils.load_config(config_path)
    def get_config(name):
        try:
            kwargs.pop(name)
        except KeyError:
            return config.get(name, '')

    service_namespace = settings.AZURE['servicebus']['service_namespace']
    shared_access_key_name = settings.AZURE['servicebus']['shared_access_key_name']
    shared_access_key_value = settings.AZURE['servicebus']['shared_access_key_value']
    servicebus_topic = settings.gateway_id
    sbs = ServiceBusService(
        service_namespace=service_namespace,
        shared_access_key_name=shared_access_key_name,
        shared_access_key_value=shared_access_key_value)


    # DATABASES
    db_host = settings.DATABASES['default']['HOST']
    db_port = settings.DATABASES['default']['PORT']
    db_database = settings.DATABASES['default']['NAME']
    db_user = settings.DATABASES['default']['USER']
    db_password = settings.DATABASES['default']['PASSWORD']
    gateway_id = settings.gateway_id
    class mqttsubAgent(Agent):
        """Listens to everything and publishes a heartbeat according to the
        heartbeat period specified in the settings module.
        """

        def __init__(self, config_path, **kwargs):
            super(mqttsubAgent, self).__init__(**kwargs)
            self.config = utils.load_config(config_path)

        @Core.receiver('onsetup')
        def onsetup(self, sender, **kwargs):
            # Demonstrate accessing a value from the config file
            _log.info(self.config.get('message', DEFAULT_MESSAGE))
            self._agent_id = self.config.get('agentid')

        @Core.receiver('onstart')
        def onstart(self, sender, **kwargs):
            _log.debug("VERSION IS: {}".format(self.core.version()))

            while True:
                try:

                    msg = sbs.receive_subscription_message(servicebus_topic, 'client1', peek_lock=False)
                    print msg
                    if msg.body is not None:
                        commsg = eval(msg.body)
                        print commsg
                        # print("message MQTT received datas")
                        type_msg = str(commsg.get('type', None))
                        if type_msg.startswith('scene'): # TODO : Recheck condition again
                            # print('Found scene')
                            self.VIPPublishApplication(commsg, type_msg)

                        elif type_msg == 'devicecontrol':
                            # Execute Device Control Function
                            # print("Device Cintrol Event")
                            self.VIPPublishDevice(commsg)

                        elif type_msg == 'login':

                            self.VIPPublishApplication(commsg, type_msg)
                            # TODO : Pub message again to Notifier agent to Store TOKEN VALUE
                            self.vip.pubsub.publish('pubsub',
                                                    '/ui/agent/update/notifier',
                                                    message=json.dumps(commsg),
                                                    )

                            home_path = expanduser("~")
                            json_path = '/workspace/hive_os/volttron/token.json'
                            automation_control_path = home_path + json_path
                            launcher = json.load(open(home_path + json_path, 'r'))  # load config.json to variable
                            #  Update new agentID to variable (agentID is relate to automation_id)
                            self.updatetoken(commsg)

                        elif type_msg == 'automationcreate':
                            # Execute Create Automation Function
                            # print("Create Automation Event")
                            self.VIPPublishApplication(commsg, type_msg)

                        elif type_msg == 'automationdelete':
                            # Execute Delete Automation Function
                            # print("Delete Automation Event")
                            self.VIPPublishApplication(commsg, type_msg)

                        elif type_msg == 'automationupdate':
                            # Execute Update Automation Function
                            # print("Update Automation Event")
                            self.VIPPublishApplication(commsg, type_msg)

                        else:
                            pass
                            # print "---------------------------------------"
                            # print('Any Topic :')
                            # print servicebus_topic
                            # print commsg
                            # print "---------------------------------------"
                    else:
                        pass
                        # print servicebus_topic
                        # print "No body message"

                except Exception as er:
                    print er

        def updatetoken(self,commsg):
            try:

                conn = psycopg2.connect(host=db_host, port=db_port, database=db_database, user=db_user,
                                        password=db_password)
                self.conn = conn
                self.cur = self.conn.cursor()
                self.cur.execute("""SELECT * FROM token """)
                rows = self.cur.fetchall()

                nullrow = True
                for row in rows:
                    if row[0] == gateway_id:
                        nullrow = False
                        self.api_token = row[1]
                self.conn.close()
                self.conn = psycopg2.connect(host=db_host, port=db_port, database=db_database,
                                             user=db_user, password=db_password)
                self.cur = self.conn.cursor()

                if nullrow == True:
                    self.cur.execute(
                        """INSERT INTO token (gateway_id, login_token, expo_token) 
                                                    VALUES (%s, %s, %s);""",
                        (servicebus_topic, commsg['token'], commsg['token']))

                self.cur.execute("""
                   UPDATE token
                   SET login_token=%s, expo_token=%s
                   WHERE gateway_id=%s
                """, (commsg['token'], commsg['token'],servicebus_topic))

                self.conn.commit()
                self.conn.close()

            except Exception as er:
                print("Error in insertdb : {}".format(er))

        def VIPPublishDevice(self,commsg):
            # TODO this is example how to write an app to control AC
            topic = str('/ui/agent/update/hive/999/' + str(commsg['device']))
            message = json.dumps(commsg)
            # print ("topic {}".format(topic))
            # print ("message {}".format(message))

            self.vip.pubsub.publish(
                'pubsub', topic,
                {'Type': 'HiVE Device to Gateway'}, message)

        def VIPPublishApplication(self, commsg, type_msg):
            topic = str('/ui/agent/update/hive/999/') + str(type_msg)
            message = json.dumps(commsg)
            # print ("topic {}".format(topic))
            # print ("message {}".format(message))

            self.vip.pubsub.publish(
                'pubsub', topic,
                {'Type': 'HiVE Application to Gateway'}, message)

    Agent.__name__ = 'mqttsubAgent'
    return mqttsubAgent(config_path, **kwargs)


def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(mqttsub_agent, version=__version__)
    except Exception as e:
        _log.exception('unhandled exception')


if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
