# pylint: disable=C0103, C0413, R0401

''' Called when needed to communicate with hosts.'''

host_ip = 'localhost'
host_user = 'bb_root'
key_path = f'/opt/brickbox/bb_vm/keys/{host_user}'

from box.command import Command

from box.connect import Connect

from box.brick import Brick
