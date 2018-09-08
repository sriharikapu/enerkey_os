# -*- coding: utf-8 -*-
'''
Copyright (c) 2016, Virginia Tech
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
 following conditions are met:
1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those of the authors and should not be
interpreted as representing official policies, either expressed or implied, of the FreeBSD Project.

This material was prepared as an account of work sponsored by an agency of the United States Government. Neither the
United States Government nor the United States Department of Energy, nor Virginia Tech, nor any of their employees,
nor any jurisdiction or organization that has cooperated in the development of these materials, makes any warranty,
express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness or
any information, apparatus, product, software, or process disclosed, or represents that its use would not infringe
privately owned rights.

Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or
otherwise does not necessarily constitute or imply its endorsement, recommendation, favoring by the United States
Government or any agency thereof, or Virginia Tech - Advanced Research Institute. The views and opinions of authors
expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.

VIRGINIA TECH – ADVANCED RESEARCH INSTITUTE
under Contract DE-EE0006352

#__author__ = "PEA HiVE Team"
#__credits__ = ""
#__version__ = "2.0"
#__maintainer__ = "BEMOSS Team"
#__email__ = "aribemoss@gmail.com"
#__website__ = "www.bemoss.org"
#__created__ = "2014-09-12 12:04:50"
#__lastUpdated__ = "2016-12-07 16:43:35"
'''
import time
import json

import requests
import urllib3
#from bemoss_lib.utils import rgb_cie
class API:
    # 1. constructor : gets call every time when create a new class
    # requirements for instantiation1. model, 2.type, 3.api, 4. address
    def __init__(self, **kwargs):
        # Initialized common attributes
        self.variables = kwargs
        self.debug = True

    def renewConnection(self):
        pass

    def set_variable(self, k, v):  # k=key, v=value
        self.variables[k] = v

    def get_variable(self,k):
        return self.variables.get(k, None)  # default of get_variable is none

    # 2. Attributes from Attributes table

    '''
    Attributes:
     ------------------------------------------------------------------------------------------
    label              GET          label in string
    Time(Unix)         GET          time in unix
    grid_current
    grid_activePower
    grid_reactivePower
    grid_powerfactor

     ------------------------------------------------------------------------------------------

    '''
    # 3. Capabilites (methods) from Capabilities table
    '''
    API3 available methods:
    1. getDeviceStatus() GET
    '''

    # ----------------------------------------------------------------------
    def getDeviceStatus(self):

        device_id = str(self.get_variable("device_id"))
        # set for event
        device_id_1 = '699639095' # grid
        device_id_2 = '250883398' # solar1
        device_id_3 = '250883398' # solar2

        # device id 1
        try:
            url = 'https://cplservice.com/apixmobile.php/cpletrix?filter=device_id,eq,'+device_id_1+'&order=trans_id,desc&page=1'
            print url
            http = urllib3.PoolManager()
            r = http.request('GET', url)
            conve_json = json.loads(r.data)

            self.set_variable('1_voltage', float(conve_json['cpletrix']['records'][0][5]))
            self.set_variable('1_current', float(conve_json['cpletrix']['records'][0][6]))

            gridactive0 = (float(conve_json['cpletrix']['records'][0][9]))

            if (gridactive0 > (-20) and gridactive0 < (0)):
                gridactive = 0
            else:
                gridactive = gridactive0

            self.set_variable('1_activePower',gridactive)
            self.set_variable('1_reactivePower', float(conve_json['cpletrix']['records'][0][10]))
            self.set_variable('1_powerfactor', float(conve_json['cpletrix']['records'][0][8]))
            self.set_variable('1_accumulated_energy', float(conve_json['cpletrix']['records'][0][11]))

        except Exception as er:
            print er

        # device id 2
        try:
            url = 'https://cplservice.com/apixmobile.php/cpletrix?filter=device_id,eq,' + device_id_2 + '&order=trans_id,desc&page=1'
            print url
            http = urllib3.PoolManager()
            r = http.request('GET', url)
            conve_json = json.loads(r.data)

            self.set_variable('2_voltage', float(conve_json['cpletrix']['records'][0][5]))
            self.set_variable('2_current', float(conve_json['cpletrix']['records'][0][6]))

            gridactive0 = (float(conve_json['cpletrix']['records'][0][9]))

            if (gridactive0 > (-20) and gridactive0 < (0)):
                gridactive = 0
            else:
                gridactive = gridactive0

            self.set_variable('2_activePower', gridactive)
            self.set_variable('2_reactivePower', float(conve_json['cpletrix']['records'][0][10]))
            self.set_variable('2_powerfactor', float(conve_json['cpletrix']['records'][0][8]))
            self.set_variable('2_accumulated_energy', float(conve_json['cpletrix']['records'][0][11]))

        except Exception as er:
            print er

        # device id 3
        try:
            url = 'https://cplservice.com/apixmobile.php/cpletrix?filter=device_id,eq,' + device_id_3 + '&order=trans_id,desc&page=1'
            print url
            http = urllib3.PoolManager()
            r = http.request('GET', url)
            conve_json = json.loads(r.data)

            self.set_variable('3_voltage', float(conve_json['cpletrix']['records'][0][5]))
            self.set_variable('3_current', float(conve_json['cpletrix']['records'][0][6]))

            gridactive0 = (float(conve_json['cpletrix']['records'][0][9]))

            if (gridactive0 > (-20) and gridactive0 < (0)):
                gridactive = 0
            else:
                gridactive = gridactive0

            self.set_variable('3_activePower', gridactive)
            self.set_variable('3_reactivePower', float(conve_json['cpletrix']['records'][0][10]))
            self.set_variable('3_powerfactor', float(conve_json['cpletrix']['records'][0][8]))
            self.set_variable('3_accumulated_energy', float(conve_json['cpletrix']['records'][0][11]))

        except Exception as er:
            print er

        # calculate
        try:
            self.set_variable('grid_voltage',
                              float(self.get_variable('1_voltage')))
            self.set_variable('grid_current',
                              float(self.get_variable('1_current') + self.get_variable('2_current') + self.get_variable('3_current')))
            self.set_variable('grid_activePower',
                              float(self.get_variable('1_activePower') + self.get_variable('2_activePower') + self.get_variable('3_activePower')))
            self.set_variable('grid_reactivePower',
                              float(self.get_variable('1_reactivePower') + self.get_variable('2_reactivePower') + self.get_variable('3_reactivePower')))
            self.set_variable('grid_powerfactor',
                              float(self.get_variable('1_powerfactor')))
            self.set_variable('grid_accumulated_energy',
                              float(self.get_variable('1_accumulated_energy') + self.get_variable('2_accumulated_energy') + self.get_variable('3_accumulated_energy')))

        except Exception as er:
            print er

        # ---------- old
        # try:
        #
        #     url = 'https://cplservice.com/apixmobile.php/cpletrix?filter=device_id,eq,'+device_id_load+'&order=trans_id,desc&page=1'
        #     print url
        #     http = urllib3.PoolManager()
        #     # r = http.request('GET','https://cplservice.com/apixmobile.php/cpletrix?filter=device_id,eq,250883398&order=trans_id,desc&page=1')
        #     # r = http.request('GET', 'https://cplservice.com/apixmobile.php/cpletrix?filter=device_id,eq,300346794&order=trans_id,desc&page=1')
        #     r = http.request('GET', url)
        #     conve_json = json.loads(r.data)
        #     # print r.data
        #     print
        #     self.set_variable('l_grid_voltage', float(conve_json['cpletrix']['records'][0][5]))
        #     self.set_variable('l_grid_current', float(conve_json['cpletrix']['records'][0][6]))
        #     self.set_variable('l_grid_activePower', float(conve_json['cpletrix']['records'][0][9]))
        #     self.set_variable('l_grid_reactivePower', float(conve_json['cpletrix']['records'][0][10]))
        #     self.set_variable('l_grid_powerfactor', float(conve_json['cpletrix']['records'][0][8]))
        #     self.set_variable('l_grid_accumulated_energy', float(conve_json['cpletrix']['records'][0][11]))
        #
        # except Exception as er:
        #     print er
        #
        # try:
        #     self.set_variable('grid_voltage', float(self.get_variable('l_grid_voltage')))
        #     self.set_variable('grid_current',
        #                       float(self.get_variable('l_grid_current') - self.get_variable('g_grid_current')))
        #     self.set_variable('grid_activePower', float(self.get_variable('l_grid_activePower') -
        #                                                 self.get_variable('g_grid_activePower')))
        #     self.set_variable('grid_reactivePower', float(
        #         self.get_variable('l_grid_reactivePower') - self.get_variable('g_grid_reactivePower')))
        #     self.set_variable('grid_powerfactor', float(self.get_variable('l_grid_powerfactor')))
        #     self.set_variable('grid_accumulated_energy', float(
        #         self.get_variable('l_grid_accumulated_energy') - self.get_variable('g_grid_accumulated_energy')))
        #
        # except Exception as er:
        #     print er

    def printDeviceStatus(self):

        print ("--------------------------------Creative Power status--------------------------------")
        print(" Voltage(V) = {}".format(self.get_variable('grid_voltage')))
        print(" Current(A) = {}".format(self.get_variable('grid_current')))
        print(" ActivePower(W) = {}".format(self.get_variable('grid_activePower')))
        print(" ReactivePower(Var) = {}".format(self.get_variable('grid_reactivePower')))
        print(" Powerfactor = {}".format(self.get_variable('grid_powerfactor')))
        print(" AccumulatedEnergy(Wh) = {}".format(self.get_variable('grid_accumulated_energy')))
        print(" 1_AccumulatedEnergy(Wh) = {}".format(self.get_variable('1_accumulated_energy')))
        print(" 2_AccumulatedEnergy(Wh) = {}".format(self.get_variable('2_accumulated_energy')))


    # ----------------------------------------------------------------------

# This main method will not be executed when this class is used as a module
def main():
    Creative_Power = API(model='e-Trix@Larm', type='powermeter', api='classAPI_CreativePower', agent_id='Creative_Power',device_id='250883398')
    Creative_Power.getDeviceStatus()
    Creative_Power.printDeviceStatus()
    # Creative_Power.printDeviceStatus()

if __name__ == "__main__": main()
