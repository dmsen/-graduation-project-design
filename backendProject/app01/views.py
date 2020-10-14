# from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
# 登陆
def linSystem_login(request):
    from .models import linSystemUser
    print("用户登录")
    jsonResponse = json.loads(request.body.decode('utf-8'))
    print (jsonResponse)
    print(request, type(jsonResponse['optionLevel']))
    if(jsonResponse['userName'].strip() =='' or jsonResponse['password'].strip() =='' ):
        return JsonResponse({"result": 2, "msg": '用户名/密码不能为空'})
    else:
        if(jsonResponse['optionLevel'] ==0):
            try:
                if ('lin' == jsonResponse['userName'].strip() and 'lin' == jsonResponse['password'].strip()):
                    return JsonResponse({"result": 0,
                                         "msg": {'userId': 1, 'userName': 'lin', 'password': 'lin', 'roles': '最高管理员',
                                                 'jurisdiction': 0, 'status': 1, 'remarks': '最高管理员','userTou':'linSystem/defaultTou.png'}})
                else:
                    return JsonResponse({"result": 3, "msg": '用户名密码错误,请检查登陆方式'})
            except:
                return JsonResponse({"result": 4, "msg": '用户名不存在/密码错误'})
        elif(jsonResponse['optionLevel'] ==1):
            return JsonResponse({"result": 0,
                                 "msg": {'userId': -2, 'userName': 'xxx', 'password': 'xxx', 'roles': '访客',
                                         'jurisdiction': 3, 'status': 1, 'remarks': '访客','userTou':'linSystem/defaultTou.png'}})
        elif (jsonResponse['optionLevel'] == 2):
            if(len(linSystemUser.objects.all().filter(userName=jsonResponse['userName'])) == 0):
                return JsonResponse({"result": 5, "msg": '用户不存在'})
            else:

                try:
                    if (jsonResponse['password'] == linSystemUser.objects.all().get(userName=jsonResponse['userName']).__dict__[
                        'password']):
                        userInfo = linSystemUser.objects.all().get(userName=jsonResponse['userName']).__dict__
                        return JsonResponse({"result": 0,
                                             "msg": {
                                                 'userId': userInfo['userId'],
                                                 'userName':  userInfo['userName'],
                                                 'password':userInfo['password'],
                                                'jurisdiction': userInfo['jurisdiction'],
                                                 'status': userInfo['status'],
                                                 'remarks':userInfo['remarks'],
                                                'userTou':userInfo['userPic']}})
                    else:
                        return JsonResponse({"result": 6, "msg": '用户名密码错误'})
                except:
                    return JsonResponse({"result": 1, "msg": '未知错误'})





#  将查询集变成字典形式
def queryset_to_json(queryset):
    obj_arr = []
    for o in queryset:
        obj_arr.append(o.toDict())
    return obj_arr


# 获取用户
def linSystem_user_get(request):
    from .models import linSystemUser, linSystemNotice
    jsonResponse = json.loads(request.body.decode('utf-8'))
    if (jsonResponse["sendPage"]):
        pastJson = linSystemUser.objects.all()[jsonResponse["sendPage"] * 10 - 10:jsonResponse["sendPage"] * 10]
    else:
        pastJson = linSystemUser.objects.all()[1 * 10 - 10:1 * 10]
    lists = []
    for i in range(len(pastJson)):
        # 此用户接受到的通知
        from django.db.models import Q
        lists.append({
            'id': pastJson[i].__dict__['userId'],
            'num': len(
                queryset_to_json(linSystemNotice.objects.filter(Q(linSystemNoticeUser=pastJson[i].__dict__['userId']) & Q(status=0)))),
            'userName': str(pastJson[i].__dict__['userName']),
            'remarks': str(pastJson[i].__dict__['remarks']),
            'level': pastJson[i].__dict__['jurisdiction'],
            "status": pastJson[i].__dict__['status'],
        })
    return JsonResponse({"allDateLength": linSystemUser.objects.all().count(), "msg": lists})

# 增加用户
def linSystem_user_add(request):
    from .models import linSystemUser
    # jsonResponse = json.load(request.body)
    jsonResponse = json.loads(request.body.decode('utf-8'))
    print("增加用户")
    print(jsonResponse, type(jsonResponse))
    dataLists = linSystemUser.objects.all().count()
    try:
        if (dataLists > 20):
            return JsonResponse({"result": 0, "msg": "增加失败,用户数目不能超过20人"})
        else:
            linSystemUser.objects.create(**jsonResponse)
    except:
        return JsonResponse({"result": 1, "msg": "增加失败,用户名重复/信息不完整"})
    else:
        return JsonResponse({"result": 0, "msg": "增加成功"})


# 用户个人信息修改
def linSystem_user_updata(request):
    from .models import linSystemUser
    print(request.body.decode('utf-8'))
    print("用户个人信息修改-")
    jsonResponse = json.loads(request.body.decode('utf-8'))
    print(jsonResponse, type(jsonResponse))
    print("用户个人信息修改-")
    print(jsonResponse['id'], type(jsonResponse['id']))
    try:
        # @@@@@@@@@@@@@@@@@@@@        这里需要做个判断，权限判断只有管理员才有权力变更用户权限   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
        if(jsonResponse['mode'] == 'usermanagementMod'):
            linSystemUser.objects.filter(userId=jsonResponse['id']).update(
                userName=jsonResponse['userName'],
                password=jsonResponse['password'],
                remarks=jsonResponse['remarks'],
                status=jsonResponse['status'],
                jurisdiction = jsonResponse['jurisdiction']
        )
        else:
            linSystemUser.objects.filter(userId=jsonResponse['id']).update(
                userName=jsonResponse['userName'],
                password=jsonResponse['password'],
                remarks=jsonResponse['remarks'],
                status=jsonResponse['status'])
    except:
        return JsonResponse({"result": 1, "msg": "修改失败，用户名重复/信息不完整"})
    else:
        return JsonResponse({"result": 0, "msg": "修改成功"})

# 删除用户
def linSystem_user_del(request):
    from .models import linSystemUser
    jsonResponse = json.loads(request.body.decode('utf-8'))
    # print (jsonResponse,type(jsonResponse))
    print("删除删除））））））））））））））））））））））））））））")
    print (jsonResponse['id'],jsonResponse['userId'])
    fJurisdiction = linSystemUser.objects.get(userId=jsonResponse['id']).__dict__['jurisdiction']
    lJurisdiction = linSystemUser.objects.get(userId=jsonResponse['userId']).__dict__['jurisdiction']
    if (jsonResponse['id'] == 1 or jsonResponse['id'] == 2):
        return JsonResponse({"result": 1, "msg": "系统默认用户无法删除"})
    else:
        if (fJurisdiction == lJurisdiction):
            return JsonResponse({"result": 1, "msg": "您们权限相等，无法删除"})
        elif (lJurisdiction > fJurisdiction):
            return JsonResponse({"result": 1, "msg": "对方权限比您高，无法删除"})
        else:
            try:
                linSystemUser.objects.filter(userId=jsonResponse['id']).delete()
            except :
                return JsonResponse({"result": 1, "msg": "未知错误"})
            else:
                return JsonResponse({"result": 0, "msg": "删除成功"})



# 用户通知
def linSystem_user_notice(request):
    from .models import  linSystemUser, linSystemNotice
    jsonResponse = json.loads(request.body.decode('utf-8'))
    print("通知")
    print (jsonResponse,type(jsonResponse))
    dataLists = linSystemNotice.objects.all().count()
    # courseGet = hutProjectsUsers.objects.get(hutCourseId=jsonResponse['hutCourseId'])
    userGet = linSystemUser.objects.get(userId=jsonResponse['hutUserId'])
    try:
    # 这里需要单独create
        if(jsonResponse['courseEvaluateMsg'].strip() == ""):
            return JsonResponse({"result": 1, "msg": "评价不能为空"})
        else:
            linSystemNotice.objects.create(
                            linSystemNoticeUser=userGet,
                            msg=jsonResponse['courseEvaluateMsg'],
                            byPerson=jsonResponse['userName'],
                            courseEvaluateDate=jsonResponse['courseEvaluateDate'],
                            )
    except :
        return JsonResponse({"result": 1, "msg": "失败,未知问题，请联系管理员解决"})
    else:
        return JsonResponse({"result": 0, "msg": "成功"})



# 修改用户头像
def linSystem_userPic_mod(request):
    from .models import linSystemUser,file_delete
    # print(request.FILES)
    # print (request.FILES['croppedImg'])
    # obj = request.FILES.get("croppedImg")
    # print (obj, type(obj), obj.name, obj.chunks())
    # print (obj.file,obj.field_name,obj.name, obj.content_type,
    #               obj.size, obj.charset, obj.content_type_extra)
    userId = int(request.POST.__getitem__('userId'))
    userName = request.POST.__getitem__('userName')
    print("修改用户头像")
    from django.core.files.base import ContentFile
    # 读取上传的文件中的video项为二进制文件
    file_content = ContentFile(request.FILES['croppedImg'].read())
    # # ImageField的save方法，第一个参数是保存的文件名，第二个参数是ContentFile对象，里面的内容是要上传的图片、视频的二进制内容
    mymodel = linSystemUser.objects.get(userId=userId)
    # print(mymodel.__dict__)
    # print(mymodel.userPic)
    if(mymodel.userPic == "/linSystem/defaultTou.png"):
        mymodel.userPic.save(request.FILES['croppedImg'].name + '_' + userName + '.png', file_content)
    else:
        # 删除之前的图片，避免 图片冗杂
        file_delete(linSystemUser, mymodel)
        #再存储头像图片
        mymodel.userPic.save(request.FILES['croppedImg'].name+'_'+userName+'.png', file_content)
    return JsonResponse({"result": 0, "msg": "用户头像修改成功"})




# 获取未读通知
def linSystem_user_getNotice(request):
    from .models import linSystemNotice,linSystemUser
    jsonResponse = json.loads(request.body.decode('utf-8'))
    # print(jsonResponse)
    from django.db.models import Q
    pastJson = queryset_to_json(linSystemNotice.objects.filter( Q(linSystemNoticeUser=jsonResponse['userId'])  & Q(status=0) ))
    pastJsonLength = len(pastJson)
    jsonLists = []
    if(len(pastJson) == 0):
        return JsonResponse({"result": 1, "msg": "为空"})
    else:
        if (jsonResponse["sendPage"]):
            pastJson =  pastJson[jsonResponse["sendPage"]*3-3:jsonResponse["sendPage"]*3]
            for i in range(len(pastJson)):
                jsonLists.append(
                    {"content": pastJson[i]["msg"],
                     "byPerson": pastJson[i]["byPerson"],
                     "time": pastJson[i]["courseEvaluateDate"],
                     "linSystemNoticeId":pastJson[i]["linSystemNoticeId"],
                     }
                )
        else:
            pastJson =  pastJson[0:3]
            for i in range(len(pastJson)):
                jsonLists.append(
                    {"content": pastJson[i]["msg"],
                     "byPerson": pastJson[i]["byPerson"],
                     "time": pastJson[i]["courseEvaluateDate"],
                     "linSystemNoticeId": pastJson[i]["linSystemNoticeId"],
                     }
                )
        return JsonResponse({"result": 0, "msg": jsonLists,"allDateLength": pastJsonLength})


# 标记通知已读
def linSystem_user_readNotice(request):
    from .models import linSystemNotice
    jsonResponse = json.loads(request.body.decode('utf-8'))
    print (jsonResponse['noticeId'],type(jsonResponse['noticeId']))
    print("测试））））））））））））））））））））））））））））")
    try:
        linSystemNotice.objects.filter(linSystemNoticeId=jsonResponse['noticeId']).update(
            status = 1
        )
    except:
        return JsonResponse({"result": 1, "msg": "未知错误"})
    else:
        return JsonResponse({"result": 0, "msg": "操作成功"})


# 查看已读通知
def linSystem_user_readEdNotice(request):
    from .models import linSystemNotice
    jsonResponse = json.loads(request.body.decode('utf-8'))
    from django.db.models import Q
    pastJson = queryset_to_json(linSystemNotice.objects.filter( Q(linSystemNoticeUser=jsonResponse['userId'])  & Q(status=1) ))
    pastJsonLength = len(pastJson)
    jsonLists = []
    if(len(pastJson) == 0):
        return JsonResponse({"result": 1, "msg": "为空"})
    else:
        if (jsonResponse["sendPage"]):
            pastJson =  pastJson[jsonResponse["sendPage"]*3-3:jsonResponse["sendPage"]*3]
            for i in range(len(pastJson)):
                jsonLists.append(
                    {"content": pastJson[i]["msg"],
                     "byPerson": pastJson[i]["byPerson"],
                     "time": pastJson[i]["courseEvaluateDate"],
                     "linSystemNoticeId":pastJson[i]["linSystemNoticeId"],
                     }
                )
        else:
            pastJson =  pastJson[0:3]
            for i in range(len(pastJson)):
                jsonLists.append(
                    {"content": pastJson[i]["msg"],
                     "byPerson": pastJson[i]["byPerson"],
                     "time": pastJson[i]["courseEvaluateDate"],
                     "linSystemNoticeId": pastJson[i]["linSystemNoticeId"],
                     }
                )
        return JsonResponse({"result": 0, "msg": jsonLists,"allDateLength": pastJsonLength})
###############################################################################
##########################    实时监测系统   ##################################
###############################################################################
# 设备类型
def linSystem_machine_type_get(request):
    from .models import machTypes
    jsonResponse = json.loads(request.body.decode('utf-8'))
    # print (jsonResponse["sendPage"])
    try:
        pastJson = queryset_to_json(machTypes.objects.all()[jsonResponse["sendPage"] * 10 - 10:jsonResponse["sendPage"] * 10])
    except:
        #  获得全部数据 便于下拉选择
        pastJson = queryset_to_json(machTypes.objects.all()[:])
    return JsonResponse({"allDateLength": machTypes.objects.all()[:].count(), "msg": pastJson})

def linSystem_machine_type_add(request):
    from .models import machTypes
    # jsonResponse = json.load(request.body)
    jsonResponse = json.loads(request.body.decode('utf-8'))
    print (jsonResponse,type(jsonResponse))
    print (jsonResponse['machTypeName'])
    dataLists = machTypes.objects.all().count()
    try:
        if(dataLists >20):
           return JsonResponse({"result": 0, "msg": "增加失败，上限为20个"})
        else:
            machTypes.objects.create(**jsonResponse)
    except :
        return JsonResponse({"result": 1, "msg": "增加失败,设备类型名重复/信息不完整"})
    else:
     return JsonResponse({"result": 0, "msg": "增加成功"})

def linSystem_machine_type_mod(request):
    from .models import machTypes
    jsonResponse = json.loads(request.body.decode('utf-8'))
    # print (jsonResponse, type(jsonResponse))
    # print (jsonResponse['machTypeId'])
    try:
        machTypes.objects.filter(machTypeId=jsonResponse['machTypeId']).update(
            machTypeName=jsonResponse['machTypeName'],
            machTypeDesc=jsonResponse['machTypeDesc'],
            machTypeCode=jsonResponse['machTypeCode'])
    except:
        return JsonResponse({"result": 1, "msg": "修改失败，设备类型名重复/信息不完整"})
    else:
        return JsonResponse({"result": 0, "msg": "修改成功"})

def linSystem_machine_type_del(request):
    from .models import machTypes
    jsonResponse = json.loads(request.body.decode('utf-8'))
    # print (jsonResponse,type(jsonResponse))
    # print (jsonResponse['machTypeId'])
    dataLists = machTypes.objects.all().count()
    try:
        if (dataLists <= 2):
            return JsonResponse({"result": 1, "msg": "删除失败,数据至少要存在2条"})
        else:
            machTypes.objects.filter(machTypeId=jsonResponse['machTypeId']).delete()
    except :
        return JsonResponse({"result":1, "msg": "删除失败"})
    else:
     return JsonResponse({"result": 0, "msg": "删除成功"})

# 客户
def linSystem_customer_get(request):
    from .models import customers
    jsonResponse = json.loads(request.body.decode('utf-8'))
    # print (jsonResponse["sendPage"])
    try:
        pastJson = queryset_to_json(customers.objects.all()[jsonResponse["sendPage"] * 10 - 10:jsonResponse["sendPage"] * 10])
    except:
        pastJson = queryset_to_json(customers.objects.all()[:])
    return JsonResponse({"allDateLength": customers.objects.all()[:].count(), "msg": pastJson})

def linSystem_customer_add(request):
    from .models import customers
    # jsonResponse = json.load(request.body)
    jsonResponse = json.loads(request.body.decode('utf-8'))
    print (jsonResponse,type(jsonResponse))
    dataLists = customers.objects.all().count()
    try:
        if(dataLists >20):
           return JsonResponse({"result": 0, "msg": "增加失败，上限为20个"})
        else:
            customers.objects.create(**jsonResponse)
    except :
        return JsonResponse({"result": 1, "msg": "增加失败，客户名重复/信息不完整"})
    else:
        return JsonResponse({"result": 0, "msg": "增加成功"})

def linSystem_customer_mod(request):
    from .models import customers
    jsonResponse = json.loads(request.body.decode('utf-8'))
    print (jsonResponse, type(jsonResponse))
    print (jsonResponse['customerId'])
    try:
        customers.objects.filter(customerId=jsonResponse['customerId']).update(
            customerName=jsonResponse['customerName'],
            customerType=jsonResponse['customerType'],
            customerLevel=jsonResponse['customerLevel'],
            sponsor=jsonResponse['sponsor'],
            phone=jsonResponse['phone'],
            address=jsonResponse['address'],
            machCount=jsonResponse['machCount'],
            remark=jsonResponse['remark']
        )
    except:
        return JsonResponse({"result": 1, "msg": "修改失败，客户名重复/信息不完整"})
    else:
        return JsonResponse({"result": 0, "msg": "修改成功"})

def linSystem_customer_del(request):
    from .models import customers
    jsonResponse = json.loads(request.body.decode('utf-8'))
    # print (jsonResponse,type(jsonResponse))
    # print (jsonResponse['id'])
    dataLists = customers.objects.all().count()
    try:
        if (dataLists <= 2):
            return JsonResponse({"result": 1, "msg": "删除失败,数据至少要保留2条"})
        else:
            customers.objects.filter(customerId=jsonResponse['customerId']).delete()
    except :
        return JsonResponse({"result": 1, "msg": "删除失败"})
    else:
     return JsonResponse({"result": 0, "msg": "删除成功"})

# 设备
def linSystem_machine_get(request):
    from .models import machines
    import time
    jsonResponse = json.loads(request.body.decode('utf-8'))
    # print (jsonResponse["sendPage"])

    lists = []
    try:
        pastJson = queryset_to_json(machines.objects.all()[jsonResponse["sendPage"] * 10 - 10:jsonResponse["sendPage"] * 10])
        # print(str(pastJson[1]['dataOfProdect']))
        # print (int(time.mktime(pastJson[1]['dataOfProdect'].timetuple())))
        #                 "machTypeName": str(pastJson[i]['machTypeName']),
        # print(pastJson[0]['machTypeId'].__dict__['machTypeName'])
        for i in range(len(pastJson)):
            lists.append({
                'machineId':pastJson[i]['machineId'],
                "machTypeId":pastJson[i]['machTypeId'].__dict__['machTypeId'],
                "machTypeName": pastJson[i]['machTypeId'].__dict__['machTypeName'],
                'machineName': pastJson[i]['machineName'],
                'machineDesc': pastJson[i]['machineDesc'],
                'dateOfProduct': time.mktime(pastJson[i]['dataOfProdect'].timetuple())*1000 + 8*60*60*1000,
                'office': pastJson[i]['office'],
                'mwordId': pastJson[i]['mwordId'],
                'customerName':str(pastJson[i]['customerName'])
            })
    except:
        pastJson = queryset_to_json(machines.objects.all()[:])
        for i in range(len(pastJson)):
            lists.append({
                'machineId':pastJson[i]['machineId'],
                "machTypeId": pastJson[i]['machTypeId'].__dict__['machTypeId'],
                "machTypeName": pastJson[i]['machTypeId'].__dict__['machTypeName'],
                'machineName': pastJson[i]['machineName'],
                'machineDesc': pastJson[i]['machineDesc'],
                'dateOfProduct': time.mktime(pastJson[i]['dataOfProdect'].timetuple())*1000 + 8*60*60*1000,
                'office': pastJson[i]['office'],
                'mwordId': pastJson[i]['mwordId'],
                'customerName':str(pastJson[i]['customerName'])
            })
    return  JsonResponse({"allDateLength": machines.objects.all()[:].count(), "msg": lists})

def linSystem_machine_add(request):
    from .models import machines,machTypes,customers
    import time
    # jsonResponse = json.load(request.body)
    jsonResponse = json.loads(request.body.decode('utf-8'))
    # print (jsonResponse,type(jsonResponse))
    # print (jsonResponse['machTypeName'])
    dataLists = machines.objects.all().count()
    machTypeGet = machTypes.objects.get(machTypeId=jsonResponse['machTypeId'])
    customerGet = customers.objects.get(customerId=jsonResponse['customerId'])
    machProductTime = time.localtime(float(jsonResponse['dateOfProduct']/1000 - 8*60*60))
    machProductTime = time.strftime('%Y-%m-%d %H:%M:%S', machProductTime)
    # print (machTypeGet,customerGet,machProductTime)
    try:
        if(dataLists >10):
           return JsonResponse({"result": 0, "msg": "增加失败"})
        else:
            machines.objects.create(machineName=jsonResponse['machineName'],
                            machTypeId=machTypeGet,
                            machineDesc=jsonResponse['machineDesc'],
                            dataOfProdect=machProductTime,
                            customerName=customerGet,
                            office=jsonResponse['office'],
                            )
    # machines.objects.create(**jsonResponse)
    except :
        return JsonResponse({"result": 1, "msg": "增加失败,设备名重复/信息不完整"})
    else:
        return JsonResponse({"result": 0, "msg": "增加成功"})

def linSystem_machine_mod(request):
    from .models import machines,machTypes,customers
    import  time
    jsonResponse = json.loads(request.body.decode('utf-8'))
    print(jsonResponse)
    try:
        machTypeGet = machTypes.objects.get(machTypeId=jsonResponse['machTypeId'])
        customerGet = customers.objects.get(customerId=jsonResponse['customerId'])
        machProductTime = time.localtime(float(jsonResponse['dateOfProduct'] / 1000 - 8 * 60 * 60))
        machProductTime = time.strftime('%Y-%m-%d %H:%M:%S', machProductTime)
        machines.objects.filter(machineId=jsonResponse['machineId']).update(
            machineName=jsonResponse['machineName'],
            machTypeId=machTypeGet,
            machineDesc=jsonResponse['machineDesc'],
            dataOfProdect=machProductTime,
            customerName=customerGet,
            office=jsonResponse['office'])
    except:
        return JsonResponse({"result": 1, "msg": "修改失败,设备名重复/信息不完整"})
    else:
        return JsonResponse({"result": 0, "msg": "修改成功"})

def linSystem_machine_del(request):
    from .models import machines
    jsonResponse = json.loads(request.body.decode('utf-8'))
    dataLists = machines.objects.all().count()
    print (dataLists)
    try:
        if (dataLists <=2):
            return JsonResponse({"result": 1, "msg": "删除失败,数据至少要存在2条"})
        else:
            machines.objects.filter(machineId=jsonResponse['machineId']).delete()
    except :
        return JsonResponse({"result": 1, "msg": "删除失败"})
    else:
     return JsonResponse({"result": 0, "msg": "删除成功"})



# 获取所有网关
def linSystem_gateways_get(request):
    from .models import  gateways_all
    pastJson = queryset_to_json(gateways_all.objects.all()[:])
    pastJson = json.dumps(pastJson, ensure_ascii=False)
    # pastJson = ["123","KSD0186701","KSD0186711","ECU-1051(2)","channel","simulation2","ECU-1051(1)","simulation1"]
    print (pastJson)
    return HttpResponse(pastJson)

# 所有机器监测点查询
def linSystem_machines_IOP_get(request):
    from .models import IOPoints
    jsonResponse = json.loads(request.body.decode('utf-8'))
    lists = []

    try:
        pastJson = queryset_to_json(IOPoints.objects.all()[jsonResponse["sendPage"] * 10 - 10:jsonResponse["sendPage"] * 10])
        for i in range(len(pastJson)):
            lists.append({
                'configId': pastJson[i]['IOPointsId'],
                'machineId': pastJson[i]['machineName'].__dict__["machineId"],
                "machineName": pastJson[i]['machineName'].__dict__["machineName"],
                'gwId': str(pastJson[i]['machineGateway']),
                # 'iop': pastJson[i]['iop'],
                'physicalName': pastJson[i]['physicalName'],
                'minLC': pastJson[i]['minRange'],
                'maxLC': pastJson[i]['maxRange'],
                'aline': str(pastJson[i]['aline']),
                'method': str(pastJson[i]['method'])
            })
    except:
        pastJson = queryset_to_json(IOPoints.objects.all()[:])
        for i in range(len(pastJson)):
            lists.append({
                'configId': pastJson[i]['IOPointsId'],
                'machineId':  pastJson[i]['machineName'].__dict__["machineId"],
                "machineName": pastJson[i]['machineName'].__dict__["machineName"],
                'gwId': str(pastJson[i]['machineGateway']),
                # 'iop': pastJson[i]['iop'],
                'physicalName': pastJson[i]['physicalName'],
                'minLC': pastJson[i]['minRange'],
                'maxLC': pastJson[i]['maxRange'],
                'aline': str(pastJson[i]['aline']),
                'method': str(pastJson[i]['method'])
            })
    return JsonResponse({"allDateLength": IOPoints.objects.all()[:].count(), "msg": lists})

def linSystem_machines_IOP_add(request):
    from .models import machines,IOPoints,gateways_all
    jsonResponse = json.loads(request.body.decode('utf-8'))
    dataLists = IOPoints.objects.all().count()
    print (jsonResponse['machineId'],jsonResponse['gwId'])
    machineNameGet = machines.objects.get(machineId=jsonResponse['machineId'])
    machineGatewayGet = gateways_all.objects.get(gatewayId=jsonResponse['gwId'])
    try:
        if(dataLists >20):
           return JsonResponse({"result": 0, "msg": "增加失败，上限为20个"})
        else:
            IOPoints.objects.create(machineName=machineNameGet,
                            machineGateway=machineGatewayGet,
                            physicalName=jsonResponse['physicalName'],
                            minRange=jsonResponse['minLC'],
                            maxRange=jsonResponse['maxLC'],
                            aline=jsonResponse['aline'],
                            method=jsonResponse['method'],
                            )
    except :
        return JsonResponse({"result": 1, "msg": "增加失败,物理名称重复/信息不完整"})
    else:
        return JsonResponse({"result": 0, "msg": "增加成功"})

def linSystem_machines_IOP_mod(request):
    from .models import machines,IOPoints,gateways_all
    jsonResponse = json.loads(request.body.decode('utf-8'))
    machinesGet = machines.objects.get(machineId=jsonResponse['machineId'])
    machineGatewayGet = gateways_all.objects.get(gatewayId=jsonResponse['gwId'])
    print (machinesGet,machineGatewayGet,jsonResponse['configId'])
    try:
        IOPoints.objects.filter(IOPointsId=jsonResponse['configId']).update(
            machineName=machinesGet,
            machineGateway=machineGatewayGet,
            minRange=jsonResponse['minLC'],
            maxRange=jsonResponse['maxLC'],
            aline=jsonResponse['aline'],
            method=jsonResponse['method'],)
    except:
        return JsonResponse({"result": 1, "msg": "修改失败,设备名重复/信息不完整"})
    else:
        return JsonResponse({"result": 0, "msg": "修改成功"})

def linSystem_machines_IOP_del(request):
    from .models import IOPoints
    jsonResponse = json.loads(request.body.decode('utf-8'))
    dataLists = IOPoints.objects.all().count()
    try:
        if (dataLists <= 2):
            return JsonResponse({"result": 1, "msg": "删除失败,数据至少要保留2条"})
        else:
            IOPoints.objects.filter(IOPointsId=jsonResponse['configId']).delete()
    except :
        return JsonResponse({"result": 1, "msg": "删除失败"})
    else:
     return JsonResponse({"result": 0, "msg": "删除成功"})


# 监测点组查询
def linSystem_iopgs_get(request):
    pastJson = [
        {
            "iopGroupId":"b5dce334",
            "iopGroupName":"温度组",
            "gwsWithIOPs":{
                "0301测试":["室外温度"],
                "02222机器":["测试压力"]
            },
            "token":""
        }]
    return JsonResponse({"result": 0, "msg": pastJson})

# 根据机器id查询物理量/监测点
def linSystem_gwIopMappingConfig_get(request):
    from .models import IOPoints,machines
    jsonResponse = json.loads(request.body.decode('utf-8'))
    # pastJson = queryset_to_json(IOPoints.objects.all()[:])
    machinesGet = machines.objects.get(machineId=jsonResponse['machineId'])
    machinePhysicalName = queryset_to_json(IOPoints.objects.all().filter(machineName=machinesGet)[:])
    pastJson = []
    for i in range(len(machinePhysicalName)):
        pastJson.append(
            {"id":machinePhysicalName[i]["IOPointsId"],"physicalName":machinePhysicalName[i]["physicalName"]}
        )
    return JsonResponse({"result": 0, "msg": pastJson})


# 异常报警
# 异常码
def linSystem_alarmCode_get(request):
    from .models import alarmCodes,machines
    jsonResponse = json.loads(request.body.decode('utf-8'))
    lists = []
    try:
        pastJson = queryset_to_json(alarmCodes.objects.all()[jsonResponse["sendPage"] * 10 - 10:jsonResponse["sendPage"] * 10])
        for i in range(len(pastJson)):
            lists.append({
                'alarmCode': pastJson[i]['alarmCodeId'],
                'alarmName': pastJson[i]['alarmCodeName'],
                'machineName': pastJson[i]['machineName'].__dict__['machineName'],
                'physicalName': str(pastJson[i]['physicalName']),
                'valueMin': pastJson[i]['minValue'],
                'valueMax': pastJson[i]['maxValue'],
                'alarmMsg': str(pastJson[i]['alarmMsg']),
                'level': str(pastJson[i]['level']),
                'timeLimit': pastJson[i]['timeLimit']
            })
    except:
       pastJson = queryset_to_json(alarmCodes.objects.all()[:])
       for i in range(len(pastJson)):
           lists.append({
               'alarmCode': pastJson[i]['alarmCodeId'],
               'alarmName': pastJson[i]['alarmCodeName'],
               'machineName': pastJson[i]['machineName'].__dict__['machineName'],
               'physicalName': str(pastJson[i]['physicalName']),
               'valueMin': pastJson[i]['minValue'],
               'valueMax': pastJson[i]['maxValue'],
               'alarmMsg': str(pastJson[i]['alarmMsg']),
               'level': str(pastJson[i]['level']),
               'timeLimit': pastJson[i]['timeLimit']
           })
    return JsonResponse({"allDateLength": alarmCodes.objects.all()[:].count(), "msg": lists})

def linSystem_alarmCodes_add(request):
    from .models import machines,IOPoints,alarmCodes
    jsonResponse = json.loads(request.body.decode('utf-8'))
    dataLists = alarmCodes.objects.all().count()
    machineNameGet = machines.objects.get(machineId=jsonResponse['machineId'])
    physicalNameGet = IOPoints.objects.get(IOPointsId=jsonResponse['configId'])
    try:
        if(dataLists >20):
           return JsonResponse({"result": 0, "msg": "增加失败,上限为20个数据"})
        else:
            alarmCodes.objects.create(
                            alarmCodeId=jsonResponse['alarmCode'],
                            alarmCodeName = jsonResponse['alarmname'],
                            machineName=machineNameGet,
                            physicalName=physicalNameGet,
                            alarmMsg=jsonResponse['alarmMsg'],
                            minValue=jsonResponse['valueMin'],
                            maxValue=jsonResponse['valueMax'],
                            level=jsonResponse['level'],
                            timeLimit=jsonResponse['timeLimit'],
                            )
    except :
        return JsonResponse({"result": 1, "msg": "增加失败,异常码名重复/信息不完整"})
    else:
        return JsonResponse({"result": 0, "msg": "增加成功"})

def linSystem_alarmCodes_mod(request):
    from .models import machines,IOPoints,alarmCodes
    jsonResponse = json.loads(request.body.decode('utf-8'))
    machineNameGet = machines.objects.get(machineId=jsonResponse['machineId'])
    physicalNameGet = IOPoints.objects.get(IOPointsId=jsonResponse['configId'])
    print (machineNameGet,physicalNameGet)
    try:
        alarmCodes.objects.filter(alarmCodeId=jsonResponse['alarmCodeId']).update(
            # alarmCodeId=jsonResponse['alarmCode'],
            alarmCodeName=jsonResponse['alarmname'],
            machineName=machineNameGet,
            physicalName=physicalNameGet,
            alarmMsg=jsonResponse['alarmMsg'],
            minValue=jsonResponse['valueMin'],
            maxValue=jsonResponse['valueMax'],
            level=jsonResponse['level'],
            timeLimit=jsonResponse['timeLimit'],)
    except:
        return JsonResponse({"result": 1, "msg": "修改失败,设备名重复/信息不完整"})
    else:
        return JsonResponse({"result": 0, "msg": "修改成功"})

def linSystem_alarmCodes_del(request):
    from .models import alarmCodes
    jsonResponse = json.loads(request.body.decode('utf-8'))
    dataLists = alarmCodes.objects.all().count()
    try:
        alarmCodes.objects.filter(alarmCodeId=jsonResponse['alarmCodeId']).delete()
    except :
        if (dataLists <= 2):
            return JsonResponse({"result": 1, "msg": "删除失败,数据至少要保留2条"})
        else:
            return JsonResponse({"result": 1, "msg": "删除失败"})
    else:
        return JsonResponse({"result": 0, "msg": "删除成功"})

# 组合异常码
def linSystem_alarmCodesGroup_get(request):
    pastJson =[{"id":17,"alarmCode":"af6f730fd358440b","alarmGroupName":"温度组异常","iopGroupId":"c35105cb","alarmMsg":"温度组异常","level":1,"timeLimit":"100s","alarmNameList":["室外温度"]}]
    return JsonResponse({"result": 0, "msg": pastJson})


# 异常记录
# 单个异常记录
def linSystem_singleAlarmCodes_get(request):
    from .models import singleAlarmCodes,machines,alarmCodes,IOPoints
    import time
    jsonResponse = json.loads(request.body.decode('utf-8'))
    print (jsonResponse["sendPage"],jsonResponse["machineId"])
    lists = []
    try:
        dataQuerySet=singleAlarmCodes.objects.all()[:].filter(machineName_id =jsonResponse["machineId"])[jsonResponse["sendPage"] * 10 - 10:jsonResponse["sendPage"] * 10]
        for i in dataQuerySet:
            dataDict = i.__dict__
            print(dataDict)
            machineNameGet = machines.objects.all().get(machineId =dataDict["machineName_id"]).__dict__["machineName"]
            # print (machineNameGet,type(machineNameGet))
            physicalNameIdGet = alarmCodes.objects.all().get(alarmCodeId =dataDict["alarmCodeName_id"]).__dict__["physicalName_id"]
            physicalNameGet = IOPoints.objects.all().get(IOPointsId =physicalNameIdGet).__dict__['physicalName']
            alarmNameGet = alarmCodes.objects.all().get(alarmCodeId=dataDict["alarmCodeName_id"]).__dict__["alarmCodeName"]
            alarmMsgGet = alarmCodes.objects.all().get(alarmCodeId=dataDict["alarmCodeName_id"]).__dict__["alarmMsg"]
            levelGet = alarmCodes.objects.all().get(alarmCodeId=dataDict["alarmCodeName_id"]).__dict__["level"]
            print (physicalNameGet,alarmNameGet,alarmMsgGet,levelGet)
            # alarmStartTime = time.localtime(float(dataDict["startTime"] / 1000 - 8 * 60 * 60))
            # print (alarmStartTime)
            # alarmStartTime = time.strftime('%Y-%m-%d %H:%M:%S', alarmStartTime)
            # print (alarmStartTime)
            lists.append({
                            'alarmId':dataDict["singleAlarmCodeId"],
                            'machineId': dataDict["machineName_id"],
                            'machineName': machineNameGet,
                            'physicalName': physicalNameGet,
                            'alarmCode':dataDict["alarmCodeName_id"],
                            'alarmName': alarmNameGet,
                            'alarmMsg': alarmMsgGet,
                            'startTime':time.mktime(dataDict["startTime"].timetuple())*1000 ,
                            'duration': dataDict["duration"],
                            'level': levelGet,
                            'status': dataDict["singleAlarmCodeStatus"],
                        })
    except:
        return JsonResponse({"allDateLength": 0, "msg": "出现未知错误"})
    return JsonResponse({"allDateLength": singleAlarmCodes.objects.all()[:].filter(machineName_id =jsonResponse["machineId"]).count(), "msg": lists})

#  单个异常记录初始化
def linSystem_singleAlarmCodes_init(request):
    from .models import singleAlarmCodes,alarmProcessHistory
    try:
        singleAlarmCodes.objects.all()[:].update(singleAlarmCodeStatus=0)
        alarmProcessHistory.objects.create(
            callbackMsg='初始化异常记录状态',
        )
    except:
        return JsonResponse({"result": 1, "msg": "初始化失败"})
    else:
        return JsonResponse({"result": 0, "msg": "初始化成功"})



# 解决方案
def linSystem_solution_get(request):
    from .models import alarmSolutons
    jsonResponse = json.loads(request.body.decode('utf-8'))
    pastJson = queryset_to_json(alarmSolutons.objects.all()[jsonResponse["sendPage"]*10-10:jsonResponse["sendPage"]*10])
    return JsonResponse({"allDateLength": alarmSolutons.objects.all()[:].count(), "msg": pastJson})
    # return HttpResponse(pastJson)

def linSystem_solution_add(request):
    from .models import alarmSolutons
    # jsonResponse = json.load(request.body)
    jsonResponse = json.loads(request.body.decode('utf-8'))
    # print (jsonResponse,type(jsonResponse['alarmCodeList']))
    dataLists = alarmSolutons.objects.all().count()
    try:
        if(dataLists >20):
           return JsonResponse({"result": 0, "msg": "增加失败,数目不能超过20"})
        else:
            alarmSolutons.objects.create(**jsonResponse)
    except :
        return JsonResponse({"result": 1, "msg": "增加失败,名称重复/信息不完整"})
    else:
        return JsonResponse({"result": 0, "msg": "增加成功"})

def linSystem_solution_mod(request):
    from .models import alarmSolutons
    jsonResponse = json.loads(request.body.decode('utf-8'))
    print (jsonResponse, type(jsonResponse))
    try:
        alarmSolutons.objects.filter(alarmSolutonId=jsonResponse['alarmSolutonId']).update(
            alarmSolutonName=jsonResponse['alarmSolutonName'],
            alarmSolutonDetail=jsonResponse['alarmSolutonDetail'],
            alarmCodeList=jsonResponse['alarmCodeList'],
        )
    except:
        return JsonResponse({"result": 1, "msg": "修改失败，名称重复/信息不完整"})
    else:
        return JsonResponse({"result": 0, "msg": "修改成功"})

def linSystem_solution_del(request):
    from .models import alarmSolutons
    jsonResponse = json.loads(request.body.decode('utf-8'))
    # print (jsonResponse,type(jsonResponse))
    # print (jsonResponse['id'])
    dataLists = alarmSolutons.objects.all().count()
    try:
        alarmSolutons.objects.filter(alarmSolutonId=jsonResponse['alarmSolutonId']).delete()
    except :
        if (dataLists <= 2):
            return JsonResponse({"result": 1, "msg": "删除失败,数据至少要保留2条"})
        else:
            return JsonResponse({"result": 1, "msg": "删除失败"})
    else:
        return JsonResponse({"result": 0, "msg": "删除成功"})


#  故障处理接口
def linSystem_alarmProcess(request):
    from .models import singleAlarmCodes,alarmProcessHistory,alarmCodes
    jsonResponse = json.loads(request.body.decode('utf-8'))
    print (jsonResponse,type(jsonResponse))
    # print ("+++++++++++++++++++")
    # pastJson = queryset_to_json(singleAlarmCodes.objects.all())
    # print (pastJson, type(pastJson))
    # aa = alarmCodes.objects.all()[:].get(alarmCodeId=jsonResponse["alarmCode"]).__dict__["alarmCodeName"]
    # print ("____+++++")
    # print (aa,type(aa))
    try:
        singleAlarmCodes.objects.all()[:].filter(singleAlarmCodeId=jsonResponse["singleAlarmCodeId"]).update(singleAlarmCodeStatus=jsonResponse["status"])
        alarmCodeNameGet = alarmCodes.objects.all()[:].get(alarmCodeId=jsonResponse["alarmCode"]).__dict__["alarmCodeName"]
        alarmProcessHistory.objects.create(
            machineName=jsonResponse["macName"],
            callbackMsg=jsonResponse["feedback"],
            alarmCode= jsonResponse["alarmCode"],
            alarmCodeName= alarmCodeNameGet,
            alarmSolutonId= jsonResponse["solveId"],
        )
    except:
        return JsonResponse({"result": 1, "msg": "处理失败"})
    else:
        return JsonResponse({"result": 0, "msg": "处理成功"})


#  故障处理历史
def linSystem_alarmProcess_history(request):
    from .models import alarmProcessHistory
    import time
    lists = []
    jsonResponse = json.loads(request.body.decode('utf-8'))
    pastJson = queryset_to_json(alarmProcessHistory.objects.all()[jsonResponse["sendPage"] * 10 - 10:jsonResponse["sendPage"] * 10])
    # print (pastJson,type(pastJson))
    for i in range(len(pastJson)):
        lists.append(
            {
                # 'machineId': pastJson[i]["machineId"],
                'alarmCode': pastJson[i]["alarmCode"],
                'alarmCodeName': pastJson[i]["alarmCodeName"],
                'alarmSolutonId': str(pastJson[i]["alarmSolutonId"]),
                'callbackMsg': pastJson[i]["callbackMsg"],
                'processTime': time.mktime(pastJson[i]["processTime"].timetuple())*1000 ,
                'machineName': pastJson[i]["machineName"],
            }
        )
    # print (lists)
    return JsonResponse({"allDateLength": alarmProcessHistory.objects.all()[:].count(), "msg": lists})