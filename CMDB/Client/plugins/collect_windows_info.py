import platform
import win32com
import wmi


class Win32Info(object):
    """
    本模块基于windows操作系统，依赖wmi和win32com库，需要提前使用pip进行安装，
    pip install wmi
    pip install pypiwin32
    """
    def __init__(self):
        self.wmi_obj = wmi.WMI()
        self.wmi_server_obj = win32com.client.Dispatch(
            "WbemScripting.SWbemLocator")
        self.wmi_service_connector = self.wmi_server_obj.\
            ConnectServer(".", "root\cimv2")

    def collect(self):
        data = {
            'os_type': platform.system(),
            'os_release': "%s %s  %s " % (
            platform.release(), platform.architecture()[0],
            platform.version()),
            'os_distribution': 'Microsoft',
            'asset_type': 'server'
        }
        data.update(self.get_cpu_info())
        data.update(self.get_disk_info())
        data.update(self.get_motherboard_info())
        data.update(self.get_nic_info())
        data.update(self.get_ram_info())
        return data

    def get_cpu_info(self):
        data = {}
        cpu_lists = self.wmi_obj.Win32_processor()
        cpu_core_count = 0
        for cpu in cpu_lists:
            cpu_core_count += cpu.NumberOfCores
        cpu_model = cpu_lists[0].Name
        data['cpu_count'] = len(cpu_lists)
        data['cpu_model'] = cpu_model
        data['cpu_core_count'] = cpu_core_count
        return data

    def get_ram_info(self):
        data = []
        # 这个模块用SQL语言获取数据
        ram_collections = self.wmi_service_connector.ExecQuery(
            "select *from Win32_PhysicalMemory"
        )
        for ram in ram_collections:
            ram_size = int(int(ram.capacity) / (1024**3))
            item_data = {
                "slot": ram.DeviceLocator.strip(),
                "capacity": ram_size,
                "model": ram.Caption,
                "manufacturer": ram.Manufacturer,
                "sn": ram.SerialNumber,
            }
            data.append(item_data)
        return {'ram': data}

    def get_motherboard_info(self):
        compute_info = self.wmi_obj.Win32_ComputerSystem()[0]
        system_info = self.wmi_obj.Win32_OperatingSystem()[0]
        data = {}
        data['manufacturer'] = compute_info.manufacturer
        data['model'] = compute_info.Model
        data['wake_up_type'] = compute_info.WakeUpType
        data['sn'] = system_info.SerialNumber
        return data

    def get_disk_info(self):
        data = []
        for disk in self.wmi_obj.Win32_DiskDrive():  # 每块硬盘都要获取相应信息
            disk_data = {}
            interface_choices = ["SAS", "SCSI", "SATA", "SSD"]
            for interface in interface_choices:
                if interface in disk.Model:
                    disk_data['interface_type'] = interface
                    break
            else:
                disk_data['interface_type'] = 'unknown'

            disk_data['slot'] = disk.Index
            disk_data['sn'] = disk.SerialNumber
            disk_data['model'] = disk.Model
            disk_data['manufacturer'] = disk.Manufacturer
            disk_data['capacity'] = int(int(disk.Size) / (1024 ** 3))
            data.append(disk_data)
        return {'physical_disk_driver': data}

    def get_nic_info(self):
        """
        网卡信息
        :return:
        """
        data = []
        for nic in self.wmi_obj.Win32_NetworkAdapterConfiguration():
            if nic.MACAddress is not None:
                nic_data = {}
                nic_data['mac'] = nic.MACAddress
                nic_data['model'] = nic.Caption
                nic_data['name'] = nic.Index
                if nic.IPAddress is not None:
                    nic_data['ip_address'] = nic.IPAddress[0]
                    nic_data['net_mask'] = nic.IPSubnet
                else:
                    nic_data['ip_address'] = ''
                    nic_data['net_mask'] = ''
                data.append(nic_data)

        return {'nic': data}


if __name__ == '__main__':
    data = Win32Info().collect()
    for key in data:
        print(key, ":", data[key])


