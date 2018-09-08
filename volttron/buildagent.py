def launch_agent(self, dir, launch_file):
    def is_agent_installed(agent_id):
        statusreply = subprocess.check_output('~/workspace/bemoss_os/env/bin/volttron-ctl status', shell=True)
        statusreply = statusreply.split('\n')
        agent_installed = False
        reg_search_term = " " + agent_id + " "
        for line in statusreply:
            # print(line, end='') #write to a next file name outfile
            match = re.search(reg_search_term, line)
            if match:  # The agent for this device is running
                agent_installed = True
            else:
                pass
        infile.close()
        return agent_installed

    _launch_file = os.path.join(dir, launch_file + ".launch.json")

    with open(_launch_file, 'r') as infile:
        data = json.load(infile)
        agent_id = str(data['agent_id'])
        agentname = str(data["type"])
    os.chdir(os.path.expanduser("~/workspace/bemoss_os"))
    if not is_agent_installed(agent_id):
        print'launch_agent'
        print agent_id
        print agentname
        print str(_launch_file)

        os.system(  # ". env/bin/activate"
            "volttron-ctl stop --tag " + agent_id +
            ";volttron-pkg configure /tmp/volttron_wheels/" + agentname + "agent-0.1-py2-none-any.whl " + str(
                _launch_file) +
            ";volttron-ctl install " + agent_id + "=/tmp/volttron_wheels/" + agentname + "agent-0.1-py2-none-any.whl" +
            ";volttron-ctl start --tag " + agent_id +
            ";volttron-ctl status")
    else:
        os.system(  # ". env/bin/activate"
            "volttron-ctl stop --tag " + agent_id +
            ";volttron-ctl start --tag " + agent_id +
            ";volttron-ctl status")

    print "Discovery Agent has successfully launched {} located in {}".format(agent_id, dir)