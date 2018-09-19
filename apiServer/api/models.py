from django.db import models


class Request_parameter(models.Model):
    # url
    url = models.CharField(max_length=50)
    # 请求方式
    method = models.CharField(max_length=11)
    # 参数
    params = models.TextField()
    # 参数
    body = models.TextField()
    # 请求头
    header = models.TextField()
    # 证书认证
    verify = models.TextField()

    class Meta:
        db_table = 'request_parameter'

    @classmethod
    def create_comment(cls, url, method, params, body, header, verify):
        u = cls(url=url, method=method, params=params, body=body, header=header, verify=verify)
        return u
