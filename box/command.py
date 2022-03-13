''' Used to send commands to the host. '''

from box import  error

class Command:
    ''' Executes commands on the host. '''

    def __init__(self, command=None):
        self.command = command

        if command is not None:
            self.connect(
                ssh_command = self.command
            )


    def list_directory(self, directory):
        '''
        Lists the contents of a directory on the host.
        '''
        self.connect(
            ssh_command = f'sudo ls {directory}'
        )
        return self.stdout

    def download_file(self, file_url, file_path, file_name=None):
        '''
        Downloads a file to the host from a given URL to a given path.
        '''
        self.connect(
            ssh_command = f'sudo curl {file_url} --output {file_path}{file_name} &',
        )
        return self.stdout
