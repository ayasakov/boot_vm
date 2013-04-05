import sys

import paramiko
from novaclient import exceptions
from novaclient.v1_1 import client


class ExecuteCommand:

    def __init__(self, user='demo', password='1234',
                 project_id='demo', auth_url='http://127.0.0.1:5000/v2.0'):
        self.user = user
        self.password = password
        self.project_id = project_id
        self.auth_url = auth_url
        self.ip = None

    def exe(self, flv, img, cmd):
        nova = client.Client(self.user, self.password,
                             project_id=self.project_id,
                             auth_url=self.auth_url)
        try:
            nova.authenticate()
        except exceptions.Unauthorized:
            print "Unauthorized"
            return None, 1
        found = None
        server = None
        try:
            flavor = nova.flavors.find(ram=int(flv))
            image = nova.images.find(name=img)
        except exceptions.NotFound:
            found = False
        else:
            for srv in nova.servers.list():
                if (srv.image['id'] == image.id and
                   srv.flavor['id'] == flavor.id):
                    found = True
                    server = srv
                    break
        if not found:
            try:
                server = nova.servers.create('name', image,
                                              flavor=flavor,
                                              key_name='last_key')
                while nova.servers.find(name='name').status == "BUILD":
                    pass
            except:
                print "Server isn't build"
                return None, 1
        self.ip = ''.join(server.addresses['private'][0]['addr'])
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(hostname=self.ip, username='cirros',
                        key_filename='last_key')
            stdin, stdout, stderr = ssh.exec_command(cmd)
            out = ''
            for line in stdout:
                out = out + '... ' + line.strip('\n')
            ssh.close()
            return out, 0
        except:
            ssh.close()
            return "Host isn't available", 1
