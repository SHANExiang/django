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
        "cpu_count": 2,
        "cpu_model": "Intel(R) Core(TM) i5-2300 CPU @ 2.80GHz",
        "cpu_core_count": 8,
        "ram": [
            {
                "slot": "A1",
                "capacity": 8,
                "model": "Physical Memory",
                "manufacturer": "kingstone ",
                "sn": "456"
            },

        ],
        "manufacturer": "Intel",
        "model": "P67X-UD3R-B3",
        "wake_up_type": 6,
        "sn": "021",
        "physical_disk_driver": [
            {
                "iface_type": "unknown",
                "slot": 0,
                "sn": "3830414130423230343234362020202020202020",
                "model": "KINGSTON SV100S264G ATA Device",
                "manufacturer": "(标准磁盘驱动器)",
                "capacity": 128
            },
            {
                "iface_type": "SATA",
                "slot": 1,
                "sn": "383041413042323023234362020102020202020",
                "model": "KINGSTON SV100S264G ATA Device",
                "manufacturer": "(标准磁盘驱动器)",
                "capacity": 2048
            },

        ],
        "nic": [
            {
                "mac": "14:CF:22:FF:48:34",
                "model": "[00000011] Realtek RTL8192CU Wireless LAN 802.11n USB 2.0 Network Adapter",
                "name": 11,
                "ip_address": "192.168.1.110",
                "net_mask": [
                    "255.255.255.0",
                    "64"
                ]
            },
            {
                "mac": "0A:01:27:00:00:00",
                "model": "[00000013] VirtualBox Host-Only Ethernet Adapter",
                "name": 13,
                "ip_address": "192.168.56.1",
                "net_mask": [
                    "255.255.255.0",
                    "64"
                ]
            },
            {
                "mac": "14:CF:22:FF:48:34",
                "model": "[00000017] Microsoft Virtual WiFi Miniport Adapter",
                "name": 17,
                "ip_address": "",
                "net_mask": ""
            },
            {
                "mac": "14:CF:22:FF:48:34",
                "model": "Intel Adapter",
                "name": 17,
                "ip_address": "192.1.1.1",
                "net_mask": ""
            },

        ]
    }
    update_test(windows_data)

