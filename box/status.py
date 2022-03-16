''' box - status.py '''

class HostStatus:
    '''
    Returns a summary of a host and its operational status.
    Each verification reports back its current status.
    '''
    def is_ready(self, auto_fix=True):
        '''
        Cycles through each of the verifications individually then return True if all pass.
        '''
        stats = [
            self.qemu_installed(auto_fix = auto_fix),
            self.vfio_pci_bind_exists(auto_fix = auto_fix),
            self.vfio_pci_bind_executable(auto_fix = auto_fix),
            self.br0_exists(auto_fix = auto_fix),
            self.enp3s0f1_is_up(auto_fix = auto_fix),
            self.br0_is_networked(auto_fix = auto_fix),
        ]
        return bool(False not in stats)


    def qemu_installed(self, auto_fix=False):
        '''
        Verifies is QEMU is instlled.
        '''
        # Verify
        self.connect(
            ssh_command = '[[ -f /usr/bin/qemu-system-x86_64 ]] && echo Exists || echo DNE'
        )
        insalled = bool(self.stdout.decode('utf-8').replace("'", '').rstrip("\n") == 'Exists')

        #Fix
        if not insalled and auto_fix:
            self.connect(
                ssh_command = 'sudo apt-get install qemu-kvm qemu-utils libvirt-daemon-system libvirt-clients bridge-utils virt-manager ovmf libguestfs-tools -y'
            )
            return self.qemu_installed()

        return insalled


    def vfio_pci_bind_exists(self, auto_fix=False):
        '''
        Check if pci binding tool directory exists.
        '''
        # Verify
        self.connect(
            ssh_command = '[[ -d /home/bb_root/vfio-pci-bind/ ]] && echo Exists || echo DNE'
        )
        exists = bool(self.stdout.decode('utf-8').replace("'", '').rstrip("\n") == 'Exists')

        # Fix
        if not exists and auto_fix:
            self.connect(
                ssh_command = 'sudo git clone https://github.com/andre-richter/vfio-pci-bind.git /home/bb_root/'
            )
            return self.vfio_pci_bind_exists()

        return exists


    def vfio_pci_bind_executable(self, auto_fix=False):
        '''
        Check if pci binding tool directory exists.
        '''
        # Verify
        self.connect(
            ssh_command = '[[ -x /home/bb_root/vfio-pci-bind/vfio-pci-bind.sh ]] && echo Executable || echo DNE'
        )
        is_executable = bool(self.stdout.decode('utf-8').replace("'", '').rstrip("\n") == 'Executable')

        # Fix
        if not is_executable and auto_fix:
            self.connect(
                ssh_command = 'sudo chmod +x /home/bb_root/vfio-pci-bind/vfio-pci-bind.sh'
            )
            return self.vfio_pci_bind_executable()

        return is_executable


    def br0_exists(self, auto_fix=False):
        '''
        Check if br0 exists.
        '''
        # Verify
        self.connect(
            ssh_command = '[[ -d /sys/class/net/br0 ]] && echo Exists || echo DNE'
        )
        exists = bool(self.stdout.decode('utf-8').replace("'", '').rstrip("\n") == 'Exists')

        # Fix
        if not exists and auto_fix:
            self.connect(
                ssh_command = 'sudo ip link add name br0 type bridge && sudo ip link set dev br0 up && sudo ip link set dev enp3s0f1 master br0'
            )
            return self.br0_exists()

        return exists


    def enp3s0f1_is_up(self, auto_fix=False):
        '''
        Verifies that the enp3s0f1 adapter is up.
        '''
        # Verify
        self.connect(
            ssh_command = '[[ $(ip -f inet addr show enp3s0f1) ]] && echo UP || echo DOWN'
        )
        is_up =  bool(self.stdout.decode('utf-8').replace("'", '').rstrip("\n") == 'UP')

        # Fix
        if not is_up and auto_fix:
            self.connect(
                ssh_command = 'sudo ip link set dev enp3s0f1 up && sudo dhclient -r enp3s0f1 && sudo dhclient enp3s0f1'
            )
            self.connect(
                ssh_command = 'sudo ip route del default dev enp3s0f1'
            )
            return self.enp3s0f1_is_up()

        return is_up


    def br0_is_networked(self, auto_fix=False):
        '''
        Verify that br0 has an IP address.
        '''
        # Verify
        self.connect(
            ssh_command = '[[ $(ip -f inet addr show br0) ]] && echo Assigned || echo Not Assigned'
        )
        is_networked = bool(self.stdout.decode('utf-8').replace("'", '').rstrip("\n") == 'Assigned')

        # Fix
        if not is_networked and auto_fix:
            self.connect(
                'sudo dhclient -r br0 && sudo dhclient br0'
            )
            return self.br0_is_networked()

        return is_networked
