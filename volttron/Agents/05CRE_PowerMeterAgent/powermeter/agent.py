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
import urllib3
import time
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import psycopg2
import psycopg2.extras

urllib3.disable_warnings()

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
def Powermetering_agent(config_path, **kwargs):
    config = utils.load_config(config_path)

    def get_config(name):
        try:
            kwargs.pop(name)
        except KeyError:
            return config.get(name, '')

    # List of all keywords for a Powermetering agent
    agentAPImapping = dict(status=[], brightness=[], color=[], saturation=[], power=[])
    log_variables = dict(status='text', brightness='double', hexcolor='text', power='double', offline_count='int')

    agent_id = get_config('agent_id')
    message = get_config('message')
    heartbeat_period = get_config('heartbeat_period')
    device_monitor_time = config.get('device_monitor_time', DEFAULT_MONITORING_TIME)
    building_name = get_config('building_name')
    zone_id = get_config('zone_id')
    model = get_config('model')
    if model == "Philips hue bridge":
        hue_username = get_config('username')
    else:
        hue_username = ''
    device_type = get_config('device_type')
    print device_type

    device = get_config('device')
    # bearer = get_config('bearer')
    url = get_config('url')
    api = get_config('api')
    address = get_config('ipaddress')
    device_id = get_config('device_id')
    identifiable = get_config('identifiable')

    _topic_Agent_UI_tail = building_name + '/' + str(zone_id) + '/' + agent_id
    topic_device_control = '/ui/agent/update/' + _topic_Agent_UI_tail
    print(topic_device_control)
    gateway_id = settings.gateway_id


    class PowermeteringAgent(Agent):
        """Listens to everything and publishes a heartbeat according to the
        heartbeat period specified in the settings module.
        """
        def __init__(self, config_path, **kwargs):
            super(PowermeteringAgent, self).__init__(**kwargs)
            self.config = utils.load_config(config_path)
            self._agent_id = agent_id
            self._message = message
            self._heartbeat_period = heartbeat_period
            self.model = model
            self.device_type = device_type
            self.url = url
            self.device_id = device_id
            self.apiLib = importlib.import_module("DeviceAPI.classAPI." + api)
            self.Powermeter = self.apiLib.API(model=self.model, type=self.device_type, agent_id=self._agent_id,
                                              url=self.url, device_id=self.device_id)
        @Core.receiver('onsetup')
        def onsetup(self, sender, **kwargs):
            # Demonstrate accessing a value from the config file
            _log.info(self.config.get('message', DEFAULT_MESSAGE))
            self.iotmodul = importlib.import_module("hive_lib.azure-iot-sdk-python.device.samples.iothub_client_sample")

        @Core.receiver('onstart')
        def onstart(self, sender, **kwargs):
            _log.debug("VERSION IS: {}".format(self.core.version()))
            self.gettoken()

        @Core.periodic(device_monitor_time)
        def deviceMonitorBehavior(self):
            self.Powermeter.getDeviceStatus()
            if ((self.Powermeter.variables['grid_voltage'] == 'None') or (
                    self.Powermeter.variables['grid_current'] == 'None') or
                    (self.Powermeter.variables['grid_activePower'] == 'None') or
                    (self.Powermeter.variables['grid_reactivePower'] == 'None')
            ):
                pass
            else:
                self.publish_firebase()
                # TODO remove comment before make a PR
                # self.publish_postgres()
                self.publish_azure_iot_hub()
                self.StatusPublish(self.Powermeter.variables)


        def StatusPublish(self, commsg):
            # TODO this is example how to write an app to control AC
            topic = str('/agent/zmq/update/hive/999/' + str(self.Powermeter.variables['agent_id']))
            message = json.dumps(commsg)
            print ("topic {}".format(topic))
            print ("message {}".format(message))

            self.StatusPublish(self.Powermeter.variables)

            self.publish_postgres()

            # update firebase
            self.publish_firebase()


        @Core.periodic(5)
        def deviceMonitorBehavior2(self):

            self.Powermeter.getDeviceStatus()
            self.vip.pubsub.publish(
                # 'pubsub', topic,
                {'Type': 'pub device status to ZMQ'}, message)

        def publish_firebase(self):
            try:
                db.child(gateway_id).child('devices').child(agent_id).child("dt").set(
                    datetime.now().replace(microsecond=0).isoformat())
                db.child(gateway_id).child('devices').child(agent_id).child("TransID(ID)").set(
                    self.Powermeter.variables['grid_transid'])
                db.child(gateway_id).child('devices').child(agent_id).child("Date(D)").set(
                    self.Powermeter.variables['grid_date'])
                db.child(gateway_id).child('devices').child(agent_id).child("Time(T)").set(
                    self.Powermeter.variables['grid_time'])
                db.child(gateway_id).child('devices').child(agent_id).child("UxTime(UT)").set(
                    self.Powermeter.variables['grid_uxtime'])
                db.child(gateway_id).child('devices').child(agent_id).child("DeviceID(DID)").set(
                    self.Powermeter.variables['grid_device_id'])
                db.child(gateway_id).child('devices').child(agent_id).child("Voltage(V)").set(
                    float(self.Powermeter.variables['grid_voltage']))
                db.child(gateway_id).child('devices').child(agent_id).child("Current(A)").set(
                    float(self.Powermeter.variables['grid_current']))
                db.child(gateway_id).child('devices').child(agent_id).child("EarthLeak(EL)").set(
                    self.Powermeter.variables['grid_earth_leak'])
                db.child(gateway_id).child('devices').child(agent_id).child("inverter_activePower").set(
                    float(self.Powermeter.variables['grid_activePower']))
                db.child(gateway_id).child('devices').child(agent_id).child("ReactivePower(Var)").set(
                    float(self.Powermeter.variables['grid_reactivePower']))
                db.child(gateway_id).child('devices').child(agent_id).child("Powerfactor").set(
                    float(self.Powermeter.variables['grid_powerfactor']))
                db.child(gateway_id).child('devices').child(agent_id).child("AccumulatedEnergy(Wh)").set(
                    float(self.Powermeter.variables['grid_accumulated_energy']))
                db.child(gateway_id).child('devices').child(agent_id).child("Kvarh").set(
                    float(self.Powermeter.variables['grid_kvarh']))
                db.child(gateway_id).child('devices').child(agent_id).child("device_type").set(
                    self.Powermeter.variables['device_type'])
                db.child(gateway_id).child('devices').child(agent_id).child("ActivePower(W)").set(
                    self.Powermeter.variables['grid_activePower'])
                print "---------------update firebase ok"
            except Exception as er:
                print er

        def publish_azure_iot_hub(self):
            # TODO publish to Azure IoT Hub u
            '''
            here we need to use code from /home/kwarodom/workspace/hive_os/volttron/
            hive_lib/azure-iot-sdk-python/device/samples/simulateddevices.py
            def iothub_client_telemetry_sample_run():
            '''
            print(self.Powermeter.variables)

            x = {}
            x["device_id"] = self.Powermeter.variables['agent_id']
            x["date_time"] = datetime.now().replace(microsecond=0).isoformat()
            x["unixtime"] = int(time.time())
            x["gridvoltage"] = self.Powermeter.variables['grid_voltage']
            x["gridcurrent"] = self.Powermeter.variables['grid_current']
            x["gridactivePower"] = self.Powermeter.variables['grid_activePower']
            x["gridreactivePower"] = self.Powermeter.variables['grid_reactivePower']
            x["activity_type"] = 'devicemonitor'
            x["username"] = 'arm'
            x["device_name"] = 'Etrix Power Meter'
            x["device_type"] = 'powermeter'
            discovered_address = self.iotmodul.iothub_client_sample_run(bytearray(str(x), 'utf8'))

        def publish_postgres(self):
            postgres_url = 'https://peahivemobilebackends.azurewebsites.net/api/v2.0/devices/'
            postgres_Authorization = 'Token '+self.api_token

            m = MultipartEncoder(
                fields={
                    "device_id": str(self.Powermeter.variables['agent_id']),
                    "device_type": "powermeter",
                    "last_scanned_time": datetime.now().replace(microsecond=0).isoformat(),
                    "grid_voltage": str(self.Powermeter.variables['grid_voltage']),
                    "grid_current": str(self.Powermeter.variables['grid_voltage']),
                    "grid_activepower": str(self.Powermeter.variables['grid_activePower']),
                    "grid_reactivepower": str(self.Powermeter.variables['grid_reactivePower']),
                }
            )
            r = requests.put(postgres_url,
                             data=m,
                             headers={'Content-Type': m.content_type,
                                      "Authorization": postgres_Authorization,
                                      })
            print r.status_code

        def gettoken(self):
            conn = psycopg2.connect(host=db_host, port=db_port, database=db_database, user=db_user,
                                    password=db_password)
            self.conn = conn
            self.cur = self.conn.cursor()
            self.cur.execute("""SELECT * FROM token """)
            rows = self.cur.fetchall()
            for row in rows:
                if row[0] == gateway_id:
                    self.api_token = row[1]
            self.conn.close()

        def StatusPublish(self, commsg):
            # TODO this is example how to write an app to control AC
            topic = str('/agent/zmq/update/hive/999/' + str(self.Powermeter.variables['agent_id']))
            message = json.dumps(commsg)
            print ("topic {}".format(topic))
            print ("message {}".format(message))
            self.vip.pubsub.publish(
                'pubsub', topic,
                {'Type': 'pub device status to ZMQ'}, message)

        @PubSub.subscribe('pubsub', topic_device_control)
        def match_device_control(self, peer, sender, bus, topic, headers, message):
            print "Topic: {topic}".format(topic=topic)
            print "Headers: {headers}".format(headers=headers)
            print "Message: {message}\n".format(message=message)
            self.Powermeter.setDeviceStatus(json.loads(message))

    Agent.__name__ = 'PowermeteringAgent'
    return PowermeteringAgent(config_path, **kwargs)


def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(Powermetering_agent, version=__version__)
    except Exception as e:
        _log.exception('unhandled exception')


if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
