# pylint: disable=C0103, C0413

''' Called when needed to communicate with hosts.'''

host_ip = 'localhost'
host_port = None
host_user = 'bb_root'
key_path = f'/opt/brickbox/bb_vm/keys/{host_user}'

from .command import Command
