''' Used to send commands to the host. '''

from box.ssh_utils import connect

from box import error

class Command:
    ''' Executes commands on the host. '''

    def __init__(self, command=None):
        self.command = command
        self.stdout = None
        self.stderr = None

        if command is not None:
            self.stdout, self.stderr = connect(
                                            ssh_command = self.command
                                        )
            if stderr:
                raise error.SSHError(self.stderr)

            return self.stdout

    @staticmethod
    def list_directory(directory):
        '''
        Lists the contents of a directory on the host.
        '''
        stdout, stderr = connect(
                                    ssh_command = f'ls {directory}'
                                    )
        if stderr:
            raise error.SSHError(stderr)

        return stdout

    @staticmethod
    def download_file(file_url, file_path, file_name=None):
        '''
        Downloads a file to the host from a given URL to a given path.
        '''
        stdout, stderr = connect(
            ssh_command = f'curl {file_url} --output {file_path}{file_name} &',
        )

        if stderr:
            raise error.SSHError(stderr)

        return stdout
