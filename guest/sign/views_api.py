from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError, ObjectDoesNotExist  # 验证错误
from django.db.utils import IntegrityError  # 完整性错误
from django.db.models import Q  # 与或非 查询
import time
import logging
from sign.models import Event, Guest

log = logging.getLogger('log')


# 添加发布会接口
def add_event(request):
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


# 查询发布会接口
def get_event_list(request):
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


# 添加嘉宾接口
def add_guest(request):
    eid = request.POST.get('eid', '')  # 关联发布会id
    realname = request.POST.get('realname', '')  # 姓名
    phone = request.POST.get('phone', '')  # 手机号
    email = request.POST.get('email', '')  # 邮箱
    if eid == '' or realname == '' or phone == '':
        log.info('参数错误，不能为空.')
        return JsonResponse({'status': 10021, 'message': 'parameter error'})
    result = Event.objects.filter(id=eid)
    if not result:
        log.info('关联Event id 为 null.')
        return JsonResponse({'status': 10022, 'message': 'event id null'})
    result = Event.objects.get(id=eid).status
    if not result:
        log.info('Event 状态未激活.')
        return JsonResponse({'status': 10023, 'message': 'event status is not available'})

    event_limit = Event.objects.get(id=eid).limit  # 限制人数
    guest_limit = Guest.objects.filter(event_id=eid)  # 发布会已添加的嘉宾数
    if len(guest_limit) >= event_limit:
        log.info('参加发布会的人已满.')
        return JsonResponse({'status': 10024, 'message': 'event number is full'})

    event_time = Event.objects.get(id=eid).start_time  # 发布会时间
    etime = str(event_time).split('+')[0]
    log.info(etime)
    timeArray = time.strptime(etime, '%Y-%m-%d %H:%M:%S')
    e_time = int(time.mktime(timeArray))
    log.info(e_time)

    now_time = str(time.time())  # 当前时间
    ntime = now_time.split('.')[0]
    now_time = int(ntime)
    log.info(now_time)

    if now_time >= e_time:
        log.info('活动已开始.')
        return JsonResponse({'status': 10025, 'message': 'event has started'})
    try:
        Guest.objects.create(realname=realname, phone=int(phone), email=email, sign=0, event_id=int(eid))
    except IntegrityError:
        log.info('手机号输入有误.')
        return JsonResponse({'status': 10026, 'message': 'the event guest phone number repeat'})
    log.info('嘉宾添加成功！')
    return JsonResponse({'status': 200, 'message': 'add guest success'})


# 查询嘉宾接口
def get_guest_list(request):
    name = request.GET.get('name', '')

    if name == '':
        datas = []
        results = Guest.objects.all()
        if results:
            for r in results:
                guest = {}
                event = Event.objects.get(id=r.event_id)
                guest['realname'] = r.realname
                guest['phone'] = r.phone
                guest['email'] = r.email
                guest['sign'] = r.sign
                guest['event_name'] = event.name
                datas.append(guest)
            log.info('查询嘉宾成功！')
            return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
    else:
        results = Guest.objects.filter(Q(phone__contains=name) | Q(realname__contains=name))  # guest 表中查询
        if results:
            datas = []
            for r in results:
                guest = {}
                event = Event.objects.get(id=r.event_id)
                guest['realname'] = r.realname
                guest['phone'] = r.phone
                guest['email'] = r.email
                guest['sign'] = r.sign
                guest['event_name'] = event.name
                datas.append(guest)
            log.info('查询嘉宾成功！')
            return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
        else:
            id_results = Event.objects.filter(name__contains=name)  # event 表联查
            if id_results:
                datas = []
                for event_id in id_results:
                    results = Guest.objects.filter(event_id=event_id)
                    for r in results:
                        if r:
                            guest = {}
                            event = Event.objects.get(id=r.event_id)
                            guest['realname'] = r.realname
                            guest['phone'] = r.phone
                            guest['email'] = r.email
                            guest['sign'] = r.sign
                            guest['event_name'] = event.name
                            datas.append(guest)
                log.info('查询嘉宾成功！')
                return JsonResponse({'status': 200, 'message': 'success', 'data': datas})
            else:
                log.info('查询结果为空.')
                return JsonResponse({'status': 10022, 'message': 'query result is empty'})


# 签到接口
def user_sign(request):
    eid = request.POST.get('eid', '')  # 发布会id
    phone = request.POST.get('phone', '')  # 嘉宾手机号

    if eid == '' or phone == '':
        log.info('参数错误，不能为空.')
        return JsonResponse({'status': 10021, 'message': 'parameter error'})

    result = Event.objects.filter(id=eid)
    if not result:
        return JsonResponse({'status': 10022, 'message': 'event id null'})

    result = Event.objects.get(id=eid).status
    if not result:
        log.info('Event 状态未激活.')
        return JsonResponse({'status': 10023, 'message': 'event status is not available'})

    event_time = Event.objects.get(id=eid).start_time  # 发布会时间
    etime = str(event_time).split('+')[0]
    log.info(etime)
    timeArray = time.strptime(etime, '%Y-%m-%d %H:%M:%S')
    e_time = int(time.mktime(timeArray))
    log.info(e_time)

    now_time = str(time.time())  # 当前时间
    ntime = now_time.split('.')[0]
    now_time = int(ntime)
    log.info(now_time)

    if now_time >= e_time:
        log.info('活动已开始.')
        return JsonResponse({'status': 10024, 'message': 'event has started'})

    result = Guest.objects.filter(phone=phone)
    if not result:
        log.info('嘉宾手机号不存在.')
        return JsonResponse({'status': 10025, 'message': 'user phone null'})

    result = Guest.objects.filter(event_id=eid, phone=phone)
    if not result:
        log.info('嘉宾签到发布会和参加发布会不符.')
        return JsonResponse({'status': 10026, 'message': 'user did not participate in the conference'})
    result = Guest.objects.get(event_id=eid, phone=phone).sign
    if result:
        log.info('嘉宾已签到.')
        return JsonResponse({'status': 10027, 'message': 'user has sign in'})
    else:
        Guest.objects.filter(event_id=eid, phone=phone).update(sign='1')
        return JsonResponse({'status': 200, 'message': 'sign success'})
