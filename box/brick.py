''' box - brick.py '''

import yaml
import time

from box import Connect

class BRICK_CONFIG:
    ''' Contains the definitions of a virtual machine instance.'''

    # ------------------------------- VM Properties ------------------------------ #

    HOST_PORT = None
    BASE_IMAGE = None
    DISk_SIZE = None    # Units in Gigabytes (G)
    MEMORY = None       # Units in megabytes, no units
    CPU_QTY = None      # Number of virtual CPUs

    # ------------------------- Clound Init Configuration ------------------------ #

    META_DATA = {}

    USER_DATA = {
        "users":[
            {
                "name": "root",
                "plain_text_passwd": "root",
            },
        ],
    }

    VENDOR_DATA = {
        "runcmd": [

            "domain_uuid=$(sudo dmidecode -s system-uuid)",

            "sudo mkdir -p /etc/sshtunnel",

            'sudo ssh-keygen -qN "" -f /etc/sshtunnel/id_rsa',

            "pub_key=$(cat /etc/sshtunnel/id_rsa.pub)",

            '''available_port=$(curl -H "Content-Type: application/x-www-form-urlencoded; charset=utf-8" \
                --data-urlencode "pub_key=$pub_key" \
                -d "domain_uuid=$domain_uuid" \
                -X POST "https://$url/vm/tunnel/")""",

            """cat <<EOF > /etc/systemd/system/sshtunnel.service
            [Unit]
            Description=Service to maintain an ssh reverse tunnel
            Wants=network-online.target
            After=network-online.target
            StartLimitIntervalSec=0
            [Service]
            Type=simple
            ExecStart=/usr/bin/ssh -qNn \\
            -o ServerAliveInterval=30 \\
            -o ServerAliveCountMax=3 \\
            -o ExitOnForwardFailure=yes \\
            -o StrictHostKeyChecking=no \\
            -o UserKnownHostsFile=/dev/null \\
            -i /etc/sshtunnel/id_rsa \\
            -R :$available_port:localhost:22 \\
            sshtunnel@$ip -p 22
            Restart=always
            RestartSec=60
            [Install]
            WantedBy=multi-user.target
            EOF''',

            "sudo systemctl enable --now sshtunnel",

            "sudo systemctl daemon-reload"
        ],
    }

class Brick(BRICK_CONFIG):
    ''' All the functions that can be done to a VM. '''

    def __init__(self, brick_id=None, host_port=None):
        self.brick_id = brick_id
        self.HOST_PORT = host_port

    # ---------------------------------- Create ---------------------------------- #
    def create(self, base_image=None, disk_size=25, memory=12288, cpu_qty=4):
        '''
        Creates a new VM using the configuration provided.
        '''
        self.DISk_SIZE = disk_size
        self.BASE_IMAGE = base_image
        self.MEMORY = memory
        self.CPU_QTY = cpu_qty

        host = Connect(host_port=self.HOST_PORT)

        # Create Brick Folder
        host.connect(
            ssh_command = f'sudo mkdir /var/lib/libvirt/images/{self.brick_id}'
        )

        # Create the VM disk image
        host.connect(
        ssh_command = f'sudo qemu-img create -b /var/lib/libvirt/images/{self.BASE_IMAGE}.img -f qcow2 -F qcow2 /var/lib/libvirt/images/{self.brick_id}.img {self.DISk_SIZE}G'
        )

        # Generate the user-data file on the host
        host.connect(
            ssh_command = f"sudo bash -c 'echo \"#cloud-config\n\n{yaml.dump(self.USER_DATA)}\" > /var/lib/libvirt/images/{self.brick_id}/user-data'"
        )

        # Add VENDOR-DATA to the host image
        self.VENDOR_DATA['runcmd'].insert(0,"url='dev.brickbox.io'")
        self.VENDOR_DATA['runcmd'].insert(0,"ip='134.209.214.111'")
        host.connect(
            ssh_command = f"sudo bash -c 'echo \"#cloud-config\n\n{yaml.dump(self.VENDOR_DATA)}\" > /var/lib/libvirt/images/{self.brick_id}/vendor-data'"
        )

        # Generate the meta-data file on the host
        self.META_DATA['instance-id'] = f"{self.brick_id}"
        self.META_DATA['local-hostname'] = f"brick-{self.brick_id}"

        host.connect(
            ssh_command = f"sudo bash -c 'echo \"{yaml.dump(self.META_DATA)}\" > /var/lib/libvirt/images/{self.brick_id}/meta-data'"
        )

        # Create the iso
        host.connect(
            ssh_command = f"sudo genisoimage -quiet -output /var/lib/libvirt/images/{self.brick_id}/{self.brick_id}.iso -V CIDATA -r -J /var/lib/libvirt/images/{self.brick_id}/user-data /var/lib/libvirt/images/{self.brick_id}/meta-data /var/lib/libvirt/images/{self.brick_id}/vendor-data"
        )

        # Create the VM
        host.connect(
            ssh_command = f"""sudo virt-install \
                                --name={self.brick_id} \
                                --virt-type=kvm \
                                --ram={self.MEMORY} \
                                --cpu=host \
                                --vcpus={self.CPU_QTY} \
                                --import --disk path=/var/lib/libvirt/images/{self.brick_id}.img,format=qcow2 \
                                --disk path=/var/lib/libvirt/images/{self.brick_id}/{self.brick_id}.iso,device=cdrom \
                                --os-variant=ubuntu20.04 \
                                --network bridge=br0,model=virtio \
                                --graphics=none \
                                --noautoconsole \
                                --boot menu=on \
                                --autostart
                            """
        )


    # ------------------------------- Toggle State ------------------------------- #
    def toggle_state(self, set_state=None):
        '''
        Called to toggle the current state. If on, turn off. If off, turn on.
        If the state is set to "on" or "off" that state is enforced.
        '''
        host = Connect(host_port=self.HOST_PORT)

        if set_state == "on" and not self.is_running():
            host.connect(
                ssh_command = f"sudo virsh autostart {self.brick_id} && sudo virsh start {self.brick_id}"
            )

        if set_state == "off" and self.is_running():
            host.connect(
                ssh_command = f"sudo virsh shutdown {self.brick_id} && sudo virsh autostart {self.brick_id} --disable"
            )


    # ---------------------------------- Reboot ---------------------------------- #
    def reboot(self):
        '''
        Called to reboot the VM.
        '''
        host = Connect(host_port=self.HOST_PORT)
        host.connect(
            ssh_command = f"sudo virsh reboot {self.brick_id}"
        )


    # ---------------------------------- Destroy --------------------------------- #
    def destroy(self):
        '''
        Called to destry and delete the VM and assosiated files.
        '''
        host = Connect(host_port=self.HOST_PORT)

        # Teminate the VM
        host.connect(
            ssh_command = f"sudo virsh shutdown {self.brick_id} && sudo virsh destroy {self.brick_id} && sudo virsh undefine {self.brick_id}"
        )

        # File cleanup
        host.connect(
            ssh_command = f"sudo rm -r /var/lib/libvirt/images/{self.brick_id} && sudo find /var/lib/libvirt/images/ -name '{self.brick_id}*' -delete"
        )


    def set_root_password(self, passord='root'):
        '''
        Called to set the root password, it will turn off the VM first then set the password.
        '''
        host = Connect(host_port=self.HOST_PORT)

        self.toggle_state(set_state="off")

        time.sleep(5)

        host.connect(
            ssh_command = f"sudo virt-customize -a /var/lib/libvirt/images/{self.brick_id}.img --root-password password:root"
        )

        self.toggle_state(set_state="on")



    def is_running(self):
        '''
        Returns True if VM is running, otherwise false.
        '''
        host = Connect(host_port=self.HOST_PORT)

        host.connect(
            ssh_command = f'[[ $(sudo virsh domstate {self.brick_id}) == "running" ]] && echo Running || echo Not Running'
        )

        return bool(host.stdout.decode('utf-8').replace("'", '').rstrip("\n") == 'Running')
