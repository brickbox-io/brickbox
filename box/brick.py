''' box - brick.py '''
# pylint disable=R0902

import time
import subprocess
import yaml

from box import Connect
from box import  error

class Brick:
    ''' All the functions that can be done to a VM. '''

    # ------------------------------- VM Properties ------------------------------ #

    port = None
    base_image = None
    disk_size = None    # Units in Gigabytes (G)
    memory = None       # Units in megabytes, no units
    cpu_qty = None      # Number of virtual CPUs

    image_directory = "/var/lib/libvirt/images/"

    # ------------------------- Clound Init Configuration ------------------------ #

    META_DATA = {}

    user_data = {}

    VENDOR_DATA = {
        "packages": [
            "ubuntu-drivers-common",
            "nvidia-driver-510",
            "nvidia-utils-510"
        ],
        "runcmd": [
            [
                "curl", "https://os-imgs.nyc3.digitaloceanspaces.com/yaml/vm_init.sh",
                "--output", "/usr/local/sbin/vm_init.sh"
            ],
            [
                "chmod", "+x", "/usr/local/sbin/vm_init.sh"
            ],
            [
                "/usr/local/sbin/vm_init.sh"
            ],
            [
                "curl", "https://os-imgs.nyc3.digitaloceanspaces.com/yaml/motd.sh",
                "--output", "/usr/local/sbin/motd.sh"
            ],
            [
                "chmod", "+x", "/usr/local/sbin/motd.sh"
            ],
            [
                "/usr/local/sbin/motd.sh"
            ]
        ]
    }

    def __init__(self, brick_id=None, host_port=None):
        self.brick_id = brick_id
        self.port = host_port

    # ---------------------------------- Create ---------------------------------- #
    def create(self, base_image=None, disk_size=50, memory=12288, cpu_qty=4):
        '''
        Creates a new VM using the configuration provided.
        '''
        self.disk_size = disk_size
        self.base_image = base_image
        self.memory = memory
        self.cpu_qty = cpu_qty

        host = Connect(host_port=self.port)

        # Create Brick Folder
        host.connect(
            ssh_command = f'sudo mkdir {self.image_directory}{self.brick_id}'
        )

        # Create the VM disk image
        host.connect(
        ssh_command = f"""sudo qemu-img create \
                            -b {self.image_directory}{self.base_image}.img \
                            -f qcow2 -F qcow2 {self.image_directory}{self.brick_id}.img {self.disk_size}G
                        """
        )

        # USER-DATA
        host.connect(
            # ssh_command = f"""sudo bash -c \
            #                     'echo \"#cloud-config\n\n{yaml.dump(self.user_data)}\" \
            #                     > {self.image_directory}{self.brick_id}/user-data'
            #                 """
            ssh_command = f"""sudo bash -c \
                                'echo \"{self.user_data}\" \
                                > {self.image_directory}{self.brick_id}/user-data'
                            """
        )

        # Add VENDOR-DATA to the host image
        host.connect(
            ssh_command = f"""sudo bash -c \
                                'echo \"#cloud-config\n\n{yaml.dump(self.VENDOR_DATA)}\" \
                                > {self.image_directory}{self.brick_id}/vendor-data'
                            """
        )

        # Generate the meta-data file on the host
        self.META_DATA['instance-id'] = f"{self.brick_id}"
        self.META_DATA['local-hostname'] = f"brick-{self.brick_id}"

        host.connect(
            ssh_command = f"""sudo bash -c \
                                'echo \"{yaml.dump(self.META_DATA)}\" \
                                > {self.image_directory}{self.brick_id}/meta-data'
                            """
        )

        # Create the iso
        host.connect(
            ssh_command = f"""sudo genisoimage \
                                -quiet \
                                -output {self.image_directory}{self.brick_id}/{self.brick_id}.iso \
                                -V CIDATA -r -J {self.image_directory}{self.brick_id}/user-data \
                                {self.image_directory}{self.brick_id}/meta-data \
                                {self.image_directory}{self.brick_id}/vendor-data
                            """
        )

        # Create the VM
        host.connect(
            ssh_command = f"""sudo virt-install \
                                --name={self.brick_id} \
                                --virt-type=kvm \
                                --ram={self.memory} \
                                --cpu=host \
                                --vcpus={self.cpu_qty} \
                                --import --disk path={self.image_directory}{self.brick_id}.img,format=qcow2 \
                                --disk path={self.image_directory}{self.brick_id}/{self.brick_id}.iso,device=cdrom \
                                --os-variant=ubuntu20.04 \
                                --network bridge=br0,model=virtio \
                                --graphics=none \
                                --video=vga \
                                --noautoconsole \
                                --boot menu=on \
                                --noreboot \
                                --autostart
                            """
        )

    # -------------------------------- Attach GPU -------------------------------- #
    def attach_gpu(self, xml_data=None):
        '''
        Required: PCIE and DEVICE ID
        Mounts the GPU from the host to the VM.
        '''
        host = Connect(host_port=self.port)
        if xml_data is not None:
            host.connect(
                ssh_command = f"""sudo bash -c \
                                    'sudo echo \"{xml_data}\" \
                                    > {self.image_directory}{self.brick_id}/GPU.xml'
                                """
            )
        host.connect(
            ssh_command = f"""sudo virsh attach-device {self.brick_id} \
                                {self.image_directory}{self.brick_id}/GPU.xml --persistent
                            """
        )

    # ------------------------------- Toggle State ------------------------------- #
    def toggle_state(self, set_state=None):
        '''
        Called to toggle the current state. If on, turn off. If off, turn on.
        If the state is set to "on" or "off" that state is enforced.
        '''
        host = Connect(host_port=self.port)

        if set_state == "on" and not self.is_running():
            host.connect(
                ssh_command = f"""sudo virsh autostart {self.brick_id} \
                                    && sudo virsh start {self.brick_id}
                                """
            )

        if set_state == "off" and self.is_running():
            try:
                host.connect(
                    ssh_command = f"""sudo virsh shutdown --mode=agent {self.brick_id} \
                                        && sudo virsh autostart {self.brick_id} --disable
                                    """
                )
            except subprocess.CalledProcessError:
                host.connect(
                    ssh_command = f"""sudo virsh destroy {self.brick_id} \
                                        && sudo virsh autostart {self.brick_id} --disable
                                    """
                )


    # ---------------------------------- Reboot ---------------------------------- #
    def reboot(self):
        '''
        Called to reboot the VM.
        '''
        host = Connect(host_port=self.port)
        host.connect(
            ssh_command = f"sudo virsh reboot {self.brick_id}"
        )


    # ---------------------------------- Destroy --------------------------------- #
    def destroy(self):
        '''
        Called to destry and delete the VM and assosiated files.
        '''
        host = Connect(host_port=self.port)

        # Shutdown if running
        if self.is_running():
            host.connect(
                ssh_command = f"sudo virsh destroy {self.brick_id}"
            )

        # Teminate the VM
        host.connect(
            ssh_command = f"sudo virsh undefine {self.brick_id}"
        )

        # File cleanup
        try:
            host.connect(
                ssh_command = f"""sudo find {self.image_directory} \
                                    -name '{self.brick_id}*' \
                                    -exec rm -r {{}} \\;
                                """
            )
        except error.SSHError as err:
            print(err)
        except subprocess.CalledProcessError as err:
            print(err)

    # ------------------------------- Root Password ------------------------------ #
    def set_root_password(self, password='root'):
        '''
        Called to set the root password, it will turn off the VM first then set the password.
        '''
        was_running = self.is_running()

        time.sleep(15)
        self.toggle_state(set_state="off")
        time.sleep(3)

        host = Connect(host_port=self.port)
        host.connect(
            ssh_command = f"""sudo virt-customize \
                                -a {self.image_directory}{self.brick_id}.img \
                                --root-password password:{password}
                            """
        )

        if was_running:
            self.toggle_state(set_state="on")

    # --------------------------------- SSH Keys --------------------------------- #
    def set_ssh_key(self, key):
        '''
        Called to add SSH keys to the VM.
        '''
        was_running = self.is_running()

        time.sleep(15)
        self.toggle_state(set_state="off")
        time.sleep(3)

        host = Connect(host_port=self.port)
        host.connect(
            ssh_command = f"sudo echo {key} | sudo tee -a ssh.key"
        )
        host.connect(
            ssh_command = f"""sudo virt-customize \
                                -a {self.image_directory}{self.brick_id}.img \
                                --ssh-inject root:file:ssh.key
                            """
        )
        host.connect(
            ssh_command = "sudo rm ssh.key"
        )

        if was_running:
            self.toggle_state(set_state="on")

    # ---------------------------------------------------------------------------- #
    #                                States and Info                               #
    # ---------------------------------------------------------------------------- #

    def img_exsists(self):
        '''
        Returns True if the VM exsists.
        '''
        host = Connect(host_port=self.port)

        host.connect(
            ssh_command = f"""[[ sudo virsh domblklist {self.brick_id} | \
                                grep "{self.image_directory}{self.brick_id}.img" ]] && \
                                echo Exists || echo DNE
                            """
        )

        return bool(host.stdout.decode('utf-8').replace("'", '').rstrip("\n") == 'Exists')


    def is_running(self):
        '''
        Returns True if VM is running, otherwise false.
        '''
        host = Connect(host_port=self.port)

        host.connect(
            ssh_command = f"""[[ $(sudo virsh domstate {self.brick_id}) == "running" ]] && \
                                echo Running || echo Not Running
                            """
        )

        return bool(host.stdout.decode('utf-8').replace("'", '').rstrip("\n") == 'Running')


    def domuuid(self):
        '''
        Returns domuuid of the VM
        '''
        host = Connect(host_port=self.port)

        host.connect(
            ssh_command = f'sudo virsh domuuid {self.brick_id}'
        )

        return host.stdout.decode('utf-8').replace("'", '').rstrip("\n")

    # ---------------------------------------------------------------------------- #
    #                                Edit Resources                                #
    # ---------------------------------------------------------------------------- #

    def add_gpu(self, xml_data=None):
        '''
        Powers off the VM, adds the GPU, then powers on the VM.
        '''
        was_running = self.is_running()

        time.sleep(15)
        self.toggle_state(set_state="off")
        time.sleep(3)

        self.attach_gpu(xml_data=xml_data)

        if was_running:
            self.toggle_state(set_state="on")
