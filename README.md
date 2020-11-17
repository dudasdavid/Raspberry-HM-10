# Raspberry-HM-10

BLE enabled Raspberry Pi shows itself as a HM-10 module and two way communication works with apps that are intended to communicate with HM-10 modules.

Dependencies:
  `pip3 install pybleno`
  
Permission:
  `sudo setcap 'cap_net_raw,cap_net_admin+eip' /usr/bin/python3.7` to give permissions for python to use BLE
  
Usage:
  `python3 main.py`
