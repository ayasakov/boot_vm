import unittest

import paramiko
from mock import patch, Mock
from novaclient import exceptions
from novaclient.v1_1 import client

from executecommand import ExecuteCommand


class TestExecuteCommand(unittest.TestCase):

    mock_file1 = Mock()
    mock_file2 = Mock()
    mock_file3 = Mock()

    @patch.object(client, 'Client')
    def test_if_client_not_authorized(self, mock_file1):
        client.Client.side_effect = KeyError(exceptions.Unauthorized)
        execommand = ExecuteCommand()
        (out, ret) = execommand.exe(flv='512', img='cirros-0.3.1-x86_64-uec',
                            cmd='echo "Hello"')
        self.assertEqual(out, "Unauthorized")

    @patch.object(client, 'flavors')
    @patch.object(client, 'images')
    def test_if_server_not_found_and_not_build(self, mock_file1, mock_file2):
        client.flavors.find.side_effect = KeyError('exceptions.NotFound')
        client.images.find.side_effect = KeyError('exceptions.NotFound')
        execommand = ExecuteCommand()
        (out, ret) = execommand.exe(flv='512', img='cirros-0.3.1-x86_64-uec',
                            cmd='echo "Hello"')
        self.assertEqual(out, "Server isn't build")

    @patch.object(client, 'flavors')
    @patch.object(client, 'images')
    @patch.object(client, 'servers')
    def test_if_server_not_found_and_build(self, mock_file1,
                                           mock_file2, mock_file3):
        client.flavors.find.side_effect = KeyError('exceptions.NotFound')
        client.images.find.side_effect = KeyError('exceptions.NotFound')
        execommand = ExecuteCommand()
        (out, ret) = execommand.exe(flv='512', img='cirros-0.3.1-x86_64-uec',
                            cmd='echo "Hello"')
        self.assertEqual(out, "Host isn't available")

    @patch.object(paramiko, 'SSHClient')
    def test_if_server_found_and_not_connection(self, mock_file1):
        paramiko.SSHClient.connect.side_effect = KeyError('foo')
        execommand = ExecuteCommand()
        (out, ret) = execommand.exe(flv='512', img='cirros-0.3.1-x86_64-uec',
                            cmd='echo "Hello"')
        self.assertEqual(out, "Host isn't available")

    def test_if_server_found_and_connection(self):
        execommand = ExecuteCommand()
        (out, ret) = execommand.exe(flv='512', img='cirros-0.3.1-x86_64-uec',
                            cmd='echo "Hello"')
        self.assertEqual(ret, 0)

if __name__ == "__main__":
    unittest.main()
