# 将local编辑器的内容解析到tmp.md
keywords = {
    'bilibili': {'para_num': 1,
                 'content': False,
                 'resolve': "```bilibili\n?$0\n```",
                 'para_prefix': ['bilibili '],
                 'para_suffix': [' ']},
    'highlight': {'para_num': 3,
                  'content': True,
                  'resolve': '```high\n?$0\n?$1\n?$2\n$c\n```',
                  'para_prefix': ['highlight', 'hl_lines=', 'linenostart='],
                  'para_suffix': [' ', ',', '"']},
    'mermaid': {'para_num': 0,
                'content': True,
                'resolve': "```merm\n$c\n```"},
    'typeit': {'para_num': 0,
               'content': True,
               'default_para': [""],
               'resolve': "```typeit\n$c\n```"},
    'image': {'para_num': 3,
              'content': False,
              'resolve': '```image\n?$0\n?$1\n?$2\n````',
              'para_prefix': ['src="', 'caption="', 'width='],
              'para_suffix': ['"', '"', ' ']},
    'echart': {'para_num': 0,
               'content': True,
               'resolve': "```echart\n$c\n```"},
    'quote': {'para_num': 0,
              'content': True,
              'resolve': "```quote\n$c\n```"},
    'admonition': {'para_num': 2,
                   'content': True,
                   'resolve': '```admon\n?$0\n?$1\n$c\n```',
                   'para_prefix': ['type=', 'title="'],
                   'para_suffix': [' ', '"']},
    'link': {'para_num': 3,
             'content': False,
             'resolve': '```link\n?$0\n?$1\n?$2\n```',
             'para_prefix': ['href="', 'content=', 'download="'],
             'para_suffix': ['"', ' ', '"']}}


# {{< highlight $0 "linenos=table,hl_lines=$1,linenostart=$2" >}}\n$c\n{{< /highlight >}}
# 将local的内容解析到tmp.md
def resolver_backward(local):
    # 长文本转化为list
    local_list = local.split('\n')
    # local_list_mask
    local_list_mask = []
    flag = False
    for i in range(len(local_list)):
        line = local_list[i]
        if len(line) > 3 and line.lstrip(' ')[0:4] == "{{< ":
            word = get_in_between(line, "{{< ", " ").replace(" ", "")
            # 多行
            if word in list(keywords.keys()) and keywords[word]["content"]:
                local_list_mask.append(word)
                flag = word
            elif word[0] == '/' and flag is not False:
                local_list_mask.append(flag)
                flag = False
            # 单行
            if word in list(keywords.keys()) and not keywords[word]['content']:
                local_list_mask.append(word)
                flag = False
        else:
            local_list_mask.append(flag)
    # 解析
    new_list = []
    para_list = []
    word = ""
    for i in range(len(local_list)):
        if local_list_mask[i] == False:
            if len(para_list) > 0:
                new_list.append(backward_word(para_list, keywords[word]))
                word = ""
                para_list = []
            new_list.append(local_list[i])
        else:
            para_list.append(local_list[i])
            word = local_list_mask[i]
    # 如果非空，则解析
    if len(para_list) > 0:
        new_list.append(backward_word(para_list, keywords[word]))
    # 解析完成后，拼接
    return "\n".join(new_list)


def backward_word(content_list, word_dict):
    # 读取参数,并替换到解析字符串
    re_str = word_dict["resolve"]
    content_head = content_list[0]
    for i in range(word_dict["para_num"]):
        re_str = re_str.replace("$" + str(i), get_in_between(content_head, word_dict['para_prefix'][i], word_dict['para_suffix'][i]))
    # 替换内容
    if word_dict['content']:
        re_str = re_str.replace("$c", '\n'.join(content_list[1:-1]))
    return re_str


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
