''' box - connect.py '''

import subprocess

from box.command import Command
from box.status import HostStatus

import box
from box import  error

class Connect(Command, HostStatus):
    ''' Contains SSH handlers. '''

    def __init__(self, host_port=None, command=None):
        super().__init__(command)
        self.port = host_port
        self.stdout = None
        self.stderr = None

    # run_command (rename)
    def connect(self, ssh_command):
        '''
        Contains the functionality to connect to a remote host via SSH.
        '''
        script = [
                'ssh',
                '-i', f'{box.key_path}',
                '-o', 'StrictHostKeyChecking=no',
                '-p', f'{self.port}',
                f'{box.host_user}@{box.host_ip}',
                f'{ssh_command}'
            ]

        result = subprocess.run(script,  check=True, capture_output=True)
        self.stdout = result.stdout
        self.stderr = result.stderr
        # with Popen(script, stdout=PIPE, stderr=PIPE) as process:
            # self.stdout, self.stderr = process.communicate()

        if self.stderr:
            raise error.SSHError(self.stderr)

        return (self.stdout, self.stderr)
