''' box.ssh_utils - ssh_connect.py '''

from subprocess import Popen, PIPE

import box

def connect(ssh_command):
    '''
    Contains the functionality to connect to a remote host via SSH.
    '''
    script = [
            'sudo', 'ssh',
            '-i', f'{box.key_path}',
            '-o', 'StrictHostKeyChecking=no',
            '-p', f'{box.host_port}',
            f'{box.host_user}@{box.host_ip}',
            'sudo', f'{ssh_command}'
        ]

    with Popen(script, stdout=PIPE, stderr=PIPE) as process:
        stdout, stderr = process.communicate()

    return (stdout, stderr)
