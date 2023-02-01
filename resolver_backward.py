# 将local编辑器的内容解析到tmp.md
import util as ut

keywords = {
    'bilibili': {'para_num': 1,
                 'content': False,
                 'resolve': "```bilibili\n?$0\n```",
                 'para_prefix': ['bilibili '],
                 'para_suffix': [' ']},
    'highlight': {'para_num': 1,
                  'content': True,
                  'resolve': '```high\n?$0\n$c\n```',
                  'para_prefix': ['highlight'],
                  'para_suffix': [' ']},
    'mermaid': {'para_num': 0,
                'content': True,
                'resolve': "```merm\n$c\n```"},
    'typeit': {'para_num': 0,
               'content': True,
               'default_para': [""],
               'resolve': "```typeit\n$c\n```"},
    'image': {'para_num': 3,
              'content': False,
              'resolve': '![$1]($0 "$2")',
              'para_prefix': ['src="', 'caption="', 'width='],
              'para_suffix': ['"', '"', ' ']},
    'echarts': {'para_num': 0,
               'content': True,
               'resolve': "```echarts\n$c\n```"},
    'center-quote': {'para_num': 0,
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
    # list_mask
    list_mask = []
    flag = False
    for i in range(len(local_list)):
        line = local_list[i]
        if len(line) > 3 and line.lstrip(' ')[0:4] == "{{< ":
            word = ut.get_in_between(line, "{{< ", " ").replace(" ", "")
            # 多行
            if word in list(keywords.keys()) and keywords[word]["content"]:
                list_mask.append(word)
                flag = word
            elif word[0] == '/' and flag is not False:
                list_mask.append(flag)
                flag = False
            # 单行
            if word in list(keywords.keys()) and not keywords[word]['content']:
                list_mask.append(word)
                flag = False
        else:
            list_mask.append(flag)
    print(list_mask)
    # 解析
    new_list = []
    buffer_list = []
    word = ""
    for i in range(len(local_list)):
        if list_mask[i] == False:
            new_list, word, buffer_list = resolve_buffer(new_list, word, buffer_list)
            new_list.append(local_list[i])
        else:
            buffer_list.append(local_list[i])
            word = list_mask[i]
    new_list, word, buffer_list = resolve_buffer(new_list, word, buffer_list)
    # 解析完成，拼接
    return "\n".join(new_list)


def resolve_buffer(new_list, word, buffer_list):
    if len(buffer_list) > 0:
        new_list.append(backward_word(buffer_list, keywords[word]))
        word = ""
        buffer_list = []
    return new_list, word, buffer_list


def backward_word(content_list, word_dict):
    # 读取参数,并替换到解析字符串
    re_str = word_dict["resolve"]
    content_head = content_list[0]
    for i in range(word_dict["para_num"]):
        re_str = re_str.replace("$" + str(i), ut.get_in_between(content_head, word_dict['para_prefix'][i], word_dict['para_suffix'][i]))
    # 替换内容
    if word_dict['content']:
        re_str = re_str.replace("$c", '\n'.join(content_list[1:-1]))
    return re_str
