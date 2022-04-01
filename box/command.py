# pylint: disable=E1101

''' Used to send commands to the host. '''

# "Recipies"
class Command:
    ''' Executes commands on the host. '''

    def __init__(self, command=None):
        # super().__init__()
        self.command = command

        if command is not None:
            self.connect(
                ssh_command = self.command
            )


    def list_directory(self, directory):
        '''
        Lists the contents of a directory on the host.
        '''

        # ls -1 {directory}
        self.connect(
            ssh_command = f'sudo ls {directory}'
        )
        return self.stdout

    def download_file(self, file_url, file_path, file_name=None):
        '''
        Downloads a file to the host from a given URL to a given path.
        '''
        self.connect(
            ssh_command = f'sudo curl --silent {file_url} --output {file_path}{file_name} &',
        )
        return self.stdout
