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

keywords = {
    'bilibili': {'para_num': 1,
                 'content': False,
                 'default_para': ["BV1ou41197zy"],
                 'resolve': "{{< bilibili $0 >}}"},
    'high': {'para_num': 3,
             'content': True,
             'default_para': ["text", '0', '1'],
             'resolve': '{{< highlight $0 "linenos=table,hl_lines=$1,linenostart=$2" >}}\n$c\n{{< /highlight >}}'},
    'merm': {'para_num': 0,
             'content': True,
             'default_para': [""],
             'resolve': "{{< mermaid >}}\n$c\n{{< /mermaid >}}"},
    'typeit': {'para_num': 0,
               'content': True,
               'default_para': [""],
               'resolve': "{{< typeit >}}\n$c\n{{< /typeit >}}"},
    'image': {'para_num': 3,
              'content': False,
              'default_para': ["", "image", "400"],
              'resolve': '{{< image src="$0" caption="$1" width=$2 linked=false >}}'},
    'echart': {'para_num': 0,
               'content': True,
               'default_para': [""],
               'resolve': "{{< echart >}}\n$c\n{{< /echart >}}"},
    'quote': {'para_num': 0,
              'content': True,
              'default_para': [""],
              'resolve': "{{< quote >}}\n$c\n{{< /quote >}}"},
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
    # tmp_list_mask
    tmp_list_mask = []
    flag = False
    for i in range(len(tmp_list)):
        line = tmp_list[i].replace(" ", "")
        if len(line) > 3 and line[0:3] == "```" and line[3:] in list(keywords.keys()):
            word = line[3:]
            tmp_list_mask.append(word)
            flag = word
        elif len(line) == 3 and line == "```" and flag is not False:
            tmp_list_mask.append(flag)
            flag = False
        else:
            tmp_list_mask.append(flag)
    # print(tmp_list_mask)
    # 解析
    new_list = []
    para_list = []
    word = ""
    for i in range(len(tmp_list)):
        if tmp_list_mask[i] == False:
            if len(para_list) > 0:
                new_list.append(forward_word(para_list, keywords[word]))
                word = ""
                para_list = []
            new_list.append(tmp_list[i])
        else:
            para_list.append(tmp_list[i])
            word = tmp_list_mask[i]
    # 如果非空，则解析
    if len(para_list) > 0:
        new_list.append(forward_word(para_list, keywords[word]))
    # 解析完成后，拼接
    return "\n".join(new_list)


# 剪掉两端
def forward_preprocess(_list):
    if len(_list) > 0:
        _list.pop()
    if len(_list) > 0:
        _list.pop(0)
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
