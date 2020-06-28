from assets import asset_handler
from assets import models
from django.shortcuts import render, get_object_or_404
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def report(request):
    if request.method == "POST":
        asset_data = request.POST.get('asset_data')
        data = json.loads(asset_data)
        # print(asset_data)
        if not data:
            return HttpResponse('未收到数据...')
        if not issubclass(dict, type(data)):
            return HttpResponse('数据必须是字典格式...')
        sn = data.get('sn', None)
        if sn:
            asset_obj = models.Asset.objects.filter(sn=sn)
            print(asset_obj)
            if asset_obj:
                update_asset = asset_handler.UpdateAsset(
                    request, asset_obj[0], data)
                return HttpResponse('数据已经更新...')
            else:
                obj = asset_handler.NewAsset(request, data)
                reponse = obj.add_to_new_asset_zone()
                return HttpResponse(reponse)
        else:
            return HttpResponse('没有资产序列，请检查...')
    return HttpResponse('200 ok! 成功收到数据！')


def index(request):

    assets = models.Asset.objects.all()
    return render(request, 'assets/index.html', locals())


def dashboard(request):
    pass
    return render(request, 'assets/dashboard.html', locals())


def detail(request, asset_id):
    """
    以显示服务器类型资产详细为例，安全设备、存储设备、网络设备等参照此例。
    :param request:
    :param asset_id:
    :return:
    """
    asset = get_object_or_404(models.Asset, id=asset_id)
    return render(request, 'assets/detail.html', locals())

