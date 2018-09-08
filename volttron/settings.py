# -*- coding: utf-8 -*-
# settings file for BEMOSS project.

import os
import fcntl, socket, struct

def getHwAddr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    info = fcntl.ioctl(s.fileno(), 0x8927,  struct.pack('256s', ifname[:15]))
    return ':'.join(['%02x' % ord(char) for char in info[18:24]])

DEBUG = True
TEMPLATE_DEBUG = DEBUG

PROJECT_DIR = os.path.dirname(__file__)
Agents_DIR = os.path.join(PROJECT_DIR, 'Agents/')
Agents_Launch_DIR = os.path.join(PROJECT_DIR, 'Agents/LaunchFiles/')
Applications_DIR = os.path.join(PROJECT_DIR, 'Applications/')
Applications_Launch_DIR = os.path.join(PROJECT_DIR, 'Applications/launch/')
Loaded_Agents_DIR = os.path.expanduser("~/.volttron/agents/")
Autostart_Agents_DIR = os.path.expanduser("~/.config/volttron/lite/autostart/")
Communications_DIR = os.path.join(PROJECT_DIR, 'bemoss_lib/communication/')
Custom_eggs_DIR = os.path.join(PROJECT_DIR, 'bemoss_lib/custom-eggs/')

try:
    gateway_mac = getHwAddr('wlan0').replace(':','')
    gateway_id = 'hive'+ getHwAddr('wlan0').replace(':','')
    print "gatewayid"
    print(gateway_id)
    print "gatewayid"
except:
    print "no wlan0"
    try:
        gateway_mac = getHwAddr('eth0').replace(':','')
        gateway_id = 'hive'+ getHwAddr('eth0').replace(':','')
        print "gatewayid"
        print(gateway_id)
    except:
        print "no eth0"

# TODO change gateway_id
gateway_id='hivecdf12345'
print('sending data to gateway: {}'.format(gateway_id))

PLATFORM = {
    'node': {
        'name': 'BEMOSS core',
        'type': 'core',
        'model': 'Odroid3',
        'building_name': 'bemoss',
        'node_monitor_time': 60,
        'node_offline_timeout': 0,
        'main_core': 'BEMOSS core'
    }
}

DEVICES = {
    'device_monitor_time': 20,
    'max_monitor_time': 1800,
    'cassandra_update_time': 10
}

CHANGE = {
    'change':{
        'apiKeyLight':'AIzaSyD4QZ7ko7uXpNK-VBF3Qthhm3Ypzi_bxgQ',
        'authLight':'hive-rt-mobile-backend.firebaseapp.com',
        'databaseLight': 'https://hive-rt-mobile-backend.firebaseio.com',
        'storageLight':'bucket.appspot.com'
    }
}

POSTGRES = {
    'postgres':{
        'url':'https://peahivemobilebackends.azurewebsites.net/api/v2.0/devices/',
        'Authorization':'Token 420afbbf66341d0c6167698087235d12df041836',
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'hiveosdb',                      # Or path to database file if using sqlite3.
        'USER': 'admin',                      # Not used with sqlite3.
        'PASSWORD': 'admin',                  # Not used with sqlite3.
        'HOST': 'localhost',
        'PORT': '5432',                    # Set to empty string for default. Not used with sqlite3.
        'firebase': True,
        'azureiot': False,
        'TABLE_dashboard_device_info': 'dashboard_device_info',
        'TABLE_dashboard_current_status': 'dashboard_current_status',
        'TABLE_building_zone': 'building_zone',
        'TABLE_global_zone_setting': 'global_zone_setting',
        'TABLE_device_info': 'device_info',
        'TABLE_device_model': 'device_model',
        'TABLE_dashboard_building_zones': 'building_zone',
        'TABLE_holiday': 'holiday',
        'TABLE_application_running': 'application_running',
        'TABLE_application_registered': 'application_registered',
        'TABLE_plugload': 'tplink',
        'TABLE_thermostat': 'thermostat',
        'TABLE_lighting': 'ac',
        'TABLE_device_metadata': 'device_metadata',
        'TABLE_vav': 'vav',
        'TABLE_rtu': 'rtu',
        'TABLE_supported_devices': 'supported_devices',
        'TABLE_node_info': 'node_info',
        'TABLE_node_device': 'node_device',
        'TABLE_notification_event': 'notification_event',
        'TABLE_bemoss_notify': 'bemoss_notify',
        'TABLE_active_alert': 'active_alert',
        'TABLE_device_type': 'device_type',
        'TABLE_alerts_notificationchanneladdress': 'alerts_notificationchanneladdress',
        'TABLE_temp_time_counter': 'temp_time_counter',
        'TABLE_temp_failure_time': 'temp_failure_time',
        'TABLE_priority': 'priority',
        'TABLE_seen_notifications_counter': 'seen_notifications_counter',
        'TABLE_powermeter': 'power_meter',
        'TABLE_AC': 'ac',
        'TABLE_Refrigerator': 'Refrigerator',
        'TABLE_MultiSensor': 'MultiSensor',
        'TABLE_LGTV': 'LGTV',
        'TABLE_Inverter': 'Inverter',
        'TABLE_Fan': 'Fan',
        'TABLE_Weather': 'Weather',
        'TABLE_Sonos': 'Sonos',
        'TABLE_NETPIESensor': 'NETPIE',
        'TABLE_daily_consumption': 'daily_consumption',
        'TABLE_PVInverter': 'PVInverter',
        'TABLE_monthly_consumption': 'monthly_consumption',
        'TABLE_annual_consumption': 'annual_consumption',
        'TABLE_DCRelay': 'DCRelay',
        'TABLE_ac_daily_consumption': 'ac_daily_consumption',
        'TABLE_ac_monthly_consumption': 'ac_monthly_consumption',
        'TABLE_lighting_daily_consumption': 'lighting_daily_consumption',
        'TABLE_lighting_monthly_consumption': 'lighting_monthly_consumption',
        'TABLE_ev_daily_consumption': 'ev_daily_consumption',
        'TABLE_ev_monthly_consumption': 'ev_monthly_consumption',
        'TABLE_plugload_daily_consumption': 'plugload_daily_consumption',
        'TABLE_plugload_monthly_consumption': 'plugload_monthly_consumption',
        'TABLE_cumulative_energy': 'cumulative_energy',
        'TABLE_pvrealtime_hourly': 'pvrealtime_hourly',
        'TABLE_CreativePowerMeter': 'CreativePowerMeter',
        'TABLE_ACDaikin': 'ACDaikin',
        'TABLE_Netatmo': 'Netatmo',
        'TABLE_RelaySW': 'RelaySW',
        'TABLE_OpenClose': 'OpenClose',
        'TABLE_Curtain': 'Curtain',
        'TABLE_Doorlock': 'Doorlock',
        'TABLE_Tplink': 'Tplink',
        'TABLE_Smartmeter': 'Smartmeter',
    }
}

NOTIFICATION = {
    'heartbeat': 24*60,  # heartbeat period to resend a message
    'heartbeat_device_tampering': 130,  # heartbeat period to resend a message
    'email': {
        'fromaddr': 'Your Email',
        'recipients': ['Your recipient 1', 'Your recipient 2'],
        'username': 'Your Email',
        'password': 'Your Password',
        'subject' : 'Message from',
        'mailServer': 'smtp.gmail.com:587'
    },
    'tplink':{
        'status': "ON",
        'power': 200
    },
    'thermostat':{
        'too_hot': 90,
        'too_cold': 60
    },
    'ac':{
        'too_dark': 10  # % of brightness
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Asia/Bangkok'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'


FIND_DEVICE_SETTINGS = {
    'findWiFi': True,
    'findWiFiHue': True,
    'findWiFiWeMo': True,
    'findBACnet': True,
    'findModbus': True,
	
}
# TODO change servicebus
AZURE = {
    'servicebus': {
        'topic': 'hivecdf12345',
        'service_namespace': 'peahiveservicebusv2',
        'shared_access_key_name': 'RootManageSharedAccessKey',
        'shared_access_key_value': 'F6hM22kIHgfzKmt2GF0NtGlrVZtapYHOG3gMb7doaM4=',
        'CONNECTION_STRING' : 'HostName=peahiveiotv2.azure-devices.net;DeviceId=hivecdf12345;SharedAccessKey=u/QZgiQ+isxKXTkkn4Hc3Oys6Ski1NjT5bTRkGTHvyw='
    }
}
