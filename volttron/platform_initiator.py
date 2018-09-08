# -*- coding: utf-8 -*-

import os
import sys
import json
os.chdir(os.path.expanduser("~/workspace/hive_os/"))  # = ~/workspace/bemoss_os
os.system("service postgresql restart")
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

cur.execute("select * from information_schema.tables where table_name=%s", ('scenes',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    cur.execute("DROP TABLE scenes")
    conn.commit()
else:
    pass

cur.execute("select * from information_schema.tables where table_name=%s", ('automation',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    cur.execute("DROP TABLE automation")
    conn.commit()
else:
    pass

cur.execute("select * from information_schema.tables where table_name=%s", ('active_scene',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    cur.execute("DROP TABLE active_scene")
    conn.commit()
else:
    pass

cur.execute("select * from information_schema.tables where table_name=%s", ('token',))
print bool(cur.rowcount)
if bool(cur.rowcount):
    cur.execute("DROP TABLE token")
    conn.commit()
else:
    pass

cur.execute('''CREATE TABLE scenes
       (SCENE_ID SERIAL   PRIMARY KEY   NOT NULL,
       SCENE_NAME   VARCHAR(30)   NOT NULL,
       SCENE_TASKS     TEXT);''')
print "Table scenes created successfully"
conn.commit()

cur.execute('''CREATE TABLE automation
            (AUTOMATION_ID SERIAL PRIMARY KEY   NOT NULL,
            AUTOMATION_IMAGE VARCHAR(100) ,
            AUTOMATION_NAME VARCHAR(30) NOT NULL,
            TRIGGER_DEVICE  TEXT NOT NULL,
            TRIGGER_EVENT VARCHAR(30) NOT NULL,
            TRIGGER_VALUE VARCHAR(30) NOT NULL,
            CONDITION_EVENT VARCHAR(30) NOT NULL,
            CONDITION_VALUE TEXT NOT NULL,
            ACTION_TASKS TEXT);''')
print("Table automation created successfully")
conn.commit()

cur.execute('''CREATE TABLE active_scene
            (SCENE_ID VARCHAR(30),
             SCENE_NAME VARCHAR(30) NOT NULL);''')
print("Table active scene created successfully")
conn.commit()

cur.execute('''CREATE TABLE token
            (gateway_id VARCHAR(30),
            login_token VARCHAR(30),
             expo_token VARCHAR(30));''')
print("Table active scene created successfully")
conn.commit()