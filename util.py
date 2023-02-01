import time
import datetime
import chardet
import json
import os

# 分析文件的编码类型 gb utf8
def checkencodingtype(file):
    with open(file, 'rb') as f:
        data = f.read()
        encoding_type = chardet.detect(data)
        print(encoding_type)


# 字符串list 连接成单个字符串
def list2str(l):
    temp = ""
    for i in l:
        temp += i + ","
    return temp.strip(",")


# 逗号分割的字符串添加双引号  1,2,3  "1","2","3"
def addquotes4list(s):
    temp = s.split(',')
    temp2 = ""
    for ss in temp:
        temp2 += '"' + ss + '",'
    return temp2.strip(',')


def getdate():
    temp = datetime.datetime.now().isoformat()
    return temp[0:19] + "+08:00"


def gettime():
    return datetime.datetime.now().strftime('%H:%M:%S')


# 文件，gb字符转化为utf-8字符
def gb2utf8(path):
    f = open(path)
    content = f.read()
    with open(path, 'w', encoding='utf-8') as f2:
        f2.write(content)
    f.close()


# 以uft-8格式加载 config.json 文件
def loadconfig():
    with open("config.json", "r", encoding='UTF-8') as f:
        return json.load(f)


# win路径转化为cyg路径
def winpath2cygpath(winpath):
    return "/cygdrive/" + winpath.replace(":", "").replace("\\", "/")


def isodate2date_time(isodate):
    date = isodate[0:10]
    time = isodate[11:19]
    return date + '   ' + time


def date_time2isodate(date_time):
    return date_time[0:10] + "T" + date_time[13:21] + "+08:00"


# 判断字符串是否为ipv4地址，可以插入空格
# 192.168.1.1    或 192.168.1.1:65535
def isIP(ip_str):
    ip_str = ip_str.replace(" ", "")
    ip_list = ip_str.split(".")  # 将字符串按点分割成列表
    if len(ip_list) != 4:
        return False
    for i in range(3):
        if not (ip_list[i].isdigit() and 0 <= int(ip_list[i]) <= 255):
            return False
    if ':' in ip_list[3]:
        ip4_list = ip_list[3].split(":")
        if not (ip4_list[0].isdigit() and 0 <= int(ip4_list[0]) <= 255):
            return False
        if not (ip4_list[1].isdigit() and 0 <= int(ip4_list[1]) <= 65535):
            return False
    elif not (ip_list[3].isdigit() and 0 <= int(ip_list[3]) <= 255):
            return False
    return True

# 输入 192.168.1.1 或 192.168.1.1:8090
# 输出 192.168.1.1
def getIPonly(ip_str):
    if isIP(ip_str):
        ip_list = ip_str.split('.')
        if ':' in ip_list[3]:
            ip_list[3] = ip_list[3].split(':')[0]
            return '.'.join(ip_list)
        else:
            return ip_str
    else:
        return False


def islocalpath(path_str):
    if os.path.exists(path_str):
        return os.path.basename(path_str)
    else:
        return False

def ishttppath(path_str):
    path_str = path_str.replace(' ','')
    if len(path_str) > 7 and path_str[0:7]=='http://' and '/' in path_str[7:] and isIP(get_in_between(path_str,'//','/')):
        tmp_list = path_str.split('/')
        return tmp_list[-1]
    else:
        return False

def iswebsitepath(path_str):
    path_str = path_str.replace(' ', '')
    if len(path_str) > 7 and path_str[0:7]=='/image/':
        tmp_list = path_str.split('/')
        return tmp_list[-1]
    else:
        return False

# 返回两个字符串中间的字符
def get_in_between(src, front, after):
    len1 = len(src)
    len2 = len(front)
    len3 = len(after)
    left = 0
    right = 0
    for i in range(len1 - len2 + 1):
        if src[i] == front[0] and src[i:i + len2] == front:
            left = i + len2
            break
    for i in range(len1 - len3 + 1):
        if i > left and src[i] == after[0] and src[i:i + len3] == after:
            right = i
            break
    return src[left:right].strip(" ")
