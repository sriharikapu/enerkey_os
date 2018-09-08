# -*- coding: utf-8 -*-
from __future__ import absolute_import
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
import json
import socket
import psycopg2
import psycopg2.extras
import pyrebase
import time
from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests

utils.setup_logging()
_log = logging.getLogger(__name__)
__version__ = '3.2'
DEFAULT_HEARTBEAT_PERIOD = 20
DEFAULT_MONITORING_TIME = 20
DEFAULT_MESSAGE = 'HELLO'

apiKeyconfig = settings.CHANGE['change']['apiKeyLight']
authDomainconfig = settings.CHANGE['change']['authLight']
dataBaseconfig = settings.CHANGE['change']['databaseLight']
stoRageconfig = settings.CHANGE['change']['storageLight']

db_host = settings.DATABASES['default']['HOST']
db_port = settings.DATABASES['default']['PORT']
db_database = settings.DATABASES['default']['NAME']
db_user = settings.DATABASES['default']['USER']
db_password = settings.DATABASES['default']['PASSWORD']

try:
    config = {
      "apiKey": apiKeyconfig,
      "authDomain": authDomainconfig,
      "databaseURL": dataBaseconfig,
      "storageBucket": stoRageconfig,
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
except Exception as er:
    print er

# Step1: Agent Initialization
def ac_agent(config_path, **kwargs):
    config = utils.load_config(config_path)
    def get_config(name):
        try:
            kwargs.pop(name)
        except KeyError:
            return config.get(name, '')


    agent_id = get_config('agent_id')
    message = get_config('message')
    heartbeat_period = get_config('heartbeat_period')
    device_monitor_time = config.get('device_monitor_time', DEFAULT_MONITORING_TIME)
    building_name = get_config('building_name')
    zone_id = get_config('zone_id')
    model = get_config('model')
    device_type = get_config('type')
    api = get_config('api')
    address = get_config('ipaddress')
    _address = address.replace('http://', '')
    _address = address.replace('https://', '')
    identifiable = get_config('identifiable')



    # construct _topic_Agent_UI based on data obtained from DB
    _topic_Agent_UI_tail = building_name + '/' + str(zone_id) + '/' + agent_id
    topic_device_control = '/ui/agent/update/'+_topic_Agent_UI_tail
    print(topic_device_control)

    gateway_id = settings.gateway_id

    class DaikinAgent(Agent):
        """Listens to everything and publishes a heartbeat according to the
        heartbeat period specified in the settings module.
        """

        def __init__(self, config_path, **kwargs):
            super(DaikinAgent, self).__init__(**kwargs)
            self.config = utils.load_config(config_path)
            self._agent_id = agent_id
            self._message = message
            self._heartbeat_period = heartbeat_period
            self.model = model
            self.device_type = device_type
            self.apiLib = importlib.import_module("DeviceAPI.classAPI." + api)
            self.AC = self.apiLib.API(model=self.model, device_type=self.device_type, agent_id=self._agent_id
                                )

        @Core.receiver('onsetup')
        def onsetup(self, sender, **kwargs):
            # Demonstrate accessing a value from the config file
            _log.info(self.config.get('message', DEFAULT_MESSAGE))
            self.iotmodul = importlib.import_module("hive_lib.azure-iot-sdk-python.device.samples.iothub_client_sample")

        @Core.receiver('onstart')
        def onstart(self, sender, **kwargs):
            _log.debug("VERSION IS: {}".format(self.core.version()))
            self.gettoken()
            self.status_old = "none"
            self.status_old2 = "none"
            self.status_old3 = "none"
            self.status_old4 = "none"
            self.status_old5 = "none"

        @Core.periodic(device_monitor_time)
        def deviceMonitorBehavior(self):

            self.AC.getDeviceStatus()

            self.StatusPublish(self.AC.variables)

            # TODO update local postgres
            # self.publish_postgres()

            if(self.AC.variables['status'] != self.status_old or
                    self.AC.variables['current_temperature'] != self.status_old2 or
                    self.AC.variables['set_temperature'] != self.status_old3 or
                    self.AC.variables['set_humidity'] != self.status_old4 or
                    self.AC.variables['mode'] != self.status_old5):
                self.publish_firebase()
                self.publish_postgres()
                self.publish_azure_iot_hub(activity_type='devicemonitor', username=agent_id)
            else:
                pass

            self.status_old = self.AC.variables['status']
            self.status_old2 = self.AC.variables['current_temperature']
            self.status_old3 = self.AC.variables['set_temperature']
            self.status_old4 = self.AC.variables['set_humidity']
            self.status_old5 = self.AC.variables['mode']


        def publish_firebase(self):

            try:
                db.child(gateway_id).child('devices').child(agent_id).child("dt").set(datetime.now().replace(microsecond=0).isoformat())
                db.child(gateway_id).child('devices').child(agent_id).child("STATUS").set(self.AC.variables['status'])
                db.child(gateway_id).child('devices').child(agent_id).child("TEMPERATURE").set(self.AC.variables['current_temperature'])
                db.child(gateway_id).child('devices').child(agent_id).child("SET_TEMPERATURE").set(self.AC.variables['set_temperature'])
                db.child(gateway_id).child('devices').child(agent_id).child("SET_HUMIDITY").set(self.AC.variables['set_humidity'])
                db.child(gateway_id).child('devices').child(agent_id).child("MODE").set(self.AC.variables['mode'])
            except Exception as er:
                print er

        def publish_postgres(self):

            postgres_url = 'https://peahivemobilebackends.azurewebsites.net/api/v2.0/devices/'
            postgres_Authorization = 'Token '+self.api_token


            m = MultipartEncoder(
                fields={
                    "status": str(self.AC.variables['status']),
                    "device_id": str(self.AC.variables['agent_id']),
                    "device_type": "airconditioner",
                    "last_scanned_time": datetime.now().replace(microsecond=0).isoformat(),
                    # "current_temperature": str(self.AC.variables['current_temperature']),
                    # "set_temperature": str(self.AC.variables['set_temperature']),
                    # "mode": str(self.AC.variables['mode']),
                }
            )

            r = requests.put(postgres_url,
                             data=m,
                             headers={'Content-Type': m.content_type,
                                      "Authorization": postgres_Authorization,
                                      })
            print r.status_code

        def StatusPublish(self, commsg):
            # TODO this is example how to write an app to control AC
            topic = str('/agent/zmq/update/hive/999/' + str(self.AC.variables['agent_id']))
            message = json.dumps(commsg)
            print ("topic {}".format(topic))
            print ("message {}".format(message))

            self.vip.pubsub.publish(
                'pubsub', topic,
                {'Type': 'pub device status to ZMQ'}, message)

        def gettoken(self):
            conn = psycopg2.connect(host=db_host, port=db_port, database=db_database, user=db_user,
                                    password=db_password)
            self.conn = conn
            self.cur = self.conn.cursor()
            self.cur.execute("""SELECT * FROM token """)
            rows = self.cur.fetchall()
            for row in rows:
                if row[0] == gateway_id:
                    self.api_token =  row[1]
            self.conn.close()

        def publish_azure_iot_hub(self, activity_type, username):
            # TODO publish to Azure IoT Hub u
            '''
            here we need to use code from /home/kwarodom/workspace/hive_os/volttron/
            hive_lib/azure-iot-sdk-python/device/samples/simulateddevices.py
            def iothub_client_telemetry_sample_run():
            '''
            x = {}
            x["device_id"] = str(self.AC.variables['agent_id'])
            x["date_time"] = datetime.now().replace(microsecond=0).isoformat()
            x["device_status"] = str(self.AC.variables['status'])
            x["unixtime"] = int(time.time())
            x["current_temperature"] = str(self.AC.variables['current_temperature'])
            x["set_temperature"] = str(self.AC.variables['set_temperature'])
            x["set_humidity"] = str(self.AC.variables['set_humidity'])
            x["mode"] = str(self.AC.variables['mode'])
            x["activity_type"] = activity_type
            x["username"] = username
            x["device_name"] = 'MY DAIKIN'
            x["device_type"] = 'airconditioner'
            discovered_address = self.iotmodul.iothub_client_sample_run(bytearray(str(x), 'utf8'))

        @PubSub.subscribe('pubsub', topic_device_control)
        def match_device_control(self, peer, sender, bus, topic, headers, message):
            print "Topic: {topic}".format(topic=topic)
            print "Headers: {headers}".format(headers=headers)
            print "Message: {message}\n".format(message=message)
            message = json.loads(message)
            if 'status' in message:
                self.AC.variables['status'] = str(message['status'])
            if 'set_temperature' in message:
                self.AC.variables['set_temperature'] = str(message['set_temperature'])
            if 'set_humidity' in message:
                self.AC.variables['set_humidity'] = str(message['set_humidity'])
            if 'mode' in message:
                self.AC.variables['mode'] = str(message['mode'])
            self.AC.setDeviceStatus(message)

            time.sleep(2)
            self.AC.getDeviceStatus()
            if(self.AC.variables['status'] != self.status_old or
                    self.AC.variables['current_temperature'] != self.status_old2 or
                    self.AC.variables['set_temperature'] != self.status_old3 or
                    self.AC.variables['set_humidity'] != self.status_old4 or
                    self.AC.variables['mode'] != self.status_old5):
                self.publish_firebase()
                self.publish_postgres()
            else:
                time.sleep(1)
                self.AC.getDeviceStatus()
                if (self.AC.variables['status'] != self.status_old or
                        self.AC.variables['current_temperature'] != self.status_old2 or
                        self.AC.variables['set_temperature'] != self.status_old3 or
                        self.AC.variables['set_humidity'] != self.status_old4 or
                        self.AC.variables['mode'] != self.status_old5):
                    self.publish_firebase()
                    self.publish_postgres()
                else:
                    time.sleep(1)
                    self.AC.getDeviceStatus()
                    if (self.AC.variables['status'] != self.status_old or
                            self.AC.variables['current_temperature'] != self.status_old2 or
                            self.AC.variables['set_temperature'] != self.status_old3 or
                            self.AC.variables['set_humidity'] != self.status_old4 or
                            self.AC.variables['mode'] != self.status_old5):
                        self.publish_firebase()
                        self.publish_postgres()
                    else:
                        pass
            self.status_old = self.AC.variables['status']
            self.status_old2 = self.AC.variables['current_temperature']
            self.status_old3 = self.AC.variables['set_temperature']
            self.status_old4 = self.AC.variables['set_humidity']


    Agent.__name__ = '01DAI_ACAgent'
    return DaikinAgent(config_path, **kwargs)

def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(ac_agent, version=__version__)
    except Exception as e:
        _log.exception('unhandled exception')

if __name__ == '__main__':
    # Entry point for script

    sys.exit(main())
