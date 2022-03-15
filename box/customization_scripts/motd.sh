#!/bin/bash

echo 'cat << EOF' >> /etc/update-motd.d/00-header
echo '  _          _      _    _                 _       ' >> /etc/update-motd.d/00-header
echo ' | |        (_)    | |  | |               (_)      ' >> /etc/update-motd.d/00-header
echo ' | |__  _ __ _  ___| | _| |__   _____  __  _  ___  ' >> /etc/update-motd.d/00-header
echo " | '_ \| '__| |/ __| |/ / '_ \ / _ \ \/ / | |/ _ \ " >> /etc/update-motd.d/00-header
echo ' | |_) | |  | | (__|   <| |_) | (_) >  < _| | (_) |' >> /etc/update-motd.d/00-header
echo ' |_.__/|_|  |_|\___|_|\_\_.__/ \___/_/\_(_)_|\___/ ' >> /etc/update-motd.d/00-header
echo 'EOF' >> /etc/update-motd.d/00-header
