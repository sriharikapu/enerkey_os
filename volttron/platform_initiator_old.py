# -*- coding: utf-8 -*-
import os
import sys
import json
os.chdir(os.path.expanduser("~/workspace/hive_os/"))  # = ~/workspace/bemoss_os
# os.system("service postgresql restart")
current_working_directory = os.getcwd()
sys.path.append(current_working_directory)
import settings
import psycopg2
import datetime
# CONFIGURATION ---------------------------------------------------------------------------------------------
#@params agent
agent_id = 'PlatformInitiator'

# @params DB interfaces
db_database = settings.DATABASES['default']['NAME']
db_host = settings.DATABASES['default']['HOST']
db_port = settings.DATABASES['default']['PORT']
db_user = settings.DATABASES['default']['USER']
db_password = settings.DATABASES['default']['PASSWORD']
db_table_building_zone = settings.DATABASES['default']['TABLE_building_zone']
db_table_global_zone_setting = settings.DATABASES['default']['TABLE_global_zone_setting']
db_table_holiday = settings.DATABASES['default']['TABLE_holiday']
db_table_device_info = settings.DATABASES['default']['TABLE_device_info']
db_table_device_model = settings.DATABASES['default']['TABLE_device_model']
db_table_application_running = settings.DATABASES['default']['TABLE_application_running']
db_table_application_registered = settings.DATABASES['default']['TABLE_application_registered']
db_table_plugload = settings.DATABASES['default']['TABLE_plugload']
db_table_thermostat = settings.DATABASES['default']['TABLE_thermostat']
db_table_lighting = settings.DATABASES['default']['TABLE_lighting']
db_table_device_metadata = settings.DATABASES['default']['TABLE_device_metadata']
db_table_vav = settings.DATABASES['default']['TABLE_vav']
db_table_rtu = settings.DATABASES['default']['TABLE_rtu']
db_table_alerts_notificationchanneladdress = settings.DATABASES['default'][
        'TABLE_alerts_notificationchanneladdress']
db_table_active_alert = settings.DATABASES['default']['TABLE_active_alert']
db_table_temp_time_counter = settings.DATABASES['default']['TABLE_temp_time_counter']
db_table_seen_notifications_counter = settings.DATABASES['default']['TABLE_seen_notifications_counter']
db_table_bemoss_notify = settings.DATABASES['default']['TABLE_bemoss_notify']
db_table_node_info = settings.DATABASES['default']['TABLE_node_info']
db_table_daily_consumption = settings.DATABASES['default']['TABLE_daily_consumption']
db_table_monthly_consumption = settings.DATABASES['default']['TABLE_monthly_consumption']

PROJECT_DIR = settings.PROJECT_DIR
Agents_Launch_DIR = settings.Agents_Launch_DIR
Loaded_Agents_DIR = settings.Loaded_Agents_DIR

# Autostart_Agents_DIR = settings.Autostart_Agents_DIR
Applications_Launch_DIR = settings.Applications_Launch_DIR
#----------------------------------------------------------------------------------------------------------
os.system("clear")
#1. Connect to bemossdb database
conn = psycopg2.connect(host=db_host, port=db_port, database=db_database,
                            user=db_user, password=db_password)
cur = conn.cursor()  # open a cursor to perform database operations
print "{} >> Done 1: connect to database name {}".format(agent_id, db_database)


# #8. create tables
cur.execute("select * from information_schema.tables where table_name=%s", ('monthly_consumption',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    cur.execute("DROP TABLE monthly_consumption")
    conn.commit()
else:
    pass

cur.execute('''CREATE TABLE monthly_consumption
       (ID SERIAL   PRIMARY KEY   NOT NULL,
       DATE   DATE   NOT NULL,
       GRIDIMPORTENERGY     FLOAT,
       GRIDEXPORTENERGY     FLOAT,
       SOLARENERGY     FLOAT,
       LOADENERGY     FLOAT,
       GRIDIMPORTBILL     FLOAT,
       GRIDEXPORTBILL     FLOAT,
       SOLARBILL     FLOAT,
       LOADBILL     FLOAT);''')
print "Table monthly_consumption created successfully"
conn.commit()

cur.execute("select * from information_schema.tables where table_name=%s", ('annual_consumption',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    cur.execute("DROP TABLE annual_consumption")
    conn.commit()
else:
    pass

cur.execute('''CREATE TABLE annual_consumption
       (ID SERIAL   PRIMARY KEY   NOT NULL,
       DATE   DATE   NOT NULL,
       GRIDIMPORTENERGY     FLOAT,
       GRIDEXPORTENERGY     FLOAT,
       SOLARENERGY     FLOAT,
       LOADENERGY     FLOAT,
       GRIDIMPORTBILL     FLOAT,
       GRIDEXPORTBILL     FLOAT,
       SOLARBILL     FLOAT,
       LOADBILL     FLOAT);''')
print "Table annual_consumption created successfully"
conn.commit()

cur.execute("select * from information_schema.tables where table_name=%s", ('ac_daily_consumption',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    cur.execute("DROP TABLE ac_daily_consumption")
    conn.commit()
else:
    pass

cur.execute('''CREATE TABLE ac_daily_consumption
       (ID SERIAL   PRIMARY KEY   NOT NULL,
       DATE   DATE   NOT NULL,
       DEVICE_ID     TEXT ,
       DEVICE_ENERGY     FLOAT,
       DEVICE_ENERGY_FROM_GRID     FLOAT,
       DEVICE_BILL     FLOAT,
       DEVICE_TOTAL_BILL     FLOAT);''')
print "Table ac_daily_consumption created successfully"
conn.commit()

cur.execute("select * from information_schema.tables where table_name=%s", ('ac_monthly_consumption',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    cur.execute("DROP TABLE ac_monthly_consumption")
    conn.commit()
else:
    pass

cur.execute('''CREATE TABLE ac_monthly_consumption
       (ID SERIAL   PRIMARY KEY   NOT NULL,
       DATE   DATE   NOT NULL,
       DEVICE_ID     TEXT ,
       DEVICE_ENERGY     FLOAT,
       DEVICE_ENERGY_FROM_GRID     FLOAT,
       DEVICE_BILL     FLOAT,
       DEVICE_TOTAL_BILL     FLOAT);''')
print "Table ac_monthly_consumption created successfully"
conn.commit()

cur.execute("select * from information_schema.tables where table_name=%s", ('lighting_daily_consumption',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    cur.execute("DROP TABLE lighting_daily_consumption")
    conn.commit()
else:
    pass

cur.execute('''CREATE TABLE lighting_daily_consumption
       (ID SERIAL   PRIMARY KEY   NOT NULL,
       DATE   DATE   NOT NULL,
       DEVICE_ID     TEXT ,
       DEVICE_ENERGY     FLOAT,
       DEVICE_ENERGY_FROM_GRID     FLOAT,
       DEVICE_BILL     FLOAT,
       DEVICE_TOTAL_BILL     FLOAT);''')
print "Table lighting_daily_consumption created successfully"
conn.commit()

cur.execute("select * from information_schema.tables where table_name=%s", ('lighting_monthly_consumption',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    cur.execute("DROP TABLE lighting_monthly_consumption")
    conn.commit()
else:
    pass

cur.execute('''CREATE TABLE lighting_monthly_consumption
       (ID SERIAL   PRIMARY KEY   NOT NULL,
       DATE   DATE   NOT NULL,
       DEVICE_ID     TEXT ,
       DEVICE_ENERGY     FLOAT,
       DEVICE_ENERGY_FROM_GRID     FLOAT,
       DEVICE_BILL     FLOAT,
       DEVICE_TOTAL_BILL     FLOAT);''')
print "Table lighting_monthly_consumption created successfully"
conn.commit()

cur.execute("select * from information_schema.tables where table_name=%s", ('ev_daily_consumption',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    cur.execute("DROP TABLE ev_daily_consumption")
    conn.commit()
else:
    pass

cur.execute('''CREATE TABLE ev_daily_consumption
       (ID SERIAL   PRIMARY KEY   NOT NULL,
       DATE   DATE   NOT NULL,
       DEVICE_ID     TEXT ,
       DEVICE_ENERGY     FLOAT,
       DEVICE_ENERGY_FROM_GRID     FLOAT,
       DEVICE_BILL     FLOAT,
       DEVICE_TOTAL_BILL     FLOAT);''')
print "Table ev_daily_consumption created successfully"
conn.commit()

cur.execute("select * from information_schema.tables where table_name=%s", ('ev_monthly_consumption',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    cur.execute("DROP TABLE ev_monthly_consumption")
    conn.commit()
else:
    pass

cur.execute('''CREATE TABLE ev_monthly_consumption
       (ID SERIAL   PRIMARY KEY   NOT NULL,
       DATE   DATE   NOT NULL,
       DEVICE_ID     TEXT ,
       DEVICE_ENERGY     FLOAT,
       DEVICE_ENERGY_FROM_GRID     FLOAT,
       DEVICE_BILL     FLOAT,
       DEVICE_TOTAL_BILL     FLOAT);''')
print "Table ev_monthly_consumption created successfully"
conn.commit()

cur.execute("select * from information_schema.tables where table_name=%s", ('plugload_daily_consumption',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    cur.execute("DROP TABLE plugload_daily_consumption")
    conn.commit()
else:
    pass

cur.execute('''CREATE TABLE plugload_daily_consumption
       (ID SERIAL   PRIMARY KEY   NOT NULL,
       DATE   DATE   NOT NULL,
       DEVICE_ID     TEXT ,
       DEVICE_ENERGY     FLOAT,
       DEVICE_ENERGY_FROM_GRID     FLOAT,
       DEVICE_BILL     FLOAT,
       DEVICE_TOTAL_BILL     FLOAT);''')
print "Table plugload_daily_consumption created successfully"
conn.commit()

cur.execute("select * from information_schema.tables where table_name=%s", ('plugload_monthly_consumption',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    cur.execute("DROP TABLE plugload_monthly_consumption")
    conn.commit()
else:
    pass

cur.execute('''CREATE TABLE plugload_monthly_consumption
       (ID SERIAL   PRIMARY KEY   NOT NULL,
       DATE   DATE   NOT NULL,
       DEVICE_ID     TEXT ,
       DEVICE_ENERGY     FLOAT,
       DEVICE_ENERGY_FROM_GRID     FLOAT,
       DEVICE_BILL     FLOAT,
       DEVICE_TOTAL_BILL     FLOAT);''')
print "Table plugload_monthly_consumption created successfully"
conn.commit()

cur.execute("select * from information_schema.tables where table_name=%s", ('application_running',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    cur.execute("DROP TABLE application_running")
    conn.commit()
else:
    pass

cur.execute('''CREATE TABLE application_running
       (APPLICATION_ID SERIAL   PRIMARY KEY   NOT NULL,
       APP_AGENT_ID   VARCHAR(50)   NOT NULL,
       START_TIME     TIMESTAMP,
       STATUS        VARCHAR(10),
       APP_SETTING   VARCHAR(200));''')
print "Table application_running created successfully"
conn.commit()

cur.execute("select * from information_schema.tables where table_name=%s", ('application_registered',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    cur.execute("DROP TABLE application_registered")
    conn.commit()
else:
    pass

cur.execute('''CREATE TABLE application_registered
       (APPLICATION_ID SERIAL   PRIMARY KEY   NOT NULL,
       APP_NAME VARCHAR (30) NOT NULL,
       EXECUTABLE VARCHAR (35) NOT NULL,
       AUTH_TOKEN VARCHAR (20) NOT NULL,
       APP_USER TEXT,
       DESCRIPTION  VARCHAR (200) NOT NULL,
       REGISTERED_TIME  TIMESTAMP  NOT NULL,
       LAST_UPDATED_TIME  TIMESTAMP NOT NULL);''')
print "Table application_registered created successfully"
conn.commit()

cur.execute("select * from information_schema.tables where table_name=%s", ('passwords_manager',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    print "table already exits. Clearing"
    cur.execute("DELETE FROM passwords_manager")
    conn.commit()

cur.execute("select * from information_schema.tables where table_name=%s", ('supported_devices',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    print "table already exits. Dropping"
    cur.execute("DELETE FROM supported_devices")
    conn.commit()
else:
    cur.execute('''CREATE TABLE supported_devices
           (DEVICE_MODEL VARCHAR(30) PRIMARY KEY   NOT NULL,
           VENDOR_NAME  VARCHAR(50),
           COMMUNICATION VARCHAR(10),
           DEVICE_TYPE VARCHAR(20),
           DISCOVERY_TYPE VARCHAR(20),
           DEVICE_MODEL_ID  VARCHAR(5),
           API_NAME VARCHAR(50),
           IDENTIFIABLE BOOLEAN);''')
    print "Table supported_devices created successfully"
    conn.commit()

cur.execute("select * from information_schema.tables where table_name=%s", ('node_device',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    cur.execute("DELETE FROM node_device")
    conn.commit()
else:
    pass

    cur.execute('''CREATE TABLE node_device
           (TRANS_NO SERIAL PRIMARY KEY   NOT NULL,
           DEVICE_ID  VARCHAR(50),
           PREVIOUS_ZONE_ID INT,
           CURRENT_ZONE_ID INT,
           DATE_MOVE TIMESTAMP);''')
    print "Table node_device created successfully"
conn.commit()

cur.execute("select * from information_schema.tables where table_name=%s", ('notification_event',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    cur.execute("DELETE FROM notification_event")
    conn.commit()
else:
    pass
    cur.execute('''CREATE TABLE notification_event
           (EVENT_ID SERIAL PRIMARY KEY   NOT NULL,
           EVENT_NAME  VARCHAR(30) NOT NULL,
           NOTIFY_DEVICE_ID  VARCHAR(50) NOT NULL,
           TRIGGERED_PARAMETER VARCHAR(20) NOT NULL,
           COMPARATOR VARCHAR(10) NOT NULL,
           THRESHOLD VARCHAR(10) NOT NULL,
           NOTIFY_CHANNEL VARCHAR(20) NOT NULL,
           NOTIFY_ADDRESS VARCHAR(30),
           NOTIFY_HEARTBEAT INT,
           DATE_ADDED TIMESTAMP,
           LAST_UPDATED TIMESTAMP);''')
    print "Table notification_event created successfully"
conn.commit()


# cur.execute("INSERT INTO supported_devices VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
#             ("CT30 V1.94","RadioThermostat","WiFi","thermostat","thermostat","1TH","classAPI_RadioThermostat",True,False,4,4,False))
# cur.execute("INSERT INTO supported_devices VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
#             ("CT50 V1.94","RadioThermostat","WiFi","thermostat","thermostat","1TH","classAPI_RadioThermostat",True,False,4,4,False))
# cur.execute("INSERT INTO supported_devices VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
#             ("Socket","Belkin International Inc.","WiFi","plugload","WeMo","3WSP","classAPI_WeMo",True,False,4,4,True))
# cur.execute("INSERT INTO supported_devices VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
#             ("LightSwitch","Belkin International Inc.","WiFi","ac","WeMo","2WL","classAPI_WeMo",True,False,4,4,True))
# cur.execute("INSERT INTO supported_devices VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
#             ("Philips hue bridge","Royal Philips Electronics","WiFi","ac","Philips","2HUE","classAPI_PhilipsHue",True,False,4,4,True))
# cur.execute("INSERT INTO supported_devices VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
#             ("LMRC-212","WattStopper","BACnet","ac","WattStopper","2WSL","classAPI_BACnet_WattStopper",True,False,4,4,True))
# cur.execute("INSERT INTO supported_devices VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
#             ("LMPL-201","WattStopper","BACnet","plugload","WattStopper","3WP","classAPI_BACnet_WattStopper",True,False,4,4,True))
# cur.execute("INSERT INTO supported_devices VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
#             ("VC1000","Prolon","Modbus","vav","Prolon_VAV","1VAV","classAPI_vav_rtu",False,False,4,4,True))
# cur.execute("INSERT INTO supported_devices VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
#             ("M1000","Prolon","Modbus","rtu","Prolon_RTU","1RTU","classAPI_vav_rtu",False,False,4,4,True))
# cur.execute("INSERT INTO supported_devices VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
#             ("Insight","Belkin International Inc.","WiFi","plugload","WeMo","3WIS","classAPI_WeMo",True,False,4,4,True))
# conn.commit()
#
# print "Table supported_devices populated successfully!"

# #8. close database connection
# try:
#     if conn:
#         conn.close()
#         print "{} >> Done 8: database {} connection is closed".format(agent_id, db_database)
# except:
#     print "{} >> database {} connection has already closed".format(agent_id, db_database)
#
# #9. clear volttron log file, kill volttron process, kill all BEMOSS processes
# os.system("sudo chmod 777 -R ~/workspace/bemoss_os")
#
# #TODO make a backup of log files
# os.system("sudo rm ~/workspace/bemoss_os/log/volttron.log")
# os.system("sudo rm ~/workspace/bemoss_os/log/cassandra.log")
#
# os.system("sudo killall volttron")
# os.system("sudo kill $(cat ~/workspace/bemoss_os/.temp/BEMOSS.pid)")
# os.system("sudo rm ~/workspace/bemoss_os/.temp/BEMOSS.pid")
# print "{} >> Done 9: clear volttron log file, kill volttron process, kill all " \
#       "BEMOSS processes".format(agent_id)
#
