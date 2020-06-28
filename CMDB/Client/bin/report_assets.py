import json
import os
import sys
import urllib.request
import urllib.parse
from CMDB.Client.conf import settings


# 设置工作目录，使得包和模块能够正常导入
BASE_DIR = os.path.dirname(os.getcwd())
sys.path.append(BASE_DIR)


def update_test(data):
    data = {'asset_data': json.dumps(data)}
    url = "http://%s:%s%s" % (
        settings.Params['server'], settings.Params['port'],
        settings.Params['url'])
    print('正在将数据发送至： [%s]  ......' % url)
    try:
        data_encode = urllib.parse.urlencode(data).encode()
        response = urllib.request.urlopen(
            url=url, data=data_encode,
            timeout=settings.Params['request_timeout'])
        print('\033[31m;1m 发送完毕！\033[0m ')
        message = response.read().decode()
        print('返回结果： %s ' % message)
    except Exception as e:
        message = '发送失败'
        print('\033[31m;1m发送失败，%s\033[0m' % e)


if __name__ == '__main__':
    windows_data = {
        "os_type": "Windows10",
        "os_release": "10 64bit  6.1.7601 ",
        "os_distribution": "Microsoft",
        "asset_type": "server",
        "cpu_count": 4,
        "cpu_model": "Intel(R) Core(TM) i5-2300 CPU @ 2.80GHz",
        "cpu_core_count": 16,
        "ram": [
            {
                "slot": "A7",
                "capacity": 8,
                "model": "Physical Memory",
                "manufacturer": "kingstone ",
                "sn": "456"
            },

        ],
        "manufacturer": "Intel",
        "model": "P67X-UD3R-B3",
        "wake_up_type": 7,
        "sn": "021",
        "physical_disk_driver": [
            {
                "iface_type": "unknown",
                "slot": 7,
                "sn": "3830414130423230343234362020202020202020",
                "model": "KINGSTON SV100S264G ATA Device",
                "manufacturer": "(标准磁盘驱动器)",
                "capacity": 256
            },
            {
                "iface_type": "SATA",
                "slot": 4,
                "sn": "383041413042323023234362020102020202020",
                "model": "KINGSTON SV100S264G ATA Device",
                "manufacturer": "(标准磁盘驱动器)",
                "capacity": 2049
            },

        ],
        "nic": [
            {
                "mac": "15:CF:22:FF:48:34",
                "model": "[00000011] Realtek RTL8192CU Wireless LAN 802.11n USB 2.0 Network Adapter",
                "name": 20,
                "ip_address": "192.168.10.120",
                "net_mask": [
                    "255.255.255.0",
                    "64"
                ]
            },
            {
                "mac": "01:01:27:00:00:10",
                "model": "[00000013] VirtualBox Host-Only Ethernet Adapter",
                "name": 13,
                "ip_address": "192.168.5.4",
                "net_mask": [
                    "255.255.255.0",
                    "64"
                ]
            },
            {
                "mac": "14:CF:22:4F:82:34",
                "model": "[00000017] Microsoft Virtual WiFi Miniport Adapter",
                "name": 152,
                "ip_address": "",
                "net_mask": ""
            },
            {
                "mac": "14:CF:22:FF:47:34",
                "model": "Intel Adapter",
                "name": 45,
                "ip_address": "192.1.7.1",
                "net_mask": ""
            },

        ]
    }
    update_test(windows_data)

