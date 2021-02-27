import requests
import json
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
from pprint import pprint


auth_url = "https://sbx-nxos-mgmt.cisco.com/api/mo/aaaLogin.json"
auth_body = {'aaaUser': {'attributes': {
    'name': 'admin', 'pwd': 'Admin_1234!'}}}
int_url = 'https://sbx-nxos-mgmt.cisco.com/api/mo/sys/intf/phys-[eth1/33].json'
headers = {'content-type': 'application/json'}

if __name__ == '__main__':
    # disable InsecureRequestWarning
    disable_warnings(InsecureRequestWarning)
    try:
        # login and set cookie
        auth_response = requests.post(
            auth_url, json=auth_body, timeout=5, verify=False).json()
        token = auth_response['imdata'][0]['aaaLogin']['attributes']['token']
        cookies = {}
        cookies['APIC-Cookie'] = token
        # get interface information
        get_response = requests.get(
            int_url, headers=headers, cookies=cookies, verify=False).json()
        pprint(get_response)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
