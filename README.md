huawei-hilink-status
===================

Simple Python command-line utility to query Huawei HiLink modems for status information.

## Installation
The utility uses the xmltodict library which can be installed using ```pip```:
```
apt-get install python-pip
pip install xmltodict
```

## Usage example

```
$ ./hstatus.py
Huawei E3276 LTE Modem (IMEI: 861711012616361)
  Hardware version: CH2F4276GM
  Software version: 22.250.04.00.186
  Serial: B3A3TC2313833197
  MAC address (Modem): 00:0D:87:22:34:AC
  Connection status: Connected
    Network type: W-CDMA (3G)
    Signal Level: ***** (92%)
    Roaming: enabled
    Modem WAN IP address: 10.197.32.60
    Public IP address: 32.131.81.221
    DNS IP addresses: 212.113.0.4, 66.28.0.61
    Network provider: Swisscom
    Connected for: 00:49:33 (hh:mm:ss)
    Downloaded: 737.0 KB
    Uploaded: 178.0 KB
  Total downloaded: 47.69 MB
  Total uploaded: 19.86 MB
```
