import time
import datetime
import chardet


def checkencodingtype(file):
    with open(file, 'rb') as f:
        data = f.read()
        encoding_type = chardet.detect(data)
        print(encoding_type)


def list2str(l):
    temp = ""
    for i in l:
        temp += i + ","
    return temp.strip(",")


def addquotes4list(s):
    temp = s.split(',')
    temp2 = ""
    for ss in temp:
        temp2 += '"' + ss + '",'
    return temp2.strip(',')


def getdate():
    temp = datetime.datetime.now().isoformat()
    return temp[0:19] + "+08:00"


def gb2utf8(path):
    f = open(path)
    content = f.read()
    with open(path, 'w', encoding='utf-8') as f2:
        f2.write(content)
    f.close()


