from django.shortcuts import render
from .models import Request_parameter
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth import logout, authenticate, login
import time
import requests
import logging
import re

logger = logging.getLogger('log')


def home(request):
    # header = {
    #     "Content-Type": "application/json",
    #     "channel": "SHOP",
    #     "uid": "91",
    #     "ukey": "d3f9aa380054b5f45b4d2b2df6447c62"
    # }
    if request.method == 'GET':
        return render(request, 'api/api.html')
    else:
        url = request.POST.get('url', '')
        method = request.POST.get('method', '')
        params = request.POST.get('params', '')
        header = request.POST.get('header', '')
        body = request.POST.get('body', '')
        verify = False
        if 'http' not in url:
            logger.error('url参数错误')
            return render(request, 'api/api.html', {'error': 'url参数错误'})
        if method.lower() not in ['post', 'get', 'delete', 'put']:
            logger.error('method参数错误')
            return render(request, 'api/api.html', {'error': 'method参数错误'})
        if 'http' in url and method != '':
            request_parameter = Request_parameter.create_comment(url=url, method=method, params=params, header=header,
                                                                 body=body, verify=verify)
            request_parameter.save()
            logger.info('请求参数保存成功！')
        if header != '':
            header = eval(header)
        if params != '':
            params = eval(params)
        if body != '':
            body = eval(body)
        s = requests.session()
        try:
            res = s.request(method=method,
                            url=url,
                            params=params,
                            headers=header,
                            data=body,
                            verify=verify)
            response_code = res.status_code
            response_headers = res.headers
            response_body = res.text
            request_url = res.url
            logger.info(
                'response_body: {}\nrequest_url: {}\nresponse_code: {}\nresponse_headers: {}'.format(
                    response_body[:255], request_url, response_code, response_headers))
            return render(request, 'api/api.html',
                          {'response_code': response_code, 'response_headers': response_headers,
                           'response_body': response_body, 'request_url': request_url})
        except Exception as error:
            logger.error('请求发送错误: {}'.format(error))
            return render(request, 'api/api.html', {'error': error})
