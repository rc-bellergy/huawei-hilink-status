#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import sys
import xmltodict
import requests
import time
import math

def to_size(size):
   if (size == 0):
       return '0 B'
   size_name = ('KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB')
   i = int(math.floor(math.log(size,1024)))
   p = math.pow(1024,i)
   s = round(size/p,2)
   return '%s %s' % (s,size_name[i])

def call_api(device_ip, resource, xml_attribs=True):
    r = requests.get('http://' + device_ip + resource)
    if r.status_code == 200:
    	return xmltodict.parse(r.text, xml_attribs=xml_attribs)
    raise Exception('Received status code ' + str(r.status_code) + ' for URL ' + r.url)     

def get_connection_status(status):
    result = 'n/a'
    if status == '2' or status == '3' or status == '5' or status == '8' or status == '20' or status == '21' or status == '23' or status == '27' or status == '28' or status == '29' or status == '30' or status == '31' or status == '32' or status == '33':
        result = 'Connection failed, the profile is invalid'
    if status == '7' or status == '11' or status == '14' or status == '37': 
        result = 'Network access not allowed'
    if status == '12' or status == '13':
        result = 'Connection failed, roaming not allowed'
    if status == '201':
        result = 'Connection failed, bandwidth exceeded'
    if status == '900':
        result = 'Connecting'
    elif status == '901':
        result = 'Connected'
    elif status == '902':
        result = 'Disconnected'
    elif status == '903':
        result = 'Disconnecting'
    return result

def get_network_type(type):
    result = 'n/a'
    if type == '0':
        result = 'No Service'
    elif type == '1':
        result = 'GSM'
    elif type == '2':
        result = 'GPRS (2.5G)'
    elif type == '3':
        result = 'EDGE (2.75G)'
    elif type == '4':
        result = 'W-CDMA (3G)'
    elif type == '5':
        result = 'HSDPA (3G)'
    elif type == '6':
        result = 'HSUPA (3G)'
    elif type == '7':
        result = 'HSPA (3G)'
    elif type == '8':
        result = 'TD-SCDMA (3G)'
    elif type == '9':
        result = 'HSPA+ (4G)'
    elif type == '10':
        result = 'EV-DO rev. 0'
    elif type == '11':
        result = 'EV-DO rev. A'
    elif type == '12':
        result = 'EV-DO rev. B'
    elif type == '13':
        result = '1xRTT'
    elif type == '14':
        result = 'UMB'
    elif type == '15':
        result = '1xEVDV'
    elif type == '16':
        result = '3xRTT'
    elif type == '17':
        result = 'HSPA+ 64QAM'
    elif type == '18':
        result = 'HSPA+ MIMO'
    elif type == '19':
        result = 'LTE (4G)'
    elif type == '41':
        result = '3G'
    return result

def get_roaming_status(status):
    result = 'n/a'
    if status == '0':
        result = 'disabled'
    elif status == '1':
        result = 'enabled'
    return result

def get_signal_level(level):
    result = '-'
    if level == '1':
        result = '*'
    if level == '2':
        result = '**'
    if level == '3':
        result = '***'
    if level == '4':
        result = '****'
    if level == '5':
        result = '*****'
    return result

def print_traffic_statistics(device_ip, connection_status):
    d = call_api(device_ip, '/api/monitoring/traffic-statistics')
    current_connect_time = d['response']['CurrentConnectTime']
    current_upload = d['response']['CurrentUpload']
    current_download = d['response']['CurrentDownload']
    total_upload = d['response']['TotalUpload']
    total_download = d['response']['TotalDownload']

    if connection_status == '901':
        print('    Connected for: ' + time.strftime('%H:%M:%S', time.gmtime(float(current_connect_time))) + ' (hh:mm:ss)')
        print('    Downloaded: ' + to_size(float(current_download)))
        print('    Uploaded: ' + to_size(float(current_upload)))
    print('  Total downloaded: ' + to_size(float(total_download)))
    print('  Total uploaded: ' + to_size(float(total_upload)))

def print_connection_status(device_ip):
    d = call_api(device_ip, '/api/monitoring/status')
    connection_status = d['response']['ConnectionStatus']
    signal_strength = d['response']['SignalStrength']
    signal_level = d['response']['SignalIcon']
    network_type = d['response']['CurrentNetworkType']
    roaming_status = d['response']['RoamingStatus']
    wan_ip = d['response']['WanIPAddress']
    primary_dns_ip = d['response']['PrimaryDns']
    secondary_dns_ip = d['response']['SecondaryDns']
    wifi_status = d['response']['WifiStatus']
    wifi_users_current = d['response']['CurrentWifiUser']
    wifi_users_max = d['response']['TotalWifiUser']

    r = requests.get('http://ip.o11.net')
    public_ip = None
    if r.status_code == 200:
        public_ip = r.text.rstrip()

    print('  Connection status: ' + get_connection_status(connection_status))
    if connection_status == '901':
        print('    Network type: ' + get_network_type(network_type))
        print('    Signal Level: ' + get_signal_level(signal_level) + ' (' + signal_strength + '%)')
        print('    Roaming: ' + get_roaming_status(roaming_status))
    if wan_ip is not None:
        print('    Modem WAN IP address: ' +  wan_ip)
    print('    Public IP address: ' + public_ip)
    print('    DNS IP addresses: ' + primary_dns_ip + ', ' + secondary_dns_ip)
    if wifi_status == '1':
        print('    WIFI users\t\t' + wifi_users_current + ' (of ' + wifi_users_max + ')')

    return connection_status

def print_device_info(device_ip):
    d = call_api(device_ip, '/api/device/information')
    device_name = d['response']['DeviceName']
    serial_number = d['response']['SerialNumber']
    imei = d['response']['Imei']
    hardware_version = d['response']['HardwareVersion']
    software_version = d['response']['SoftwareVersion']
    mac_address1 = d['response']['MacAddress1']
    mac_address2 = d['response']['MacAddress2']
    product_family = d['response']['ProductFamily']

    print('Huawei ' + device_name + ' ' + product_family + ' Modem (IMEI: ' + imei + ')')
    print('  Hardware version: ' + hardware_version) 
    print('  Software version: ' + software_version)
    print('  Serial: ' + serial_number)
    print('  MAC address (Modem): ' + mac_address1, end='')
    if mac_address2 is not None:
        print('\tMAC address (WiFi): ' + mac_address2)
    else:
        print('')

def print_provider(device_ip, connection_status):
    d = call_api(device_ip, '/api/net/current-plmn')
    state = d['response']['State']
    provider_name = d['response']['FullName']
    if connection_status == '901':
        print('    Network provider: ' + provider_name)

def print_unread(device_ip):
    d = call_api(device_ip, '/api/monitoring/check-notifications')
    unread_messages = d['response']['UnreadMessage']
    if unread_messages is not None and int(unread_messages) > 0:
        print('  Unread SMS: ' + unread_messages)

device_ip = '192.168.1.1'
if len(sys.argv) == 2:
    device_ip = sys.argv[1]
  
print_device_info(device_ip)
connection_status = print_connection_status(device_ip)
print_provider(device_ip, connection_status)
print_traffic_statistics(device_ip, connection_status)
print_unread(device_ip)
print('')
