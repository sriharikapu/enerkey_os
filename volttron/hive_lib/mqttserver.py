# -*- coding: utf-8 -*-
#UDP server responds to broadcast packets
#you can have only one instance of this running as a BEMOSS core!!
import os
import sys
os.chdir(os.path.expanduser("~/workspace/hive_os/"))  # = ~/workspace/bemoss_os
current_working_directory = os.getcwd()
sys.path.append(current_working_directory)
from azure.servicebus import ServiceBusService, Message, Topic, Rule, DEFAULT_RULE_NAME
from zmqhelper.ZMQHelper.zmq_pub import ZMQ_PUB
import requests
import json
import time
import logging
import os
from volttron.platform.agent import utils, matching
from uuid import getnode as get_mac
import fcntl, socket, struct

utils.setup_logging()  # setup logger for debugging
_log = logging.getLogger(__name__)

PUSH_SOCKET = "ipc:///home/dell-hive01/.volttron/run/publish"
SUB_SOCKET = "ipc:///home/dell-hive01/.volttron/run/subscribe"

kwargs = {'subscribe_address': SUB_SOCKET, 'publish_address': PUSH_SOCKET}
zmq_pub = ZMQ_PUB(**kwargs)

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

def hue(commsg):
    # TODO this is example how to write an app to control Lighting
    topic = "/ui/agent/ac/update/bemoss/999/2HUE0017881cab4b"
    # now = datetime.utcnow().isoformat(' ') + 'Z'
    # headers = {
    #     headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
    #     headers_mod.DATE: now,
    # }
    message = json.dumps(commsg)
    print type(message)

    zmq_pub.requestAgent(topic, message, "text/plain", "UI")
    print ("topic{}".format(topic))
    print ("message{}".format(message))

def kitchen(commsg):
    # TODO this is example how to write an app to control Lighting
    topic = "/ui/agent/light/update/bemoss/999/1KR221445K1200138"
    # now = datetime.utcnow().isoformat(' ') + 'Z'
    # headers = {
    #     headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
    #     headers_mod.DATE: now,
    # }
    message = json.dumps(commsg)
    print type(message)

    zmq_pub.requestAgent(topic, message, "text/plain", "UI")
    print ("topic{}".format(topic))
    print ("message{}".format(message))

def yale(commsg):
    # TODO this is example how to write an app to control Lighting
    topic = "/ui/agent/tv/update/bemoss/999/18DOR06"
    # now = datetime.utcnow().isoformat(' ') + 'Z'
    # headers = {
    #     headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
    #     headers_mod.DATE: now,
    # }
    message = json.dumps(commsg)
    print type(message)

    zmq_pub.requestAgent(topic, message, "text/plain", "UI")
    print ("topic{}".format(topic))
    print ("message{}".format(message))

def living(commsg):
    # TODO this is example how to write an app to control Lighting
    topic = "/ui/agent/light/update/bemoss/999/1LR221445K1200138"
    # now = datetime.utcnow().isoformat(' ') + 'Z'
    # headers = {
    #     headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
    #     headers_mod.DATE: now,
    # }
    message = json.dumps(commsg)
    print type(message)

    zmq_pub.requestAgent(topic, message, "text/plain", "UI")
    print ("topic{}".format(topic))
    print ("message{}".format(message))

def saijo1(commsg):
    # TODO this is example how to write an app to control Lighting
    topic = "/ui/agent/airconditioner/update/bemoss/999/1TH20000000000001"
    # now = datetime.utcnow().isoformat(' ') + 'Z'
    # headers = {
    #     headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
    #     headers_mod.DATE: now,
    # }
    message = json.dumps(commsg)
    print type(message)

    zmq_pub.requestAgent(topic, message, "text/plain", "UI")
    print ("topic{}".format(topic))
    print ("message{}".format(message))

def saijo2(commsg):
    # TODO this is example how to write an app to control Lighting
    topic = "/ui/agent/airconditioner/update/bemoss/999/1TH20000000000002"
    # now = datetime.utcnow().isoformat(' ') + 'Z'
    # headers = {
    #     headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
    #     headers_mod.DATE: now,
    # }
    message = json.dumps(commsg)
    print type(message)

    zmq_pub.requestAgent(topic, message, "text/plain", "UI")
    print ("topic{}".format(topic))
    print ("message{}".format(message))

def saijo3(commsg):
    # TODO this is example how to write an app to control Lighting
    topic = "/ui/agent/airconditioner/update/bemoss/999/1TH20000000000003"
    # now = datetime.utcnow().isoformat(' ') + 'Z'
    # headers = {
    #     headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
    #     headers_mod.DATE: now,
    # }
    message = json.dumps(commsg)
    print type(message)

    zmq_pub.requestAgent(topic, message, "text/plain", "UI")
    print ("topic{}".format(topic))
    print ("message{}".format(message))


def wemo(commsg):
    # TODO this is example how to write an app to control Lighting
    topic = '/ui/agent/plugload/update/bemoss/999/3WSP231613K1200162'
    # now = datetime.utcnow().isoformat(' ') + 'Z'
    # headers = {
    #     headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
    #     headers_mod.DATE: now,
    # }
    message = json.dumps(commsg)
    zmq_pub.requestAgent(topic, message, "text/plain", "UI")
    print ("topic{}".format(topic))
    print ("message{}".format(message))


def daikin(commsg):
    # TODO this is example how to write an app to control Lighting


    topic = '/ui/agent/AC/update/bemoss/999/1ACD1200138'
    # topic = '/ui/agent/AC/update/bemoss/999/ACD1200138'
    # {"status": "OFF"}
    # now = datetime.utcnow().isoformat(' ') + 'Z'
    # headers = {
    #     headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
    #     headers_mod.DATE: now,
    # }
    message = json.dumps(commsg)
    zmq_pub.requestAgent(topic, message, "text/plain", "UI")
    print ("topic{}".format(topic))
    print ("message{}".format(message))


def fan(commsg):
    # TODO this is example how to write an app to control Lighting
    topic = '/ui/agent/relaysw/update/bemoss/999/1FN221445K1200138'
    # {"status": "OFF"}
    # now = datetime.utcnow().isoformat(' ') + 'Z'
    # headers = {
    #     headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
    #     headers_mod.DATE: now,
    # }
    message = json.dumps(commsg)
    zmq_pub.requestAgent(topic, message, "text/plain", "UI")
    print ("topic{}".format(topic))
    print ("message{}".format(message))

def lg(commsg):
    # TODO this is example how to write an app to control Lighting
    topic = '/ui/agent/tv/update/bemoss/999/1LG221445K1200137'
    # {"status": "OFF"}
    # now = datetime.utcnow().isoformat(' ') + 'Z'
    # headers = {
    #     headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
    #     headers_mod.DATE: now,
    # }
    message = json.dumps(commsg)
    zmq_pub.requestAgent(topic, message, "text/plain", "UI")
    print ("topic{}".format(topic))
    print ("message{}".format(message))


def somfy(commsg):
    # TODO this is example how to write an app to control Lighting
    topic = '/ui/agent/tv/update/bemoss/999/3WSP221445K1200328'
    # {"status": "OFF"}
    # now = datetime.utcnow().isoformat(' ') + 'Z'
    # headers = {
    #     headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
    #     headers_mod.DATE: now,
    # }
    message = json.dumps(commsg)
    zmq_pub.requestAgent(topic, message, "text/plain", "UI")
    print ("topic{}".format(topic))
    print ("message{}".format(message))

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

while True:
    try:
	print "mqtt server is waiting for message from Azure"
        msg = sbs.receive_subscription_message(topic, 'client1', peek_lock=False)
        commsg = eval(msg.body)
        print commsg
        print("message MQTT received")
        for k, v in commsg.items():
            if k == 'device':

                if commsg['device'] == '--':
                    commsg['device'] = '2HUEH0017881cab4b'

                pub(commsg)

            elif k == 'scene':
                HC(commsg)
            else:
                print ""
        if (commsg['devicediscovery'] == True):
            deviceMonitorBehavior()
        else:
            print ""


    except Exception as er:
        print er



