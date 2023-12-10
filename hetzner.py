import requests
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

API_TOKEN = config.get('hetzner', 'apikey')

headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json',
}

def list_regions():
    response = requests.get('https://api.hetzner.cloud/v1/locations', headers=headers)
    regions = [item['name'] for item in response.json()['locations']]
    return regions

def list_server_types():
    response = requests.get('https://api.hetzner.cloud/v1/server_types', headers=headers)
    server_types = [item['name'] for item in response.json()['server_types']]
    return server_types

def create_server(region,name,server_type):
    data = {
        "automount": False,
        "image": "ubuntu-20.04",
        "labels": {},
        "location": region,
        "name": name,
        "server_type": server_type,
        "start_after_create": True,
        "user_data": "#cloud-config\nruncmd:\n- [touch, /root/cloud-init-worked]\n",
    }

    response = requests.post('https://api.hetzner.cloud/v1/servers', headers=headers, data=json.dumps(data))
    ID = response.json()['server']['id']
    ip = response.json()['server']['public_net']['ipv4']['ip']
    pwd = response.json()['root_password']

    return ip, pwd, ID

def reset_pwd(ID):
    url = f"https://api.hetzner.cloud/v1/servers/{ID}/actions/reset_password"
    response = requests.post(url, headers=headers)
    newpass = response.json()['root_password']
    return newpass

def delete_servers():
    response = requests.get('https://api.hetzner.cloud/v1/servers', headers=headers)
    data = response.json()

    for server in data['servers']:
        if server['name'].startswith("AutoTrickster"):
            confirm_deletion = input("Do you want to delete server {} (yes/no)? ".format(server['name'])) or 'no'

            if confirm_deletion.lower() == 'yes':
                deletion_response = requests.delete('https://api.hetzner.cloud/v1/servers/{}'.format(server['id']), headers=headers)
                print("Deleted server {}, response status: {}".format(server['name'], deletion_response.status_code))
            else:
                print("Skipping deletion for server {}".format(server['name']))
