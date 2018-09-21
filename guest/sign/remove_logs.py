import os, datetime, time
import logging

log = logging.getLogger('log')


def TimeStampToTime(timestamp):
    """格式化时间"""
    timeStruct = time.localtime(timestamp)
    return str(time.strftime('%Y-%m-%d', timeStruct))


def remove_logs():
    """到期删除日志文件"""
    dir_list = ['logs']  # 要删除文件的目录名
    for dir in dir_list:
        dirPath = os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '\\' + dir  # 拼接删除目录完整路径
        file_list = os.listdir(dirPath)  # 返回目录下的文件list
        log.info(file_list)
        if file_list:
            for i in file_list:
                file_path = os.path.join(dirPath, i)  # 拼接文件的完整路径
                t_list = TimeStampToTime(os.path.getctime(file_path)).split('-')
                now_list = TimeStampToTime(time.time()).split('-')
                t = datetime.datetime(int(t_list[0]), int(t_list[1]), int(t_list[2]))  # 将时间转换成datetime.datetime 类型
                now = datetime.datetime(int(now_list[0]), int(now_list[1]), int(now_list[2]))
                if (now - t).days > 6 or os.path.getsize(file_path) > 1048576:  # 时间大于6天，大小大于5m删除
                    pass
                    # os.remove(file_path)
            if len(file_list) > 9:
                file_list = file_list[0:-6]
                for i in file_list:
                    file_path = os.path.join(dirPath, i)  # 拼接文件的完整路径
                    # os.remove(file_path)


remove_logs()
