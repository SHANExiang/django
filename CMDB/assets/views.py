from assets import asset_handler
from assets import models
from django.shortcuts import render
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

