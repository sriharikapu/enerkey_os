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
#__maintainer__ = "PEAHiVE Team"
#__email__ = "peahive@gmail.com"
#__website__ = "www.peahive.github.io"
#__created__ = "2018-01-12 12:04:50"
#__lastUpdated__ = "2018-04-01 16:43:35"
'''

import json
import urllib3
urllib3.disable_warnings()

class API:

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



    '''
    Attributes:
     ------------------------------------------------------------------------------------------
    label                               GET          label in string
    Time(Unix)                          GET          time in unix
    grid_transid
    grid_date
    grid_time
    grid_uxtime
    grid_device_id
    grid_voltage
    grid_current
    grid_earth_leak
    grid_powerfactor
    grid_activePower
    grid_reactivePower
    grid_accumulated_energy
    grid_kvarh
    grid_cp_afci_arc_count_show
    grid_cp_a0_magoutput
    grid_cp_a0_rmsoutput
    grid_cp_Irms_rate
    grid_cp_dc_rate
    grid_cp_b1_rmsoutput
    grid_afe_i_a
    grid_afe_v
    grid_cp_pfci_t_high
    grid_cp_operation_status
  

     ------------------------------------------------------------------------------------------

    '''

    '''
    API3 available methods:
    1. getDeviceStatus() GET
    '''

    # ----------------------------------------------------------------------
    def getDeviceStatus(self):


        url = str(self.get_variable("url"))
        http = urllib3.PoolManager()
        r = http.request('GET', url)
        conve_json = json.loads(r.data)
        # print conve_json
        self.set_variable('grid_transid', str(conve_json['cpletrix']['records'][0][0]))
        self.set_variable('grid_date', str(conve_json['cpletrix']['records'][0][1]))
        self.set_variable('grid_time', str(conve_json['cpletrix']['records'][0][2]))
        self.set_variable('grid_uxtime', str(conve_json['cpletrix']['records'][0][3]))
        self.set_variable('grid_device_id', str(conve_json['cpletrix']['records'][0][4]))
        self.set_variable('grid_voltage', str(conve_json['cpletrix']['records'][0][5]))
        self.set_variable('grid_current', str(conve_json['cpletrix']['records'][0][6]))
        self.set_variable('grid_earth_leak', str(conve_json['cpletrix']['records'][0][7]))
        self.set_variable('grid_powerfactor', str(conve_json['cpletrix']['records'][0][8]))
        self.set_variable('grid_activePower', str(conve_json['cpletrix']['records'][0][9]))
        self.set_variable('grid_reactivePower', str(conve_json['cpletrix']['records'][0][10]))
        self.set_variable('grid_accumulated_energy', str(conve_json['cpletrix']['records'][0][11]))
        self.set_variable('grid_kvarh', str(conve_json['cpletrix']['records'][0][12]))
        self.set_variable('grid_cp_afci_arc_count_show', str(conve_json['cpletrix']['records'][0][13]))
        self.set_variable('grid_cp_a0_magoutput', str(conve_json['cpletrix']['records'][0][14]))
        self.set_variable('grid_cp_a0_rmsoutput', str(conve_json['cpletrix']['records'][0][15]))
        self.set_variable('grid_cp_Irms_rate', str(conve_json['cpletrix']['records'][0][16]))
        self.set_variable('grid_cp_dc_rate', str(conve_json['cpletrix']['records'][0][17]))
        self.set_variable('grid_cp_b1_rmsoutput', str(conve_json['cpletrix']['records'][0][18]))
        self.set_variable('grid_afe_i_a', str(conve_json['cpletrix']['records'][0][19]))
        self.set_variable('grid_afe_v', str(conve_json['cpletrix']['records'][0][20]))
        self.set_variable('grid_cp_pfci_t_high', str(conve_json['cpletrix']['records'][0][21]))
        self.set_variable('grid_cp_operation_status', str(conve_json['cpletrix']['records'][0][22]))

        print self.get_variable("type")

        self.set_variable('device_type', self.get_variable("type"))

        gridactive0 = str(conve_json['cpletrix']['records'][0][9])
        if (gridactive0 > (-30) and gridactive0 < (0)) :
            gridactive = 0
        else:
            gridactive = gridactive0
        self.set_variable('grid_activePower', gridactive)
        self.printDeviceStatus()



    def printDeviceStatus(self):

        print ("--------------------------------Creative Power status--------------------------------")
        print(" TransID(ID) = {}".format(self.get_variable('grid_transid')).upper())
        print(" Date(D) = {}".format(self.get_variable('grid_date')).upper())
        print(" Time(T) = {}".format(self.get_variable('grid_time')).upper())
        print(" UxTime(UT) = {}".format(self.get_variable('grid_uxtime')).upper())
        print(" DeviceID(DID) = {}".format(self.get_variable('grid_device_id')).upper())
        print(" Voltage(V) = {}".format(self.get_variable('grid_voltage')).upper())
        print(" Current(A) = {}".format(self.get_variable('grid_current')).upper())
        print(" EarthLeak(EL) = {}".format(self.get_variable('grid_earth_leak')).upper())
        print(" ActivePower(W) = {}".format(self.get_variable('grid_activePower')).upper())
        print(" ReactivePower(Var) = {}".format(self.get_variable('grid_reactivePower')).upper())
        print(" Powerfactor = {}".format(self.get_variable('grid_powerfactor')).upper())
        print(" AccumulatedEnergy(Wh) = {}".format(self.get_variable('grid_accumulated_energy')).upper())
        print(" Kvarh = {}".format(self.get_variable('grid_kvarh')).upper())
        print(" Show = {}".format(self.get_variable('grid_cp_afci_arc_count_show')).upper())
        print(" A0magOut = {}".format(self.get_variable('grid_cp_a0_magoutput')).upper())
        print(" A0rmsOut = {}".format(self.get_variable('grid_cp_a0_rmsoutput')).upper())
        print(" IrmsRate = {}".format(self.get_variable('grid_cp_Irms_rate')).upper())
        print(" DcRate = {}".format(self.get_variable('grid_cp_dc_rate')).upper())
        print(" B1RmsOut = {}".format(self.get_variable('grid_cp_b1_rmsoutput')).upper())
        print(" Afeia = {}".format(self.get_variable('grid_afe_i_a')).upper())
        print(" Afev = {}".format(self.get_variable('grid_afe_v')).upper())
        print(" PfcHigh = {}".format(self.get_variable('grid_cp_pfci_t_high')).upper())
        print(" OperationStatus = {}".format(self.get_variable('grid_cp_operation_status')).upper())
        print(" device_type = {}".format(self.get_variable('device_type')).upper())
        print("--------------------------------------------------------------------------------------")


def main():
    Creative_Power = API(model='e-Trix@Larm', type='powermeter', api='classAPI_CreativePower', agent_id='Creative_Power',device_id='250883398',url = 'https://cplservice.com/apixmobile.php/cpletrix?filter=device_id,eq,250883398&order=trans_id,desc&page=1')
    Creative_Power.getDeviceStatus()


if __name__ == "__main__": main()