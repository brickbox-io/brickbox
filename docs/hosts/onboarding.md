# Adding New Hosts

To add a new host to brickbox.io they need to be registered as a host. The host serial number is required and can be found by running the following on hte host:

```bash
dmidecode -s system-serial-number
```

After the host is registered use the [mason](https://github.com/brickbox-io/mason) script to begin the onboarding process:

```bash
sudo wget -qO- mason.brickbox.io | bash /dev/stdin
```

When the script as finished restart the host then enable it on the admin dashboard.
