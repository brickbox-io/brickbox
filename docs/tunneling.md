# SSH Tunneling

## Server Side

1) Create a "sshtunnel" user on the server.
2) Crate the .ssh directory.
3) Provide read access of the .ssh directory to the "sshtunnel" user.
4) Chmod 700 the .ssh directory.
5) Create a file named "authorized_keys" in the .ssh directory.
6) Chmod 600 the "authorized_keys" file.
7) Change the ownership of the "authorized_keys" directory to the "sshtunnel" user.
8) Add the public key of the "sshtunnel" user to the "authorized_keys" file.

## Client Side

1) Create /etc/sshtunnel directory.
2) Create a key pair for the "sshtunnel" user.
3) Create a sshtunnel.service file.

``````BASH
sudo mkdir -p /etc/sshtunnel
sudo ssh-keygen -qN "" -f /etc/sshtunnel/id_rsa
```
