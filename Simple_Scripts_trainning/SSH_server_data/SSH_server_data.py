import paramiko
import subprocess

#pprint makes output cleaner
from pprint import PrettyPrinter

printer = PrettyPrinter()
servers=['l-fwdev-071', 'l-fwdev-072', 'l-fwdev-073']
servers_data=list()

# Define the SSH connection details
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
for server in servers:   
    ssh.connect(hostname=server, username='root', password='3tango',port=22, timeout=2)
    # Define the command to be executed
    command = 'mst status -v /'
    # Execute the command and capture the output
    stdin, stdout, stderr = ssh.exec_command(command,get_pty=True)
    for line in iter(stdout.readline, ""):
        print(line, end="")
        # servers_data.append(output,end='')
        # output = stdout.read().decode('utf-8')
        # servers_data.append(output)

    # Close the SSH connection
    ssh.close()

# print("Servers data = {}".format(servers_data))



