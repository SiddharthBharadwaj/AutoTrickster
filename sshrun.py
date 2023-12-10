import paramiko
import time
import socket

class SilentMissingHostKeyPolicy(paramiko.MissingHostKeyPolicy):
    def missing_host_key(self, client, hostname, key):
        # No action to be taken when a host key is missing
        pass

# Create a new SSH client
client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(SilentMissingHostKeyPolicy())


def is_ssh_ready(ip, username, password, max_retries=10):
    retries = 0
    while retries < max_retries:
        try:
            client.connect(ip, username=username, password=password)
            client.close()  # Don't forget to close the connection when you're done
            return True
        except (paramiko.AuthenticationException, paramiko.SSHException, socket.error) as e:
            print(f"Waiting for SSH to be ready... (Attempt: {retries+1}/{max_retries})")
            time.sleep(5)
            retries += 1


def doit(ip,username,pwd,token,secret):
    command = f'export TRICKEST_CLIENT_AUTH_ID="{token}" && export TRICKEST_CLIENT_AUTH_SECRET="{secret}" && curl https://gist.githubusercontent.com/SiddharthBharadwaj/d18ed034d9fe36bef26cb1f209bacae1/raw/trickest-agent.sh -so init.sh && chmod +x init.sh && ./init.sh'
    while True:
        try:
            # Establish connection
            client.connect(ip, username=username, password=pwd)
            print(f"Executing command: {command}")
            stdin, stdout, stderr = client.exec_command(command)
            
            # Print command output in real-time
            for line in iter(lambda: stdout.readline(2048), ""):
                stripped_line = line.strip()
                print(stripped_line)
            client.close()
            break
        except paramiko.ssh_exception.NoValidConnectionsError as e:
            print("Will retry in 5 seconds.")
            time.sleep(5)  # delay for 5 seconds before retrying
        except paramiko.AuthenticationException:
            print("Authentication failed, retrying...")
            time.sleep(1)  # delay for 1 second
        except paramiko.SSHException as e:
            print("Unable to establish SSH connection: ", e)
            time.sleep(1) 
        except paramiko.BadHostKeyException as e:
            print("Unable to verify server's host key:", e)
            # don't retry for host key exception