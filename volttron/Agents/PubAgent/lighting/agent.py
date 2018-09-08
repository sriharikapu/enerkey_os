# -*- coding: utf-8 -*-
from __future__ import absolute_import
import logging
import sys
from volttron.platform.vip.agent import Agent, Core, PubSub
from volttron.platform.agent import utils
import importlib
import json
import os, sys
from os.path import expanduser

utils.setup_logging()
_log = logging.getLogger(__name__)
__version__ = '3.2'
DEFAULT_HEARTBEAT_PERIOD = 20
DEFAULT_MONITORING_TIME = 20
DEFAULT_MESSAGE = 'HELLO'


# Step1: Agent Initialization
def lighting_agent(config_path, **kwargs):
    config = utils.load_config(config_path)
    def get_config(name):
        try:
            kwargs.pop(name)
        except KeyError:
            return config.get(name, '')

    agent_id = get_config('agent_id')
    message = get_config('message')
    model = get_config('model')
    api = get_config('api')
    identifiable = get_config('identifiable')
    # construct _topic_Agent_UI based on data obtained from DB
    topic_device_control = '/ui/agent/update/'+agent_id
    send_notification = True

    class LightingAgent(Agent):
        """Listens to everything and publishes a heartbeat according to the
        heartbeat period specified in the settings module.
        """

        def __init__(self, config_path, **kwargs):
            super(LightingAgent, self).__init__(**kwargs)
            self.config = utils.load_config(config_path)
            self._agent_id = agent_id
            self._message = message
            self.model = model
            # initialize device object
            self.apiLib = importlib.import_module("DeviceAPI.classAPI." + api)
            self.Light = self.apiLib.API(model=self.model, agent_id=self._agent_id)

        @Core.receiver('onsetup')
        def onsetup(self, sender, **kwargs):
            # Demonstrate accessing a value from the config file
            _log.info(self.config.get('message', DEFAULT_MESSAGE))

        @Core.receiver('onstart')
        def onstart(self, sender, **kwargs):
            import os
            _log.debug("VERSION IS: {}".format(self.core.version()))
            for ind in range(101, 201):
                print('Build Agent ...')
                self.build_agent(ind)

        def build_agent(self, index):
            print(' >>> Build Agent Process')
            #  get PATH Environment
            home_path = expanduser("~")
            json_path = '/workspace/hive_os/volttron/Agents/ChildAgent/pub002.config.json'
            self.control_path = home_path+json_path
            launcher = json.load(open(home_path + json_path, 'r'))  # load config.json to variable
            #  Update new agentID to variable (agentID is relate to automation_id)
            launcher.update({'agentid': 'childagent_{}'.format(index)})
            #  dump new config to file
            json.dump(launcher, open(home_path + json_path, 'w'), sort_keys=True, indent=4)
            print(" >>> Change config file successful")

            os.system("volttron-pkg package /home/peahive/workspace/hive_os/volttron/Agents/ChildAgent;" +
                      "volttron-pkg configure /home/peahive/.volttron/packaged/childagent-0.1-py2-none-any.whl" +
                      " /home/peahive/workspace/hive_os/volttron/Agents/ChildAgent/pub002.config.json" +
                      ";volttron-ctl install " +
                      "/home/peahive/.volttron/packaged/childagent-0.1-py2-none-any.whl " +
                      "--tag childagent_{}".format(index) +
                      ";volttron-ctl enable --tag childagent_{}".format(index) +
                      ";volttron-ctl start --tag childagent_{}".format(index))

    Agent.__name__ = '02ORV_InwallLightingAgent'
    return LightingAgent(config_path, **kwargs)


def main(argv=sys.argv):
    '''Main method called by the eggsecutable.'''
    try:
        utils.vip_main(lighting_agent, version=__version__)
    except Exception as e:
        _log.exception('unhandled exception')


if __name__ == '__main__':
    # Entry point for script
    sys.exit(main())
