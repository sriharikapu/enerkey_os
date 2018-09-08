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
import requests
import socket
import psycopg2
import psycopg2.extras
import pyrebase
import pprint
import psycopg2
import sys
from ISStreamer.Streamer import Streamer
utils.setup_logging()
_log = logging.getLogger(__name__)
__version__ = '3.2'

config = {
    "apiKey": "AIzaSyD4QZ7ko7uXpNK-VBF3Qthhm3Ypzi_bxgQ",
    "authDomain": "hive-rt-mobile-backend.firebaseapp.com",
    "databaseURL": "https://hive-rt-mobile-backend.firebaseio.com",
    "storageBucket": "bucket.appspot.com",
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()

def energybillappagent(config_path, **kwargs):
    config = utils.load_config(config_path)

    def get_config(name):
        try:
            kwargs.pop(name)
        except KeyError:
            return config.get(name, '')

    # 1. @params agent
    agent_id = get_config('agent_id')
    grid_device_id = get_config('grid_device_id')
    load_device_id = get_config('load_device_id')
    solar_device_id = get_config('solar_device_id')
    gateway_id = str(get_config('gateway_id'))

    # 2. @param DB interfaces
    db_host = settings.DATABASES['default']['HOST']
    db_port = settings.DATABASES['default']['PORT']
    db_database = settings.DATABASES['default']['NAME']
    db_user = settings.DATABASES['default']['USER']
    db_password = settings.DATABASES['default']['PASSWORD']
    db_table_daily_consumption = settings.DATABASES['default']['TABLE_daily_consumption']
    # db_table_weekly_consumption = settings.DATABASES['default']['TABLE_weekly_consumption']
    db_table_monthly_consumption = settings.DATABASES['default']['TABLE_monthly_consumption']
    db_table_annual_consumption = settings.DATABASES['default']['TABLE_annual_consumption']
    db_table_cumulative_energy = settings.DATABASES['default']['TABLE_cumulative_energy']

    class EnergyBillAppDevAgent(Agent):
        '''Calculate energy and bill from evergy power sources'''

        def __init__(self, **kwargs):
            super(Agent, self).__init__(**kwargs)
            self.variables = kwargs
            self.start_first_time = True
            self.check_day = datetime.datetime.now().weekday()
            # self.check_week = datetime.datetime.now().isocalendar()[1]
            self.check_month = datetime.datetime.now().month
            self.check_year = datetime.datetime.now().year
            self.current_electricity_price = 3.5
            self.gateway_claimcode = settings.gateway_id
            print('++++++++++++++++++++++++++++++++')
            print('gateway_claimcode : {}'.format(self.gateway_claimcode))
            try:
                self.con = psycopg2.connect(host=db_host, port=db_port, database=db_database,
                                            user=db_user, password=db_password)
                self.cur = self.con.cursor()
                print ("{} connects to the database name {} successfully".format(agent_id, db_database))
            except:
                print("ERROR: {} fails to connect to the database name {}".format(agent_id, db_database))
            self.start_new_day()

        def set_variable(self, k, v):  # postgre k=key, v=value
            self.variables[k] = v

        def get_variable(self, k):
            return self.variables.get(k, None)  # default of get variable is none

        def setup(self):
            super(Agent, self).setup()
            # Demonstrate accessing value from the config file
            # _log.info(config['message'])
            self._agent_id = agent_id
            self.get_yesterday_data()
            self.get_today_data()
            # self.get_last_week_data()
            # self.get_this_week_data()
            self.get_this_month_data()
            self.get_annual_data()

        @Core.receiver('onsetup')
        def onsetup(self, sender, **kwargs):
            # Demonstrate accessing a value from the config file
            _log.info(self.config.get('message', DEFAULT_MESSAGE))
            # self._agent_id = self.config.get('agentid')
            # self.url = self.config.get('backend_url') + self.config.get('scene_api')
            # self.token = self.config.get('token')

        @Core.receiver('onstart')
        def onstart(self, sender, **kwargs):
            _log.debug("VERSION IS: {}".format(self.core.version()))
            self.load_config()
            self.status_old = ""

        def get_today_data(self):
            today = str(datetime.datetime.now().date())
            self.cur.execute("SELECT * FROM " + db_table_daily_consumption + " WHERE date = '" + today + "'" + " AND gateway_id = " + gateway_id)
            try:
                if bool(self.cur.rowcount):
                    data = self.cur.fetchall()[0]
                    self.grid_import_energy_today = float(data[2])
                    self.grid_export_energy_today = float(data[3])
                    self.solar_energy_today = float(data[4])
                    self.load_energy_today = float(data[5])
                    self.grid_import_bill_today = float(data[6])
                    self.grid_export_bill_today = float(data[7])
                    self.solar_bill_today = float(data[8])
                    self.load_bill_today = float(data[9])
                else:
                    self.start_new_day()
            except Exception as er:
                print("get_today_data failed with er: {}".format(er))
                self.start_new_day()

        def start_new_day(self):
            print("staring new day: {}".format(self.check_day))
            self.load_energy_today = 0
            self.solar_energy_today = 0
            self.grid_import_energy_today = 0
            self.grid_export_energy_today = 0
            self.load_bill_today = 0
            self.solar_bill_today = 0
            self.grid_import_bill_today = 0
            self.grid_export_bill_today = 0
            self.get_yesterday_data()
            self.get_this_month_data()

        # def start_new_week(self):
        #     self.load_energy_this_week = 0
        #     self.solar_energy_this_week = 0
        #     self.grid_import_energy_this_week = 0
        #     self.grid_export_energy_this_week = 0
        #     self.load_bill_this_week = 0
        #     self.solar_bill_this_week = 0
        #     self.grid_import_bill_this_week = 0
        #     self.grid_export_bill_this_week = 0
        #     self.get_last_week_data()

        def start_new_month(self):
            self.load_energy_this_month = 0
            self.solar_energy_this_month = 0
            self.grid_import_energy_this_month = 0
            self.grid_export_energy_this_month = 0
            self.load_bill_this_month = 0
            self.solar_bill_this_month = 0
            self.grid_import_bill_this_month = 0
            self.grid_export_bill_this_month = 0
            self.get_last_month_data()

        def start_new_year(self):
            self.load_energy_annual = 0
            self.solar_energy_annual = 0
            self.grid_import_energy_annual = 0
            self.grid_export_energy_annual = 0
            self.load_bill_annual = 0
            self.solar_bill_annual = 0
            self.grid_import_bill_annual = 0
            self.grid_export_bill_annual = 0

        # @matching.match_start('/app/ui/grid/update_ui/bemoss/999')
        # def on_match_gridappagent(self, topic, headers, message, match):
        #     message_from_gridApp = json.loads(message[0])
        #     self.current_electricity_price = message_from_gridApp['current_electricity_price']
        #     print "Current electricity price : {}".format(self.current_electricity_price)

        # # Grid Input
        # @matching.match_exact('/agent/ui/power_meter/device_status_response/bemoss/999/'+grid_device_id)
        # def on_match_etrixgrid(self, topic, headers, message, match):
        #     print "Hello from Grid E-trix: {}".format(json.loads(message[0]))
        #     message_from_power_meter = json.loads(message[0])
        #     if (message_from_power_meter['grid_activePower'] >= 0):
        #         self.energy_from_grid_import = message_from_power_meter['grid_energy']
        #         self.energy_from_grid_export = 0
        #     else:
        #         self.energy_from_grid_export = message_from_power_meter['grid_energy']
        #         self.energy_from_grid_import = 0
        #
        #     self.calculate_grid_energy_bill()
        #
        # # Load Input
        # @matching.match_exact('/agent/ui/power_meter/device_status_response/bemoss/999/' + load_device_id)
        # def on_match_etrixload(self, topic, headers, message, match):
        #     print "Hello from Load E-trix: {}".format(json.loads(message[0]))
        #     message_from_power_meter = json.loads(message[0])
        #     self.energy_from_load = float(message_from_power_meter['grid_energy'])
        #     self.calculate_load_energy_bill()
        #
        # # Solar Input
        # @matching.match_exact('/agent/ui/power_meter/device_status_response/bemoss/999/' + solar_device_id)
        # def on_match_etrixsolar(self, topic, headers, message, match):
        #     print "Hello from Solar E-trix: {}".format(json.loads(message[0]))
        #     message_from_power_meter = json.loads(message[0])
        #     self.energy_from_solar = float(message_from_power_meter['grid_energy'])
        #     self.calculate_solar_energy_bill()

        def calculate_grid_energy_bill(self):
            self.start_new_day_checking()
            self.calculate_grid_energy_today()
            self.calculate_grid_bill_today()
            self.calculate_grid_energy_this_month()
            self.calculate_grid_bill_this_month()
            self.calculate_grid_energy_annual()
            self.calculate_grid_bill_annual()
            # self.updateDB()
            self.publish_message()
            print 'publish firebase grid'
            self.publish_firebase_grid()
            print 'publish streamer grid'
            self.publish_streamer_grid()

        def calculate_load_energy_bill(self):
            self.start_new_day_checking()
            self.calculate_load_energy_today()
            self.calculate_load_bill_today()
            self.calculate_load_energy_this_month()
            self.calculate_load_bill_this_month()
            self.calculate_load_energy_annual()
            self.calculate_load_bill_annual()
            self.updateDB()
            self.publish_message()
            print 'publish firebase load'
            self.publish_firebase_load()
            print 'publish streamer load'
            self.publish_streamer_load()

        def calculate_solar_energy_bill(self):
            self.start_new_day_checking()
            self.calculate_solar_energy_today()
            self.calculate_solar_bill_today()
            self.calculate_solar_energy_this_month()
            self.calculate_solar_bill_this_month()
            self.calculate_solar_energy_annual()
            self.calculate_solar_bill_annual()
            self.updateDB()
            self.publish_message()
            print 'publish firebase solar'
            self.publish_firebase_solar()
            print 'publish streamer solar'
            self.publish_streamer_solar()

        def start_new_day_checking(self):
            today = datetime.datetime.now().weekday()
            print("start_new_day_checking: by comparing today {} with check_dat: {}".format(today, self.check_day))
            if ((self.check_day == 6) and (self.check_day > today)) or (
                (self.check_day is not 6) and (self.check_day < today)):
                self.start_new_day()
                self.check_day = today
            else:
                print("")

        def calculate_grid_energy_today(self):
            self.grid_import_energy_today += self.energy_from_grid_import
            self.grid_export_energy_today += self.energy_from_grid_export

        def calculate_grid_bill_today(self):
            self.grid_import_bill_today += self.energy_from_grid_import * self.current_electricity_price
            self.grid_export_bill_today += self.energy_from_grid_export * self.current_electricity_price

        def calculate_grid_energy_this_month(self):
            self.grid_import_energy_this_month = self.grid_import_energy_this_month_until_last_day + self.grid_import_energy_today
            self.grid_export_energy_this_month = self.grid_export_energy_this_month_until_last_day + self.grid_export_energy_today

        def calculate_grid_bill_this_month(self):
            self.grid_import_bill_this_month = self.grid_import_bill_this_month_until_last_day + self.grid_import_bill_today
            self.grid_export_bill_this_month = self.grid_export_bill_this_month_until_last_day + self.grid_export_bill_today

        def calculate_grid_energy_annual(self):
            self.grid_import_energy_annual = self.grid_import_energy_annual_until_last_month + self.grid_import_energy_this_month
            self.grid_export_energy_annual = self.grid_export_energy_annual_until_last_month + self.grid_export_energy_this_month

        def calculate_grid_bill_annual(self):
            self.grid_import_bill_annual = self.grid_import_bill_annual_until_last_month + self.grid_import_bill_this_month
            self.grid_export_bill_annual = self.grid_export_bill_annual_until_last_month + self.grid_export_bill_this_month

        def calculate_load_energy_today(self):
            self.load_energy_today += self.energy_from_load

        def calculate_load_bill_today(self):
            self.load_bill_today += self.energy_from_load * self.current_electricity_price

        def calculate_load_energy_this_month(self):
            self.load_energy_this_month = self.load_energy_this_month_until_last_day + self.load_energy_today

        def calculate_load_bill_this_month(self):
            self.load_bill_this_month = self.load_bill_this_month_until_last_day + self.load_bill_today

        def calculate_load_energy_annual(self):
            self.load_energy_annual = self.load_energy_annual_until_last_month + self.load_energy_this_month

        def calculate_load_bill_annual(self):
            self.load_bill_annual = self.load_bill_annual_until_last_month + self.load_bill_this_month

        def calculate_solar_energy_today(self):
            self.solar_energy_today += self.energy_from_solar

        def calculate_solar_bill_today(self):
            self.solar_bill_today += self.energy_from_solar * self.current_electricity_price

        def calculate_solar_energy_this_month(self):
            self.solar_energy_this_month = self.solar_energy_this_month_until_last_day + self.solar_energy_today

        def calculate_solar_bill_this_month(self):
            self.solar_bill_this_month = self.solar_bill_this_month_until_last_day + self.solar_bill_today

        def calculate_solar_energy_annual(self):
            self.solar_energy_annual = self.solar_energy_annual_until_last_month + self.solar_energy_this_month

        def calculate_solar_bill_annual(self):
            self.solar_bill_annual = self.solar_bill_annual_until_last_month + self.solar_bill_this_month

        def start_new_month_checking(self):
            this_month = datetime.datetime.now().month
            if ((self.check_month == 12) and (self.check_month > this_month)) or (
                (self.check_month is not 12) and (self.check_month < this_month)):
                self.start_new_month()
                self.check_month = this_month
            else:
                pass

        def start_new_year_checking(self):
            this_year = datetime.datetime.now().year
            if self.check_year < this_year:
                self.start_new_year()
                self.check_year = this_year
            else:
                pass

        def insertDB(self, table):
            if (table == 'daily'):
                self.cur.execute("INSERT INTO " + db_table_daily_consumption +
                                 " (date, gridimportenergy, gridexportenergy, solarenergy, loadenergy, "
                                 "gridimportbill, gridexportbill, solarbill, loadbill, updated_at, gateway_id) "
                                 "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                 ((str(datetime.datetime.now().date())),
                                  self.grid_import_energy_today, self.grid_export_energy_today,
                                  self.solar_energy_today, self.load_energy_today,
                                  self.grid_import_bill_today, self.grid_export_bill_today,
                                  self.solar_bill_today, self.load_bill_today,
                                  datetime.datetime.now(), gateway_id))
                self.con.commit()

            # elif (table == 'weekly'):
            #     self.cur.execute("INSERT INTO " + db_table_weekly_consumption +
            #                      " (date, gridimportenergy, gridexportenergy, solarenergy, loadenergy, "
            #                      "gridimportbill, gridexportbill, solarbill, loadbill, updated_at, gateway_id) "
            #                      "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            #                      ((str((datetime.datetime.now() - relativedelta(weekday=MO(-1))).date())),
            #                       self.grid_import_energy_this_week, self.grid_export_energy_this_week,
            #                       self.solar_energy_this_week, self.load_energy_this_week,
            #                       self.grid_import_bill_this_week, self.grid_export_bill_this_week,
            #                       self.solar_bill_this_week, self.load_bill_this_week, datetime.datetime.now(), '8'))
            #     self.con.commit()

            elif (table == 'monthly'):
                self.cur.execute("INSERT INTO " + db_table_monthly_consumption +
                                 " (date, gridimportenergy, gridexportenergy, solarenergy, loadenergy, "
                                 "gridimportbill, gridexportbill, solarbill, loadbill, updated_at, gateway_id) "
                                 "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                 ((str(datetime.datetime.now().date() + relativedelta(day=31))),
                                  self.grid_import_energy_this_month, self.grid_export_energy_this_month,
                                  self.solar_energy_this_month, self.load_energy_this_month,
                                  self.grid_import_bill_this_month, self.grid_export_bill_this_month,
                                  self.solar_bill_this_month, self.load_bill_this_month, datetime.datetime.now(), gateway_id))
                self.con.commit()

            elif (table == 'annual'):
                self.cur.execute("INSERT INTO " + db_table_annual_consumption +
                                 " (date, gridimportenergy, gridexportenergy, solarenergy, loadenergy, "
                                 "gridimportbill, gridexportbill, solarbill, loadbill, gateway_id) "
                                 "VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                 ((str(datetime.datetime.now().replace(month=12).date() + relativedelta(day=31))),
                                  self.grid_import_energy_annual, self.grid_export_energy_annual,
                                  self.solar_energy_annual, self.load_energy_annual,
                                  self.grid_import_bill_annual, self.grid_export_bill_annual,
                                  self.solar_bill_annual, self.load_bill_annual, gateway_id))
                self.con.commit()

            elif (table == 'cumulative'):
                # self.connect_postgresdb()
                self.cur.execute("INSERT INTO " + db_table_cumulative_energy +
                                 " (date_add, energyconsumption, solargeneration, gateway_id) "
                                 "VALUES(%s, %s, %s, %s)",
                                 (datetime.datetime.now(), self.energy_from_grid_import, self.energy_from_solar, gateway_id))

                self.con.commit()
                print"insert to db:Success"

        def updateDB(self):
            try:
                self.insertDB('cumulative')
            except Exception as er:
                print "insert data base error: {}".format(er)
            today = str(datetime.datetime.now().date())
            last_day_of_this_month = str(datetime.datetime.now().date() + relativedelta(day=31))
            last_day_of_end_month = str(datetime.datetime.now().replace(month=12).date() + relativedelta(day=31))

            # Update table "daily_consumption"
            self.cur.execute("SELECT * FROM " + db_table_daily_consumption + " WHERE date = '" + today + "'" + " AND gateway_id = " + gateway_id)
            try:
                if bool(self.cur.rowcount):
                    try:
                        self.cur.execute(
                            "UPDATE " + db_table_daily_consumption + " SET gridimportenergy=%s, gridexportenergy=%s, "
                                                                     "solarenergy=%s, loadenergy=%s, gridimportbill=%s,"
                                                                     "gridexportbill=%s, solarbill=%s, loadbill=%s, updated_at=%s"
                                                                     " WHERE date = '" + today + "'" + " AND gateway_id = " + gateway_id,
                            (self.grid_import_energy_today, self.grid_export_energy_today,
                            self.solar_energy_today, self.load_energy_today,
                            self.grid_import_bill_today, self.grid_export_bill_today,
                                  self.solar_bill_today, self.load_bill_today, datetime.datetime.now()))
                        self.con.commit()
                        print"update daily db:Success"
                    except Exception as er:
                        print "update data base error: {}".format(er)
                else:
                    self.insertDB('daily')
            except Exception as er:
                print("{} failed to updateDB daily_energy with error: {}".format(agent_id, er))

            # Update table "monthly consumption"
            try:
                self.cur.execute(
                    "SELECT * FROM " + db_table_monthly_consumption + " WHERE date = '" + last_day_of_this_month + "'" + " AND gateway_id = " + gateway_id)
                if bool(self.cur.rowcount):
                    try:
                        self.cur.execute(
                            "UPDATE " + db_table_monthly_consumption + " SET gridimportenergy=%s, gridexportenergy=%s, "
                                                                       "solarenergy=%s, loadenergy=%s, gridimportbill=%s,"
                                                                       "gridexportbill=%s, solarbill=%s, loadbill=%s"
                                                                       " WHERE date = '" + last_day_of_this_month + "'" + " AND gateway_id = " + gateway_id,
                            (self.grid_import_energy_this_month, self.grid_export_energy_this_month,
                             self.solar_energy_this_month, self.load_energy_this_month,
                             self.grid_import_bill_this_month, self.grid_export_bill_this_month,
                             self.solar_bill_this_month, self.load_bill_this_month))

                        self.con.commit()
                        print"update monthly db:Success"
                    except Exception as er:
                        print "update data base error: {}".format(er)
                else:
                    self.insertDB('monthly')
            except Exception as er:
                print("{} failed to updateDB monthly_energy with error: {}".format(agent_id, er))

            # Update table "annual consumption"
            try:
                self.cur.execute(
                    "SELECT * FROM " + db_table_annual_consumption + " WHERE date = '" + last_day_of_end_month + "'" + " AND gateway_id = " + gateway_id)
                if bool(self.cur.rowcount):
                    try:
                        self.cur.execute(
                            "UPDATE " + db_table_annual_consumption + " SET gridimportenergy=%s, gridexportenergy=%s, "
                                                                      "solarenergy=%s, loadenergy=%s, gridimportbill=%s,"
                                                                      "gridexportbill=%s, solarbill=%s, loadbill=%s"
                                                                      " WHERE date = '" + last_day_of_end_month + "'" + " AND gateway_id = " + gateway_id,
                            (self.grid_import_energy_annual, self.grid_export_energy_annual,
                             self.solar_energy_annual, self.load_energy_annual,
                             self.grid_import_bill_annual, self.grid_export_bill_annual,
                             self.solar_bill_annual, self.load_bill_annual))

                        self.con.commit()
                        print"update annual db:Success"
                    except Exception as er:
                        print "update data base error: {}".format(er)
                else:
                    self.insertDB('annual')
            except Exception as er:
                print("{} failed to updateDB annual_energy with error: {}".format(agent_id, er))

        def get_yesterday_data(self):
            print("getting yesterday data")
            time_now = datetime.datetime.now()
            last_day = str((time_now - datetime.timedelta(days=1)).date())
            self.cur.execute("SELECT * FROM " + db_table_daily_consumption + " WHERE date = '" + last_day + "'" + " AND gateway_id = " + gateway_id)
            if bool(self.cur.rowcount):
                try:
                    data = self.cur.fetchall()[0]
                    self.grid_import_energy_last_day = float(data[2])
                    self.grid_export_energy_last_day = float(data[3])
                    self.solar_energy_last_day = float(data[4])
                    self.load_energy_last_day = float(data[5])
                    self.grid_import_bill_last_day = float(data[6])
                    self.grid_export_bill_last_day = float(data[7])
                    self.solar_bill_last_day = float(data[8])
                    self.load_bill_last_day = float(data[9])
                except Exception as er:
                    self.grid_import_energy_last_day = 0
                    self.grid_export_energy_last_day = 0
                    self.solar_energy_last_day = 0
                    self.load_energy_last_day = 0
                    self.grid_import_bill_last_day = 0
                    self.grid_export_bill_last_day = 0
                    self.solar_bill_last_day = 0
                    self.load_bill_last_day = 0
                    print("There is no yesterday data: {}".format(er))
            else:
                self.grid_import_energy_last_day = 0
                self.grid_export_energy_last_day = 0
                self.solar_energy_last_day = 0
                self.load_energy_last_day = 0
                self.grid_import_bill_last_day = 0
                self.grid_export_bill_last_day = 0
                self.solar_bill_last_day = 0
                self.load_bill_last_day = 0

        def get_last_month_data(self):
            self.grid_import_energy_last_month = 0
            self.grid_export_energy_last_month = 0
            self.solar_energy_last_month = 0
            self.load_energy_last_month = 0
            self.grid_import_bill_last_month = 0
            self.grid_export_bill_last_month = 0
            self.solar_bill_last_month = 0
            self.load_bill_last_month = 0
            first_date = (datetime.datetime.now() - relativedelta(months=1)).replace(day=1).date()
            end_date = first_date + relativedelta(day=31)
            first_date_str = str(first_date)
            end_date_str = str(end_date)
            self.cur.execute("SELECT * FROM " + db_table_daily_consumption + " WHERE (date BETWEEN '" +
                             first_date_str + "' AND '" + end_date_str + "')" + " AND gateway_id = 8")
            if bool(self.cur.rowcount):
                data = self.cur.fetchall()
                for i in range(len(data)):
                    self.grid_import_energy_last_month += float(data[i][2])
                    self.grid_export_energy_last_month += float(data[i][3])
                    self.solar_energy_last_month += float(data[i][4])
                    self.load_energy_last_month += float(data[i][5])
                    self.grid_import_bill_last_month += float(data[i][6])
                    self.grid_export_bill_last_month += float(data[i][7])
                    self.solar_bill_last_month += float(data[i][8])
                    self.load_bill_last_month += float(data[i][9])
            else:
                pass

        def get_this_month_data(self):
            print('getting this month data')
            self.grid_import_energy_this_month_until_last_day = 0
            self.grid_export_energy_this_month_until_last_day = 0
            self.solar_energy_this_month_until_last_day = 0
            self.load_energy_this_month_until_last_day = 0
            self.grid_import_bill_this_month_until_last_day = 0
            self.grid_export_bill_this_month_until_last_day = 0
            self.solar_bill_this_month_until_last_day = 0
            self.load_bill_this_month_until_last_day = 0

            first_date = datetime.datetime.now().replace(day=1).date()
            end_date = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
            first_date_str = str(first_date)
            end_date_str = str(end_date)
            # self.connect_postgresdb()
            self.cur.execute("SELECT * FROM " + db_table_daily_consumption + " WHERE (date BETWEEN '" +
                             first_date_str + "' AND '" + end_date_str + "')" + " AND gateway_id = " + gateway_id)
            if bool(self.cur.rowcount):
                data = self.cur.fetchall()
                for i in range(len(data)):
                    try:
                        self.grid_import_energy_this_month_until_last_day += float(data[i][2])
                        self.grid_export_energy_this_month_until_last_day += float(data[i][3])
                        self.solar_energy_this_month_until_last_day += float(data[i][4])
                        self.load_energy_this_month_until_last_day += float(data[i][5])
                        self.grid_import_bill_this_month_until_last_day += float(data[i][6])
                        self.grid_export_bill_this_month_until_last_day += float(data[i][7])
                        self.solar_bill_this_month_until_last_day += float(data[i][8])
                        self.load_bill_this_month_until_last_day += float(data[i][9])
                    except Exception as er:
                        print("no data {}".format(er))
            else:
                self.start_new_month()

        def get_annual_data(self):
            self.grid_import_energy_annual_until_last_month = 0
            self.grid_export_energy_annual_until_last_month = 0
            self.solar_energy_annual_until_last_month = 0
            self.load_energy_annual_until_last_month = 0
            self.grid_import_bill_annual_until_last_month = 0
            self.grid_export_bill_annual_until_last_month = 0
            self.solar_bill_annual_until_last_month = 0
            self.load_bill_annual_until_last_month = 0

            first_month = datetime.datetime.now().replace(month=1, day=31).date()
            this_month = (datetime.datetime.now() - datetime.timedelta(days=31) + relativedelta(day=31)).date()
            first_month_str = str(first_month)
            this_month_str = str(this_month)

            self.cur.execute("SELECT * FROM " + db_table_monthly_consumption + " WHERE (date BETWEEN '" +
                             first_month_str + "' AND '" + this_month_str + "')" + " AND gateway_id = " + gateway_id)

            if bool(self.cur.rowcount) and (first_month < this_month):
                    data = self.cur.fetchall()
                    for i in range(len(data)):
                        self.grid_import_energy_annual_until_last_month += float(data[i][2])
                        self.grid_export_energy_annual_until_last_month += float(data[i][3])
                        self.solar_energy_annual_until_last_month += float(data[i][4])
                        self.load_energy_annual_until_last_month += float(data[i][5])
                        self.grid_import_bill_annual_until_last_month += float(data[i][6])
                        self.grid_export_bill_annual_until_last_month += float(data[i][7])
                        self.solar_bill_annual_until_last_month += float(data[i][8])
                        self.load_bill_annual_until_last_month += float(dataf[i][9])
            else:
                self.start_new_year()

        def publish_message(self):
            topic = "/app/ui/energybillapp/update_ui/bemoss/999"
            now = datetime.datetime.utcnow().isoformat(' ') + 'Z'
            headers = {
                'AgentID': self._agent_id,
                headers_mod.CONTENT_TYPE: headers_mod.CONTENT_TYPE.PLAIN_TEXT,
                headers_mod.DATE: now,
                'receiver_agent_id': "ui"
            }
            try:
                message = json.dumps(({"daily_energy_usage": round(self.get_variable('loadEnergy'), 2),
                                       "last_day_energy_usage": round(self.load_energy_last_day, 2),
                                       "daily_electricity_bill": round(self.get_variable('gridImportBill'), 2),
                                       "last_day_bill_compare": round(
                                           self.get_variable('gridImportBill') - self.grid_import_bill_last_day, 2),
                                       "monthly_energy_usage": round(self.load_energy_this_month, 2),
                                       "last_month_energy_usage": round(self.load_energy_last_month, 2),
                                       "monthly_electricity_bill": round(self.grid_import_bill_this_month, 2),
                                       "last_month_bill_compare": round(
                                           (self.grid_import_bill_this_month - self.grid_import_bill_last_month), 2),
                                       "netzero_onsite_generation": round(self.solar_energy_annual, 2),
                                       "netzero_energy_consumption": round(self.load_energy_annual, 2)}))

                self.publish(topic, headers, message)
                print ("{} published topic: {}, message: {}").format(self._agent_id, topic, message)
            except:
                pass

        def publish_firebase_grid(self):
            try:
                # daily_energy
                db.child(self.gateway_claimcode).child('daily_energy').child("gridimportbill").set(round(self.grid_import_bill_today, 4))
                print("Firebase: daily_energy gridimportbill: {}".format(round(self.grid_import_bill_today, 4)))
                db.child(self.gateway_claimcode).child('daily_energy').child("gridimportenergy").set(round(self.grid_import_energy_today, 4))
                print("Firebase: daily_energy gridimportenergy: {}".format(round(self.grid_import_energy_today, 4)))

                # monthly_energy
                db.child(self.gateway_claimcode).child('monthly_energy').child("gridimportbill").set(
                    round(self.grid_import_bill_this_month, 4))
                print("Firebase: monthly_energy gridimportbill: {}".format(round(self.grid_import_bill_this_month, 4)))
                db.child(self.gateway_claimcode).child('monthly_energy').child("gridimportenergy").set(
                    round(self.grid_import_energy_this_month, 4))
                print("Firebase: monthly_energy gridimportenergy: {}".format(round(self.grid_import_energy_this_month, 4)))

                # annual_energy
                db.child(self.gateway_claimcode).child('annual_energy').child("gridimportbill").set(
                    round(self.grid_import_bill_annual, 4))
                print("Firebase: annual_energy gridimportbill: {}".format(round(self.grid_import_bill_annual, 4)))
                db.child(self.gateway_claimcode).child('annual_energy').child("gridimportenergy").set(
                    round(self.grid_import_energy_annual, 4))
                print("Firebase: annual_energy gridimportenergy: {}".format(round(self.grid_import_energy_annual, 4)))

            except Exception as er:
                print "cannot read data: {}".format(er)

        def publish_firebase_load(self):
            print 'data sent to LOAD firebase'
            try:
                # daily_energy
                print("Firebase: daily_energy loadbill: {}".format(round(self.load_bill_today, 4)))
                db.child(self.gateway_claimcode).child('daily_energy').child("loadbill").set(round(self.load_bill_today, 4))
                print("Firebase: daily_energy loadenergy: {}".format(round(self.load_energy_today, 4)))
                db.child(self.gateway_claimcode).child('daily_energy').child("loadenergy").set(round(self.load_energy_today, 4))

                # monthly_energy
                print("Firebase: monthly_energy loadbill: {}".format(round(self.load_bill_this_month, 4)))
                db.child(self.gateway_claimcode).child('monthly_energy').child("loadbill").set(round(self.load_bill_this_month, 4))
                print("Firebase: monthly_energy loadenergy: {}".format(round(self.load_energy_this_month, 4)))
                db.child(self.gateway_claimcode).child('monthly_energy').child("loadenergy").set(round(self.load_energy_this_month, 4))

                # annual_energy
                print("Firebase: annual_energy loadbill: {}".format(round(self.load_bill_annual, 4)))
                db.child(self.gateway_claimcode).child('annual_energy').child("loadbill").set(
                    round(self.load_bill_annual, 4))
                print("Firebase: annual_energy loadenergy: {}".format(round(self.load_energy_this_month, 4)))
                db.child(self.gateway_claimcode).child('annual_energy').child("loadenergy").set(
                    round(self.load_energy_annual, 4))

            except Exception as er:
                print "cannot read data: {}".format(er)

        def publish_firebase_solar(self):
            print 'data sent to Solar firebase'
            try:
                # daily_energy
                print("Firebase: daily_energy solarbill: {}".format(round(self.solar_bill_today, 4)))
                db.child(self.gateway_claimcode).child('daily_energy').child("solarbill").set(round(self.solar_bill_today, 4))
                print("Firebase: daily_energy solarenergy: {}".format(round(self.solar_energy_today, 4)))
                db.child(self.gateway_claimcode).child('daily_energy').child("solarenergy").set(round(self.solar_energy_today, 4))

                # monthly_energy
                print("Firebase: monthly_energy solarbill: {}".format(round(self.solar_bill_this_month, 4)))
                db.child(self.gateway_claimcode).child('monthly_energy').child("solarbill").set(
                    round(self.solar_bill_this_month, 4))
                print("Firebase: monthly_energy solarenergy: {}".format(round(self.solar_energy_this_month, 4)))
                db.child(self.gateway_claimcode).child('monthly_energy').child("solarenergy").set(
                    round(self.solar_energy_this_month, 4))

                # annual_energy
                print("Firebase: annual_energy solarbill: {}".format(round(self.solar_bill_annual, 4)))
                db.child(self.gateway_claimcode).child('annual_energy').child("solarbill").set(
                    round(self.solar_bill_annual, 4))
                print("Firebase: annual_energy solarenergy: {}".format(round(self.solar_energy_this_month, 4)))
                db.child(self.gateway_claimcode).child('annual_energy').child("solarenergy").set(
                    round(self.solar_energy_annual, 4))

            except Exception as er:
                print "cannot read data: {}".format(er)

        def publish_streamer_grid(self):
            try:
                streamer = Streamer(bucket_name="srisaengtham", bucket_key="WSARH9FBXEBX",
                                    access_key="4YM0GM6ZNUAZtHT8LYWxQSAdrqaxTipw")
                streamer.log(self._agent_id + '_daily_energy' + '_gridimportbill', round(self.grid_import_bill_today, 4))
                streamer.log(self._agent_id + '_daily_energy' + '_gridimportenergy', round(self.grid_import_energy_today, 4))
                streamer.log(self._agent_id + '_monthly_energy' + '_gridimportbill', round(self.grid_import_bill_this_month, 4))
                streamer.log(self._agent_id + '_monthly_energy' + '_gridimportenergy', round(self.grid_import_energy_this_month, 4))
                streamer.log(self._agent_id + '_annual_energy' + '_gridimportbill', round(self.grid_import_bill_annual, 4))
                streamer.log(self._agent_id + '_annual_energy' + '_gridimportenergy', round(self.grid_import_energy_annual, 4))

            except Exception as er:
                print "update data base error: {}".format(er)

        def publish_streamer_load(self):
            try:
                streamer = Streamer(bucket_name="srisaengtham", bucket_key="WSARH9FBXEBX",
                                    access_key="4YM0GM6ZNUAZtHT8LYWxQSAdrqaxTipw")
                streamer.log(self._agent_id + '_daily_energy' + '_loadimportbill',
                             round(self.load_bill_today, 4))
                streamer.log(self._agent_id + '_daily_energy' + '_loadimportenergy',
                             round(self.load_energy_today, 4))
                streamer.log(self._agent_id + '_monthly_energy' + '_loadimportbill',
                             round(self.load_bill_this_month, 4))
                streamer.log(self._agent_id + '_monthly_energy' + '_loadimportenergy',
                             round(self.load_energy_this_month, 4))
                streamer.log(self._agent_id + '_annual_energy' + '_loadimportbill',
                             round(self.load_bill_annual, 4))
                streamer.log(self._agent_id + '_annual_energy' + '_loadimportenergy',
                             round(self.load_energy_annual, 4))
            except Exception as er:
                print "update data base error: {}".format(er)

        def publish_streamer_solar(self):
            try:
                streamer = Streamer(bucket_name="srisaengtham", bucket_key="WSARH9FBXEBX",
                                    access_key="4YM0GM6ZNUAZtHT8LYWxQSAdrqaxTipw")
                streamer.log(self._agent_id + '_daily_energy' + '_solarimportbill',
                             round(self.solar_bill_today, 4))
                streamer.log(self._agent_id + '_daily_energy' + '_solarimportenergy',
                             round(self.solar_energy_today, 4))
                streamer.log(self._agent_id + '_monthly_energy' + '_solarimportbill',
                             round(self.solar_bill_this_month, 4))
                streamer.log(self._agent_id + '_monthly_energy' + '_solarimportenergy',
                             round(self.solar_energy_this_month, 4))
                streamer.log(self._agent_id + '_annual_energy' + '_solarimportbill',
                             round(self.solar_bill_annual, 4))
                streamer.log(self._agent_id + '_annual_energy' + '_solarimportenergy',
                             round(self.solar_energy_annual, 4))
            except Exception as er:
                print "update data base error: {}".format(er)

    Agent.__name__ = 'energybillappdevAgent'
    return EnergyBillAppDevAgent(config_path, **kwargs)

def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(energybillappagent, version=__version__)

    except Exception as e:
        _log.exception('unhandled exception')


if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
