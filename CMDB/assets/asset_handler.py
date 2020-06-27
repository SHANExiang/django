from assets import models
import json


class NewAsset(object):
    def __init__(self, request, data):
        self.request = request
        self.data = data

    def add_to_new_asset_zone(self):
        defaults = {
            'data': json.dumps(self.data),
            'asset_type': self.data.get('asset_type'),
            'manufacturer': self.data.get('manufacturer'),
            'model': self.data.get('model'),
            'ram_size': self.data.get('ram_size'),
            'cpu_model': self.data.get('cpu_model'),
            'cpu_count': self.data.get('cpu_count'),
            'cpu_core_count': self.data.get('cpu_core_count'),
            'os_distribution': self.data.get('os_distribution'),
            'os_release': self.data.get('os_release'),
            'os_type': self.data.get('os_type'),
        }
        models.NewAssetApprovalZone.objects.update_or_create(
            sn=self.data.get('sn'), defaults=defaults)

        return '资产已经加入或更新待审批区！'


def log(log_type, msg=None, asset=None, new_asset=None, request=None):
    event = models.EventLog()
    if log_type == 'upline':
        event.name = '%s <%s>: 上线' % (asset.name, asset.sn)
        event.asset = asset
        event.detail = '资产成功上线！'
        event.user = request.user
    elif log_type == 'approve_failed':
        event.name = '%s <%s>: 审批失败' % (new_asset.asset_type,
                                        new_asset.sn)
        event.new_asset = new_asset
        event.detail = '审批失败！\n%s' % msg
        event.user = request.user
    elif log_type == 'update':
        event.name = '%s <%s>: 更新' % (asset.asset_type, asset.sn)
        event.asset = asset
        event.detail = '更新成功'
    elif log_type == 'update_failed':
        event.name = "%s <%s> ：  更新失败" % (asset.asset_type, asset.sn)
        event.asset = asset
        event.detail = "更新失败！\n%s" % msg
    event.save()


class UpdateAsset(object):
    def __init__(self, request, asset, report_asset):
        self.request = request
        self.asset = asset
        self.report_asset = report_asset
        self.asset_update()

    def asset_update(self):
        func = getattr(self, '_%s_update' % self.asset.asset_type)
        ret = func()
        return ret

    def _server_update(self):
        pass


    def _update_manufacturer(self):
        m = self.report_asset.get('manufacturer')
        if m:
            manufacturer_obj, _ = models.Manufacturer.objects.get_or_create(
                name=m)
            self.asset.manufacturer = manufacturer_obj
        else:
            self.asset.manufacturer = None
        self.asset.manufacturer.save()

    def _update_server(self):
        self.asset.server.model = self.report_asset.get('model')
        self.asset.server.os_type = self.report_asset.get('os_type')
        self.asset.server.os_distribution = self.report_asset.get(
            "os_distribution"
        )
        self.asset.server.os_release = self.report_asset.get('os_release')
        self.asset.server.save()

    def _update_CPU(self):
        self.asset.CPU.cpu_model = self.report_asset.get('cpu_model')
        self.asset.CPU.cpu_count = self.report_asset.get('cpu_count')
        self.asset.CPU.cpu_core_count = self.report_asset.get(
            'cpu_core_count')
        self.asset.CPU.save()

    def _update_RAM(self):
        old_rams = models.RAM.objects.filter(asset=self.asset)
        old_rams_dict = dict()
        if old_rams:
            for ram in old_rams:
                old_rams_dict[ram.slot] = ram
        new_rams = self.report_asset.get('ram')
        new_rams_dict = dict()
        if new_rams:
            for ram in new_rams:
                new_rams_dict[ram['slot']] = ram
        need_deleted_keys = set(old_rams_dict.keys()) - \
                            set(new_rams_dict.keys())







class ApproveAsset(object):
    def __init__(self, request, asset_id):
        self.request = request
        self.new_asset = models.NewAssetApprovalZone.objects.get(
            id=asset_id
        )
        self.data = json.loads(self.new_asset.data)

    def asset_upline(self):
        func = getattr(self, '_%s_upline' % self.new_asset.asset_type)
        ret = func()
        return ret

    def _server_upline(self):
        # 创建一条资产并返回资产对象。注意要和待审批区的资产区分开。
        asset = self._create_asset()
        try:
            self._create_manufacturer(asset)
            self._create_server(asset)  # 创建服务器
            self._create_CPU(asset)  # 创建CPU
            self._create_RAM(asset)  # 创建内存
            self._create_disk(asset)  # 创建硬盘
            self._create_nic(asset)  # 创建网卡
            self._delete_original_asset()  # 从待审批资产区删除已审批上线的资产
        except Exception as e:
            asset.delete()
            log('approve_failed', msg=e, new_asset=self.new_asset,
                request=self.request)
            print(e)
            return False
        else:
            log('upline', asset=asset, request=self.request)
            print('新服务器上线！')
            return True

    def _create_asset(self):
        asset = models.Asset.objects.create(
            asset_type=self.new_asset.asset_type,
            name='%s: %s' % (self.new_asset.asset_type,
                             self.new_asset.sn),
            sn=self.new_asset.sn,
            approved_by=self.request.user
        )
        return asset

    def _create_manufacturer(self, asset):
        m = self.new_asset.manufacturer
        if m:
            manufacturer_obj, _ = models.Manufacturer.objects.\
                get_or_create(name=m)
            asset.manufacturer = manufacturer_obj
            asset.save()

    def _create_server(self, asset):
        models.Server.objects.create(
            asset=asset,
            model=self.new_asset.model,
            os_type=self.new_asset.os_type,
            os_distribution=self.new_asset.os_distribution,
            os_release=self.new_asset.os_distribution
        )

    def _create_CPU(self, asset):
        cpu = models.CPU.objects.create(asset=asset)
        cpu.cpu_core_count = self.new_asset.cpu_core_count
        cpu.cpu_model = self.new_asset.cpu_model
        cpu.cpu_count = self.new_asset.cpu_core_count
        cpu.save()

    def _create_RAM(self, asset):
        ram_list = self.data.get('ram')
        if not ram_list:
            return
        for ram_dict in ram_list:
            if not ram_dict.get('slot'):
                raise ValueError("未知的内存插槽！")  # 使用虚拟机的时候，可能无法获取内存插槽，需要你修改此处的逻辑。
            ram = models.RAM()
            ram.asset = asset
            ram.sn = ram_dict.get('sn')
            ram.slot = ram_dict.get('slot')
            ram.model = ram_dict.get('model')
            ram.manufacturer = ram_dict.get('manufacturer')
            ram.capacity = ram_dict.get('capacity')
            ram.save()

    def _create_disk(self, asset):
        disk_list = self.data.get('physical_disk_driver')
        if not disk_list:
            return
        for disk_dict in disk_list:
            if not disk_dict.get('sn'):
                raise ValueError('未知sn的硬盘')
            disk = models.Disk()
            disk.asset = asset
            disk.sn = disk_dict.get('sn')
            disk.slot = disk_dict.get('slot')
            disk.model = disk_dict.get('model')
            disk.manufacturer = disk_dict.get('manufacturer')
            disk.capacity = disk_dict.get('capacity', 0)
            iface = disk_dict.get('interface_type')
            if iface in ['SATA', 'SAS', 'SCSI', 'SSD', 'unknown']:
                disk.interface_type = iface
            disk.save()

    def _create_nic(self, asset):
        nic_list = self.data.get('nic')
        if not nic_list:
            return
        for nic_dict in nic_list:
            if not nic_dict.get('mac'):
                raise ValueError('网卡缺少mac地址')
            if not nic_dict.get('model'):
                raise ValueError('网卡型号未知')
            nic = models.NIC()
            nic.asset = asset
            nic.name = nic_dict.get('name')
            nic.model = nic_dict.get('model')
            nic.mac = nic_dict.get('mac')
            nic.ip_address = nic_dict.get('ip_address')
            if nic_dict.get('net_mask'):
                if len(nic_dict.get('net_mask')) > 0:
                    nic.net_mask = nic_dict.get('net_mask')[0]
            nic.save()

    def _delete_original_asset(self):
        self.new_asset.delete()



