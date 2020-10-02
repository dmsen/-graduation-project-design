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
