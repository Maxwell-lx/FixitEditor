import json


# 头文件以：冒号+空格为分割
#         除了menu功能以外，其他功能均单行存在
#         加载范围：从title到menu

def _getstrvalue(s):
    temp = s.split(': ')[1]
    return temp.split('"')[1]


def _getliststrvalue(ss):
    temp = ss.split('"')
    temp2 = []
    for i in range(len(temp)):
        if i % 2 == 1:
            temp2.append(temp[i])
    return temp2


def _getboldvalue(s):
    return s.split(': ')[1]


def head2json(h):
    head_list = h.split('---\n')
    head = head_list[1].split('\n')
    abstract = head_list[2]
    title = _getstrvalue(head[0])
    subtitle = _getstrvalue(head[1])
    description = _getstrvalue(head[2])
    keywords = _getliststrvalue(head[3])
    tags = _getliststrvalue(head[4])
    categories = _getliststrvalue(head[5])
    featuredImage = _getstrvalue(head[6])
    hiddenFromHomePage = _getboldvalue(head[8])
    pageStyle = _getstrvalue(head[9])
    password = _getboldvalue(head[10])
    message = _getstrvalue(head[11])
    author = _getstrvalue(head[12])
    date = _getboldvalue(head[13])
    lastmod = _getboldvalue(head[14])
    license_ = _getstrvalue(head[15])
    menu_flag = head[16]
    if menu_flag == "#menu_y":
        menu = _getstrvalue(head[20])
    else:
        menu = ""
    dict_ = {"abstract": abstract,
             "title": title,
             "subtitle": subtitle,
             "description": description,
             "keywords": keywords,
             "tags": tags,
             "categories": categories,
             "featuredImage": featuredImage,
             "hiddenFromHomePage": hiddenFromHomePage,
             "pageStyle": pageStyle,
             "password": password,
             "message": message,
             "author": author,
             "date": date,
             "lastmod": lastmod,
             "license": license_,
             "menu": menu
             }
    return dict_
    # # 写入json
    # json_str = json.dumps(dict, indent=4, ensure_ascii=False)
    # with open('test_data.json', 'w') as json_file:
    #     json_file.write(json_str)
    # # 读取json文件
    # with open("test_data.json", "r") as f:
    #     data = json.load(f)
    #     print(data)
