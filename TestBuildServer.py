import BuildServer


class TestBuildServer:

    def __init__(self):
        self.server = BuildServer()
        self.names = ['new_name1', 'new_name2', 'new_name3']

    def test_create(self):
        self.server.create(name=self.names[0])
        self.server.create(name=self.names[1], flavor='1024')
        self.server.create(name=self.names[2],
                           image='cirros-0.3.1-x86_64-uec-kernel')

    def test_commands(self):
        self.server.create()
        (output, ret) = self.server.commands(command='ls')
        (output, ret) = self.server.commands(command='echo "Hello, world"')
        (output, ret) = self.server.commands(command='mkdir "test"')
        (output, ret) = self.server.commands(command='ls -l')
        (output, ret) = self.server.commands(command='cd test')
        (output, ret) = self.server.commands(command='ls -l')
        (output, ret) = self.server.commands(command='cd')
        (output, ret) = self.server.commands(command='rm test')

    def test_delete(self):
        for i in enumerate(self.names):
            self.server.delete(name=self.names[i])
