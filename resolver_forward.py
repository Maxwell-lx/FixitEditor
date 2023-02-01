# tmp.md中，短代码格式
# ---关键词
# #参数1
# #参数2
# 内容（多行）
# ---
# bilibili BV号
# highlight "linenos=table,hl_lines=8 15-17,linenostart=199"
# image src title width
# admonition type title open
# link href content download
import util as ut

keywords = {
    'bilibili': {'para_num': 1,
                 'content': False,
                 'default_para': ["BV1ou41197zy"],
                 'resolve': "{{< bilibili $0 >}}"},
    'high': {'para_num': 1,
             'content': True,
             'default_para': ["text"],
             'resolve': '{{< highlight $0 "linenos=table,hl_lines=0,linenostart=1" >}}\n$c\n{{< /highlight >}}'},
    'merm': {'para_num': 0,
             'content': True,
             'default_para': [""],
             'resolve': "{{< mermaid >}}\n$c\n{{< /mermaid >}}"},
    'typeit': {'para_num': 0,
               'content': True,
               'default_para': [""],
               'resolve': "{{< typeit >}}\n$c\n{{< /typeit >}}"},
    # 'image': {'para_num': 3,
    #           'content': False,
    #           'default_para': ["", "image", "400"],
    #           'resolve': '{{< image src="$0" caption="$1" width=$2 linked=false >}}'},
    'echart': {'para_num': 0,
               'content': True,
               'default_para': [""],
               'resolve': "{{< echart >}}\n$c\n{{< /echart >}}"},
    'quote': {'para_num': 0,
              'content': True,
              'default_para': [""],
              'resolve': "{{< center-quote >}}\n$c\n{{< /center-quote >}}"},
    'admon': {'para_num': 2,
              'content': True,
              'default_para': ["tip", 'title'],
              'resolve': '{{< admonition type=$0 title="$1" open=true >}}\n$c\n{{< /admonition >}}'},
    'link': {'para_num': 3,
             'content': False,
             'default_para': ["", "超链接内容", ""],
             'resolve': '{{< link href="$0" content=$1 card=true download="$2" >}}'}}


# 将tmp.md的内容解析到local编辑器
def resolver_forward(tmp):
    # 长文本转化为list
    tmp_list = tmp.split('\n')
    # 行 mask，1. ```关键词 开头和```结尾 2. md原版图片格式 ![$1]($2)
    list_mask = []
    flag = False
    for i in range(len(tmp_list)):
        line = tmp_list[i].replace(" ", "")
        # 第一类
        if len(line) > 3 and line[0:3] == "```" and line[3:] in list(keywords.keys()):
            word = line[3:]
            list_mask.append(word)
            flag = word
        elif len(line) == 3 and line == "```" and flag is not False:
            list_mask.append(flag)
            flag = False
        elif len(line) > 5 and (line[0:2] == "![") and ("](" in line) and (")" in line):
            list_mask.append('image')
        else:
            list_mask.append(flag)

    # print(list_mask)
    # 根据mask的类型进行解析
    new_list = []
    buffer_list = []
    word = ""
    # 对image进行解析
    for i in range(len(tmp_list)):
        if "image" == list_mask[i]:
            list_mask[i] = False
            if '"' in tmp_list[i]:
                title = ut.get_in_between(tmp_list[i], "![", '](').replace(" ", "")
                url = ut.get_in_between(tmp_list[i], '](', '"').replace(" ", "")
                width = ut.get_in_between(tmp_list[i], '"', '"').replace(" ", "")
                tmp_list[i] = '{{< image src="' + url + '" caption="' + title + '" width=' + width + ' linked=false >}}'
            else: #默认宽度400
                title = ut.get_in_between(tmp_list[i], "![", '](').replace(" ", "")
                url = ut.get_in_between(tmp_list[i], '](', ")").replace(" ", "")
                tmp_list[i] = '{{< image src="' + url + '" caption="' + title + '" width=400 linked=false >}}'
    # 通用解析
    for i in range(len(tmp_list)):
        if list_mask[i] == False:
            new_list, word, buffer_list = resolve_buffer(new_list, word, buffer_list)
            new_list.append(tmp_list[i])
        else:
            buffer_list.append(tmp_list[i])
            word = list_mask[i]
    new_list, word, buffer_list = resolve_buffer(new_list, word, buffer_list)

    # 解析完成,拼接
    return "\n".join(new_list)


# 解析buffer
def resolve_buffer(new_list, word, buffer_list):
    if len(buffer_list) > 0:
        new_list.append(forward_word(buffer_list, keywords[word]))
        word = ""
        buffer_list = []
    return new_list, word, buffer_list


# 剪掉两端
def forward_preprocess(_list):
    if len(_list) > 0:
        _list.pop()  # 尾
    if len(_list) > 0:
        _list.pop(0)  # 头
    return _list


def forward_word(content_list, word_dict):
    content_list = forward_preprocess(content_list)
    # 读取参数,并替换到解析字符串
    re_str = word_dict["resolve"]
    last_index = 0
    for i in range(word_dict["para_num"]):
        if len(content_list) > i:
            para = content_list[i].lstrip(" ")
        if len(content_list) <= i or \
                (len(content_list) > i and len(para) > 0 and para[0] != "?") or \
                (len(content_list) > i and len(para) <= 0):
            re_str = re_str.replace("$" + str(i), word_dict["default_para"][i])
        else:
            re_str = re_str.replace("$" + str(i), content_list[i].lstrip(" ").lstrip("?"))
            last_index = i + 1

    # 替换内容
    if word_dict['content']:
        re_str = re_str.replace("$c", '\n'.join(content_list[last_index:]))
    return re_str
