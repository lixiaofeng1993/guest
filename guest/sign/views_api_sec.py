from django.contrib import auth as django_auth
import base64
import hashlib
from django.http import JsonResponse, HttpResponse
from sign.models import Event, Guest
from django.core.exceptions import ValidationError, ObjectDoesNotExist  # 验证错误
from django.db.utils import IntegrityError  # 完整性错误
from django.db.models import Q  # 与或非 查询
import time
import logging

log = logging.getLogger('log')


# 添加发布会接口-增加签名和时间戳
def add_event_encode(request):
    sign_result = user_sign_api(request)
    if sign_result == 'error':
        return JsonResponse({'status': 10011, 'message': 'request error'})
    elif sign_result == 'sign null':
        return JsonResponse({'status': 10012, 'message': 'user sign null'})
    elif sign_result == 'timeout':
        return JsonResponse({'status': 10013, 'message': 'user sign timeout'})
    elif sign_result == 'sign fail':
        return JsonResponse({'status': 10014, 'message': 'user sign fail'})

    eid = request.POST.get('eid', '')  # 发布会id
    name = request.POST.get('name', '')  # 发布会标题
    limit = request.POST.get('limit', '')  # 限制人数
    status = request.POST.get('status', '')  # 状态
    address = request.POST.get('address', '')  # 地址
    start_time = request.POST.get('start_time', '')  # 发布会时间

    if eid == '' or name == '' or limit == '' or status == '' or address == '' or start_time == '':
        log.info('参数错误，不能为空.')
        return JsonResponse({'status': 10021, 'message': 'parameter error'})
    result = Event.objects.filter(id=eid)
    if result:
        log.info('发布会id已经存在.')
        return JsonResponse({'status': 10022, 'message': 'event id already exists'})
    result = Event.objects.filter(name=name)
    if result:
        log.info('发布会名称已经存在.')
        return JsonResponse({'status': 10023, 'message': 'event name already exists'})
    if status == '':
        status = 1
    try:
        Event.objects.create(id=eid, name=name, limit=limit, address=address, status=int(status), start_time=start_time)
    except ValidationError as e:
        error = 'start_time format error.It must be in YYYY-MM-DD HH:MM:SS format. error: {}'.format(e)
        log.info('开始时间格式错误.')
        return JsonResponse({'status': 10024, 'message': error})
    log.info('发布会添加成功！')
    return JsonResponse({'status': 200, 'message': 'add event success'})


# 查询发布会接口--增加用户认证
def get_event_list_encode(request):
    auth_result = user_auth(request)  # 认证函数
    if auth_result == 'null':
        return JsonResponse({'status': 10011, 'message': 'user auth null'})
    if auth_result == 'fail':
        return JsonResponse({'status': 10012, 'message': 'user auth fail'})

    eid = request.GET.get('eid', '')  # 发布会id
    name = request.GET.get('name', '')  # 发布会名称

    if eid == '' and name == '':
        log.info('参数错误，不能为空.')
        return JsonResponse({'status': 10021, 'message': 'parameter error'})
    if eid != '':
        event = {}
        try:
            result = Event.objects.get(id=eid)
        except ObjectDoesNotExist:
            log.info('查询结果为空.')
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})
        else:
            event['name'] = result.name
            event['limit'] = result.limit
            event['status'] = result.status
            event['address'] = result.address
            event['start_time'] = result.start_time
            log.info('查询嘉宾成功！')
            return JsonResponse({'status': 200, 'message': 'success', 'data': event})

    if name != '':
        datas = []
        results = Event.objects.filter(name__contains=name)
        if results:
            for r in results:
                event = {}
                event['name'] = r.name
                event['limit'] = r.limit
                event['status'] = r.status
                event['address'] = r.address
                event['start_time'] = r.start_time
                datas.append(event)
                log.info('查询发布会成功！')
            return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
        else:
            log.info('查询结果为空.')
            return JsonResponse({'status': 10022, 'message': 'query result is empty'})


# 用户认证-提取出用户数据，并判断其正确性
def user_auth(request):
    get_http_auth = request.META.get('HTTP_AUTHORIZATION',
                                     'b')  # request.META 一个dict，包含HTTP请求的header信息 HTTP_AUTHORIZATION 获取HTTP认证数据，为空，返回bytes对象 返回值例如: Basic YWRtaW46YW4xMjM0NTY=
    log.info(get_http_auth)
    auth = get_http_auth.split()  # 拆分成list
    log.info(auth)
    try:
        auth_parts = base64.b64decode(auth[1]).decode('utf-8').partition(
            ':')  # 取出加密串，通过base64解密 partition()方法以冒号为分隔符对字符串进行拆分 元组
        log.info(auth_parts)
    except IndexError:
        return 'null'
    username, password = auth_parts[0], auth_parts[2]
    user = django_auth.authenticate(username=username, password=password)
    log.info(user)
    if user is not None:
        django_auth.login(request, user)
        return 'success'
    else:
        return 'fail'


# 用户签名+时间戳
def user_sign_api(request):
    if request.method == 'POST':
        client_time = request.POST.get('time', '')  # 客户端时间戳
        client_sign = request.POST.get('sign', '')  # 客户端签名
        print(client_time)
        print(client_sign)
    else:
        return 'error'

    if client_sign == '' and client_time == '':
        return 'sign null'

    # 服务器时间
    now_time = time.time()
    server_time = str(now_time).split('.')[0]
    # 获取时间差
    time_difference = int(server_time) - int(client_time)
    if time_difference >= 60:
        return 'timeout'

    # 签名检查
    md5 = hashlib.md5()
    sign_str = client_time + '&Guest-Bugmaster'
    sign_bytes_utf8 = sign_str.encode(encoding='utf-8')
    md5.update(sign_bytes_utf8)
    server_sign = md5.hexdigest()
    log.info(server_sign)

    if server_sign != client_sign:
        return 'fail'
    else:
        return 'sign success'
