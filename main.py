from novaclient.v1_1 import client
import paramiko, base64
import sys

def build(user="demo", password="1234", project="demo", auth_url="http://127.0.0.1:5000/v2.0"):
    nova = client.Client(user, password, project_id=project, auth_url=auth_url)

    #---------------------------------------
    flv = nova.flavors.find(ram=512)
    name = "last_"
    #---------------------------------------

    for img in nova.images.list():
        print "Build " + name + img.name
        #nova.servers.create(name + img.name, img, flavor=flv, key_name='last_key')
        while nova.servers.find(name=name + img.name).status == "BUILD":
            pass
        if nova.servers.find(name=name + img.name).status == "ACTIVE":
            print "Server " + name + img.name + " is ready to work."
        else:
            print "Server " + name + img.name + " : ERROR."

    #print dir(nova.servers.find(name='last_cirros-0.3.1-x86_64-uec'))
    return nova.servers.list()

def connect(server_list):
    for srv in server_list:
        ip = srv.addresses['private'][0]['addr']
        sshclient = paramiko.SSHClient()
        sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #help(paramiko.SSHClient)
        try:
            sshclient.connect(hostname=ip, username='cirros', key_filename='last_key')
            stdin, stdout, stderr = sshclient.exec_command('echo "Hello world"')
            for line in stdout:
                print '... ' + line.strip('\n')
            sshclient.close()
        except:
            print ip + " isn't available"

if __name__ == "__main__":
    server_list = build()
    connect(server_list)