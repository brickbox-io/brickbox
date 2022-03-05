''' Used to send commands to the host. '''

from box import host_ip, host_user, host_port
from box import ssh_utils

class Command:
    ''' Executes commands on the host. '''

    def __init__(self, command=None):
        self.command = command
        self.stdout = None
        self.stderr = None

        if command is not None:
            self.stdout, self.stderr = ssh_utils.connect(
                                            ssh_command = self.command
                                        )


    def list_directory(directory):
        '''
        Lists the contents of a directory on the host.
        '''
        stdout, stderr = ssh_utils.connect(
                                    ssh_command = f'ls {directory}'
                                    )
        return (stdout, stderr)


    def download_file(file_url, file_path, file_name=None):
        '''
        Downloads a file to the host from a given URL to a given path.
        '''
        stdout, stderr = ssh_utils.connect(
            ssh_command = f'curl {file_url} --output {file_path}{file_name} &',
        )
        return (stdout, stderr)
