#!/usr/bin/env python
from ncclient import manager
from ncclient.operations import RPCError
import xmltodict
import yaml
from pprint import pprint
if __name__ == '__main__':
    # get parameters from yaml file
    with open('hosts.yaml') as f:
        hosts = yaml.load(f, Loader=yaml.FullLoader)
    # iterate onto the list
    for host in hosts:
        # connect to netconf agent
        with manager.connect(host=host['host'],
                             port=host['port'],
                             username=host['username'],
                             password=host['password'],
                             timeout=90,
                             hostkey_verify=False,
                             device_params={'name': host['name']}) as m:
            # execute netconf operation
            try:
                # get Python dict information from rpc expression filter
                response = m.get(host['payloads']['expression'].format(
                    interface_name='eth1/1'))
                python_dict = xmltodict.parse(response.xml)[
                    'rpc-reply']['data']
                pprint(python_dict)
            except RPCError as e:
                print(e._raw)
