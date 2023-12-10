import argparse
import requests
import hetzner
import sshrun
import time
import configparser
import subprocess
import sys

class ColoredText:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'
    
    def red(self, text): return self.RED + text + self.END
    def green(self, text): return self.GREEN + text + self.END
    def yellow(self, text): return self.YELLOW + text + self.END
    def blue(self, text): return self.BLUE + text + self.END
    def magenta(self, text): return self.MAGENTA + text + self.END
    def cyan(self, text): return self.CYAN + text + self.END
    def white(self, text): return self.WHITE + text + self.END
    def bold(self, text): return self.BOLD + text + self.END



config = configparser.ConfigParser()
session = requests.Session()
ct = ColoredText()

def check_config(filename, create=False):
    config = configparser.ConfigParser()
    config.read(filename)

    # "trickest" section values are always compulsory
    if not 'trickest' in config or not all([key in config['trickest'] and config['trickest'][key] for key in ['email', 'password']]):
        print(ct.red("Error: 'trickest' section or its values are missing in the config file."))
        sys.exit(1)
    
    # "hetzner" section values are compulsory if --create flag is used
    if create and (not 'hetzner' in config or not config['hetzner']['apikey']):
        print(ct.red("Error: 'hetzner' section or its 'apikey' value is missing in the config file."))
        sys.exit(1)

    print(ct.green("All necessary config values are available."))

config.read('config.ini')

def trickest(var):
    trickest_auth = "https://hive-api.trickest.io:443/token-auth/"
    headers = {"Content-Type": "application/json"}
    json={"email": config.get('trickest', 'email'), "password": config.get('trickest', 'password')}
    res = session.post(trickest_auth, headers=headers, json=json)
    res.raise_for_status()

    token = res.json()['access']

    session.headers.update({
        'Authorization': f'Bearer {token}',
    })

    userinfo = "https://hive-api.trickest.io/v1/users/me/"
    res = session.get(userinfo, headers=headers)
    vl = res.json()['profile']['vault_info']['id']

    vault = f"https://hive-api.trickest.io/v1/fleet/?vault={vl}"
    res = session.get(vault, headers=headers)

    for result in res.json()["results"]:
        if result["name"] == "Self-hosted fleet":
            fleet = result["id"]
            break
    
    if var == 1:
        fleeturl = "https://hive-api.trickest.io/v1/machine/"
        fljson = {"fleet":fleet}
        res = session.post(fleeturl, headers=headers, json=fljson)
        machine_id = res.json()['id']
        authtoken = res.json()['auth']['id']
        authsecret = res.json()['auth']['secret']

        fleet_ren = f"https://hive-api.trickest.io/v1/machine/{machine_id}/"
        jsonname = {"name":"AutoTrickster"}
        session.put(fleet_ren, headers=headers, json=jsonname)

        return authtoken, authsecret
    elif var == 0:
        fleeturl = f"https://hive-api.trickest.io/v1/machine/?fleet={fleet}"
        res = session.get(fleeturl, headers=headers)
        data = res.json()
        ids = [result['id'] for result in data['results']]
        for id in ids:
            fleetdel = f"https://hive-api.trickest.io/v1/machine/{id}/"
            session.delete(fleetdel, headers=headers)

def makehetzner(region,size,num):
    name=f"AutoTrickster-{num}"
    print(ct.blue(f"\nCreating {name}"))
    ip, pwd, ID = hetzner.create_server(region,name,size)
    token, secret = trickest(1)
    print(ct.green("Checking for server status..."))
    if (sshrun.is_ssh_ready(ip,"root",pwd)):
        time.sleep(10)
        newpwd = hetzner.reset_pwd(ID)
        time.sleep(5)
        print(ct.green("Installing and running Trickest agent..."))
        sshrun.doit(ip,"root",newpwd,token,secret)

def main():
    parser = argparse.ArgumentParser(description='Manage Trickest Community Machines.')
    parser.add_argument('--create', action='store_true', help='Create and add cloud instances to Trickest fleets.')
    parser.add_argument('--delete', action='store_true', help='Delete and remove instances from Trickest Fleets')
    parser.add_argument('--this', action='store_true', help='Use the current machine as a fleet for Trickest Community')

    args = parser.parse_args()

    print('''
  ___        _      _____    _      _        _            
 / _ \      | |    |_   _|  (_)    | |      | |           
/ /_\ \_   _| |_ ___ | |_ __ _  ___| | _____| |_ ___ _ __ 
|  _  | | | | __/ _ \| | '__| |/ __| |/ / __| __/ _ \ '__|
| | | | |_| | || (_) | | |  | | (__|   <\__ \ ||  __/ |   
\_| |_/\__,_|\__\___/\_/_|  |_|\___|_|\_\___/\__\___|_|   
''')
    
    check_config('config.ini')
    if not any(vars(args).values()):
        print(ct.red("Please enter atleast one of the supported arguments."))
        parser.print_help()

    if args.create:
        check_config('config.ini', args.create)
        machine = input("Enter the number of machines(Max 3): ")
        print(ct.blue("Available regions: "), hetzner.list_regions())
        print(ct.blue("Available server types: "), hetzner.list_server_types())

        region = input(ct.bold("\nEnter the region (default 'nbg1'): ")) or 'nbg1'
        server_type = input(ct.bold("Enter the server type (default 'cpx11'): ")) or 'cpx11'
        for i in range(int(machine)):
            makehetzner(region, server_type, i)
    elif args.delete:
        print(ct.green("Deleting all Trickest fleets..."))
        trickest(0)
        print(ct.green("Deleting Hetzner instances..."))
        hetzner.delete_servers()
    elif args.this:
        token, secret = trickest(1)
        command = f'export TRICKEST_CLIENT_AUTH_ID="{token}" && export TRICKEST_CLIENT_AUTH_SECRET="{secret}" && curl curl https://trickest.io/download/agent/latest/init -so init.sh && chmod +x init.sh && ./init.sh'
        subprocess.call(command, shell=True)


main()