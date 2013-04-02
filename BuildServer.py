import sys
import paramiko
from novaclient.v1_1 import client


class BuildServer:

    def __init__(self, user='demo', password='1234',
                 project_id='demo', auth_url='http://127.0.0.1:5000/v2.0'):
        self.name = ''
        self.user = user
        self.password = password
        self.project_id = project_id
        self.auth_url = auth_url
        self.build = False
        self.ip = None

    def create(self, name='unnamed', flavor='512',
               image='cirros-0.3.1-x86_64-uec', pkey='last_key'):
        nova = client.Client(self.user, self.password,
                             project_id=self.project_id,
                             auth_url=self.auth_url)

        flavor = nova.flavors.find(ram=int(flavor))
        image = nova.images.find(name=image)
        self.name = name

        nova.servers.create(name, image, flavor=flavor, key_name=pkey)

        while nova.servers.find(name=name).status == "BUILD":
            pass
        if nova.servers.find(name=name).status == "ACTIVE":
            ip = nova.servers.find(name=name).addresses['private'][0]['addr']
            self.ip = ''.join(ip)
            self.build = True
            return 0
        else:
            seld.build = False
            return 1

    def commands(self, command='echo "Hello, world!"'):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if not self.build:
            ssh.close()
            return "Server isn't build.", 1
        try:
            ssh.connect(hostname=self.ip, username='cirros',
                        key_filename='last_key')
            stdin, stdout, stderr = ssh.exec_command(command)
            out = ''
            for line in stdout:
                out = out + '... ' + line.strip('\n')
            ssh.close()
            return out, 0
        except:
            ssh.close()
            return "Host isn't available", 1

    def delete(self):
        nova = client.Client(self.user, self.password,
                             project_id=self.project_id,
                             auth_url=self.auth_url)
        try:
            nova.servers.delete(nova.servers.find(name=self.name))
            return 0
        except:
            return 1
