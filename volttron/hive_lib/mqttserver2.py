# -*- coding: utf-8 -*-
#UDP server responds to broadcast packets
#you can have only one instance of this running as a BEMOSS core!!
import os
import sys
os.chdir(os.path.expanduser("~/workspace/hive_os/"))  # = ~/workspace/bemoss_os
current_working_directory = os.getcwd()
sys.path.append(current_working_directory)
from azure.servicebus import ServiceBusService, Message, Topic, Rule, DEFAULT_RULE_NAME
# from zmqhelper.ZMQHelper.zmq_pub import ZMQ_PUB
import requests
import json
import time
import logging
import os
from volttron.platform.agent import utils, matching
from uuid import getnode as get_mac
import fcntl, socket, struct

from datetime import datetime
import logging
import sys
import settings
from pprint import pformat

from volttron.platform.messaging.health import STATUS_GOOD
from volttron.platform.vip.agent import Agent, Core, PubSub, compat
from volttron.platform.agent import utils
from volttron.platform.messaging import headers as headers_mod
import importlib
import random


from contextlib import closing
from zmq import green as zmq
from volttron.platform.agent import json as jsonapi
from . import Core, RPC, PeerList, PubSub
from .subsystems.pubsub import encode_peer
from volttron.platform.messaging.headers import Headers

PEER = b'pubsub'
PUBLISH_ADDRESS = 'inproc://vip/compat/agent/publish'
SUBSCRIBE_ADDRESS = 'inproc://vip/compat/agent/subscribe'





DEFAULT_MESSAGE = 'Listener Message'
DEFAULT_AGENTID = "listener"
DEFAULT_HEARTBEAT_PERIOD = 5
DEFAULT_MONITORING_TIME = 5
oat_point = 'devices/Building/LAB/Device/OutsideAirTemperature'
all_topic = 'devices/Building/LAB/Device/all'
test = 'test/1'
test2 = 'test/2'


utils.setup_logging()  # setup logger for debugging
_log = logging.getLogger(__name__)

# PUSH_SOCKET = "ipc:///home/dell-hive01/.volttron/run/publish"
# SUB_SOCKET = "ipc:///home/dell-hive01/.volttron/run/subscribe"

# kwargs = {'subscribe_address': SUB_SOCKET, 'publish_address': PUSH_SOCKET}
# zmq_pub = ZMQ_PUB(**kwargs)

sbs = ServiceBusService(
                service_namespace='peahiveservicebus',
                shared_access_key_name='RootManageSharedAccessKey',
                shared_access_key_value='vOjEoWzURJCJ0bAgRTo69o4BmLy8GAje4CfdXkDiwzQ=')

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])

def deviceMonitorBehavior():

    agent_id = "devicediscoveryagent"

    os.system(  # ". env/bin/activate"
        "volttron-ctl stop --tag " + agent_id +
        ";volttron-ctl start --tag " + agent_id +
        ";volttron-ctl status")
    print "1"
    time.sleep(60)

    os.system(  # ". env/bin/activate"
        "volttron-ctl stop --tag " + agent_id +
        ";volttron-ctl status")


def HC(commsg):
    print commsg
    print "testhomescence"
    # TODO this is example how to write an app to control AC
    topic = '/ui/agent/lighttrigger/update/bemoss/999/HC001'
    message = json.dumps(commsg)
    zmq_pub.requestAgent(topic, message, "text/plain", "UI")
    print ("topic{}".format(topic))
    print ("message{}".format(message))

def pub(commsg):
    print commsg
    print "testhomescence"
    # TODO this is example how to write an app to control AC



    topic = str('/ui/agent/'+ str(commsg['device'][0:5])+'/update/bemoss/999/'+str(commsg['device']))
    print topic
    message = json.dumps(commsg)
    zmq_pub.requestAgent(topic, message, "text/plain", "UI")
    print ("topic{}".format(topic))
    print ("message{}".format(message))

# mac = hex(get_mac())[2:10]
#
# try:
#
#     gateway_mac = getHwAddr('eth0').replace(':', '')
#     gateway_id = 'hive' + getHwAddr('eth0').replace(':', '')
#     print(gateway_id)
#
# except:
#     print "no wlan0"
#     try:
#         gateway_mac = getHwAddr('wlan0').replace(':', '')
#         gateway_id = 'hive' + getHwAddr('wlan0').replace(':', '')
#         print(gateway_id)
#     except:
#         print "no eth0"
# topic = gateway_id

topic = 'hiveac7ba18fe1c0'
print topic

def pub_fake_data():
    ''' This method publishes fake data for use by the rest of the agent.
    The format mimics the format used by VOLTTRON drivers.

    This method can be removed if you have real data to work against.
    '''

    # Make some random readings
    oat_reading = random.uniform(30, 100)
    mixed_reading = oat_reading + random.uniform(-5, 5)
    damper_reading = random.uniform(0, 100)

    # Create a message for all points.
    all_message = [{'OutsideAirTemperature': oat_reading, 'MixedAirTemperature': mixed_reading,
                    'DamperSignal': damper_reading},
                   {'OutsideAirTemperature': {'units': 'F', 'tz': 'UTC', 'type': 'float'},
                    'MixedAirTemperature': {'units': 'F', 'tz': 'UTC', 'type': 'float'},
                    'DamperSignal': {'units': '%', 'tz': 'UTC', 'type': 'float'}
                    }]

    # Create messages for specific points
    oat_message = [oat_reading, {'units': 'F', 'tz': 'UTC', 'type': 'float'}]
    mixed_message = [mixed_reading, {'units': 'F', 'tz': 'UTC', 'type': 'float'}]
    damper_message = [damper_reading, {'units': '%', 'tz': 'UTC', 'type': 'float'}]

    # Create timestamp
    now = datetime.utcnow().isoformat(' ') + 'Z'
    headers = {
        headers_mod.DATE: now
    }

    # # Publish messages
    # self.vip.pubsub.publish(
    #     'pubsub', all_topic, headers, all_message)

    vip.pubsub.publish(
        'pubsub', 'test/2', headers, oat_message)

    # self.vip.pubsub.publish(
    #     'pubsub', mixed_point, headers, mixed_message)
    #
    # self.vip.pubsub.publish(
    #     'pubsub', damper_point, headers, damper_message)



while True:
    try:
        time.sleep(4)
        print "ttttttttttt"
        pub_fake_data()
	# print "mqtt server is waiting for message from Azure"
     #    msg = sbs.receive_subscription_message(topic, 'client1', peek_lock=False)
     #    commsg = eval(msg.body)
     #    print commsg
     #    print("message MQTT received")
     #    for k, v in commsg.items():
     #        if k == 'device':
    #
     #            if commsg['device'] == '--':
     #                commsg['device'] = '2HUEH0017881cab4b'
    #
     #            # pub(commsg)
    #
     #        elif k == 'scene':
     #            HC(commsg)
     #        else:
     #            print ""
     #    if (commsg['devicediscovery'] == True):
     #        deviceMonitorBehavior()
     #    else:
     #        print ""


    except Exception as er:
        print er



