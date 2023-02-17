import paramiko
from openpyxl import Workbook

# Define the SSH connection parameters
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
hostname = 'l-fwdev-072'
username = 'root'
password = '3tango'

# Establish the SSH connection
ssh.connect(hostname, username=username, password=password)

# Run the command(s) to collect the necessary data
stdin, stdout, stderr = ssh.exec_command('mst status -v')

# Capture the output and parse it as necessary
data = stdout.readlines()
print(data)

# Create an XLSX file and write the data to it
wb = Workbook()
ws = wb.active
for row in data:
    values = row.strip().split(',')
    ws.append(values)
wb.save('servers_data.xlsx')

# Close the SSH connection
ssh.close()
