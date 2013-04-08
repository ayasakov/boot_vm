import unittest

from mock import patch, Mock

from buildserver import BuildServer


class TestBuildServer(unittest.TestCase):

    mock_file = Mock()

    @patch.object(BuildServer, 'create')
    def test_create(self, mock_file):
        mock_file.return_value = 0
        bs = BuildServer()
        result = bs.create()
        self.assertEquals(result, 0)
        result = bs.create(name='name1', flavor='1024')
        self.assertEquals(result, 0)
        result = bs.create(name='name2',
                           image='cirros-0.3.1-x86_64-uec-kernel')
        self.assertEquals(result, 0)

    @patch.object(BuildServer, 'commands')
    def test_commands(self, mock_file):
        mock_file.return_value = 0
        bs = BuildServer()
        out, ret = bs.commands()
        self.assertEquals(ret, 0)
        out, ret = bs.commands(command='mkdir "test"')
        self.assertEquals(ret, 0)
        out, ret = bs.commands(command='ls -l')
        self.assertEquals(ret, 0)

    @patch.object(BuildServer, 'delete')
    def test_delete(self, mock_file):
        mock_file.return_value = 0
        bs = BuildServer()
        ret = bs.delete()
        self.assertEquals(ret, 0)

if __name__ == "__main__":
    unittest.main()
