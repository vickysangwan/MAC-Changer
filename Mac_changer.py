#!/usr/bin/env python

import subprocess
import optparse
import re

def get_inputs():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options,arguements)=parser.parse_args()
    if not options.interface:
        parser.error("[-] Please specify an interface ,use --help for more info")
    if not options.new_mac:
        parser.error("[-]Please specify a new_mac,use --help for more info")
    return options
def mac_changer(interface,new_mac):
    print("![+]Changing MAC address for "+interface+" to "+new_mac)
    subprocess.call(["ifconfig",interface, "down"])
    subprocess.call(["ifconfig",interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig",interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result.decode('utf-8'))
    if mac_address_search_result:
       return mac_address_search_result.group(0)
    else:
        return None

options = get_inputs()
current_mac = get_current_mac(options.interface)
if current_mac:
    print("Current MAC address:"+current_mac)
else:
    print("[-]Could not fetch MAC address")
mac_changer(options.interface,options.new_mac)
current_mac = get_current_mac(options.interface)
if current_mac == options.new_mac:
    print("![+]MAC address successfully changed to:"+current_mac)
else:
    print("![-]MAC address did not chaneged")