import unittest, hashlib
import requests, time


class GetEventListTest(unittest.TestCase):
    """查询发布会信息（带用户认证）"""

    def test_get_event_list(self):
        """查询成功"""
        auth_user = ('lixiaofeng', 'fengzi802300')
        r = requests.get('http://localhost:8000/api/get_event_list_encode/', auth=auth_user, params={'eid': 1})
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'success')


class AddEventTest(unittest.TestCase):
    def setUp(self):
        self.url = 'http://localhost:8000/api/add_event_encode/'
        # apikey
        self.api_key = '&Guest-Bugmaster'
        # 当前时间
        now_time = time.time()
        self.client_time = str(now_time).split('.')[0]
        # sign
        md5 = hashlib.md5()
        sign_str = self.client_time + self.api_key
        sign_bytes_utf8 = sign_str.encode(encoding='utf-8')
        md5.update(sign_bytes_utf8)
        self.sign_md5 = md5.hexdigest()

    def test_add_event_success(self):
        """添加成功"""
        payload = {"eid": "16", "name": "一加8手机发布会", "limit": 2000, "status": "0", "address": "深圳宝体会展中心",
                   "start_time": "2018-09-15 22:40:00", 'time': self.client_time, 'sign': self.sign_md5}
        r = requests.post(self.url, data=payload)
        result = r.json()
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'add event success')


if __name__ == '__main__':
    unittest.main()
