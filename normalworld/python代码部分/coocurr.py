"""
@filename:coocurr.py.py
@author:Hu Tingting
@time:2024-04-03

"""

import jieba.posseg as pseg

##--- 第0步：准备工作，重要变量的声明

# 输入文件
txt_file_name = './data/平凡的世界.txt'
# 输出文件
node_file_name = './output/平凡的世界-人物节点.csv'
link_file_name = './output/平凡的世界-人物连接.csv'

# 运行时，经常出现目标文件被打开，导致写文件失败
# 可以提前测试打开，这样可以很大程度避免问题，但更好的方式是用异常处理机制
test = open(node_file_name, 'w')
test.close()
test = open(link_file_name, 'w')
test.close()

# 打开文件，读入文字
txt_file = open(txt_file_name, 'r', encoding='utf-8')
line_list = txt_file.readlines()
txt_file.close()

##--- 第1步：生成基础数据（一个列表，一个字典）
line_name_list = []  # 每个段落出现的人物列表
name_cnt_dict = {}  # 统计人物出现次数

# ！！设置忽略词的列表
ignore_list = ['双水村', '老汉', '师傅', '明白', '和晓霞', '阳光', '和润叶',
               '米家镇', '洪水', '金家湾']

print('正在分段统计……')
print('已处理词数：')
progress = 0  # 用于计算进度条
for line in line_list:  # 逐个段落循环处理
    word_gen = pseg.cut(line)  # peseg.cut返回分词结果，“生成器”类型
    line_name_list.append([])

    for one in word_gen:
        word = one.word
        flag = one.flag

        if len(word) == 1:  # 跳过单字词
            continue

        if word in ignore_list:  # 跳过标记忽略的人名
            continue

        # 对指代同一人物的名词进行合并
        if word == '玉厚':
            word = '孙玉厚'
        if word == '福堂':
            word = '田福堂'
        if word == '红梅':
            word = '郝红梅'
        if word == '晓霞':
            word = '田晓霞'
        if word == '玉亭':
            word = '孙玉亭'


        if flag == 'nr':
            line_name_list[-1].append(word)
            if word in name_cnt_dict.keys():
                name_cnt_dict[word] = name_cnt_dict[word] + 1
            else:
                name_cnt_dict[word] = 1

        # 因为词性分析耗时很长，所以需要打印进度条，以免用户误以为死机了
        progress = progress + 1
        progress_quo = int(progress / 1000)
        progress_mod = progress % 1000  # 取模，即做除法得到的余数
        if progress_mod == 0:  # 每逢整千的数，打印一次进度
            # print('---已处理词数（千）：' + str(progress_quo))
            print('\r' + '-' * progress_quo + '> ' \
                  + str(progress_quo) + '千', end='')
# 循环结束点
print()
print('基础数据处理完成')

##--- 第2步：用字典统计人名“共现”数量（relation_dict）
relation_dict = {}

# 只统计出现次数达到限制数的人名
name_cnt_limit = 50

for line_name in line_name_list:
    for name1 in line_name:
        # 判断该人物name1是否在字典中
        if name1 in relation_dict.keys():
            pass  # 如果已经在字典中，继续后面的统计工作
        elif name_cnt_dict[name1] >= name_cnt_limit:  # 只统计出现较多的人物
            relation_dict[name1] = {}  # 添加到字典
        else:  # 跳过出现次数较少的人物
            continue

        # 统计name1与本段的所有人名（除了name1自身）的共现数量
        for name2 in line_name:
            if name2 == name1 or name_cnt_dict[name2] < name_cnt_limit:
                # 不统计name1自身；不统计出现较少的人物
                continue

            if name2 in relation_dict[name1].keys():
                relation_dict[name1][name2] = relation_dict[name1][name2] + 1
            else:
                relation_dict[name1][name2] = 1

print('共现统计完成，仅统计出现次数达到' + str(name_cnt_limit) + '及以上的人物')

##--- 第3步：输出统计结果
# 字典转成列表，按出现次数排序
item_list = list(name_cnt_dict.items())
item_list.sort(key=lambda x: x[1], reverse=True)

## 导出节点文件
node_file = open(node_file_name, 'w')
# 节点文件，格式：Name,Weight -> 人名,出现次数
node_file.write('Name,Weight\n')
node_cnt = 0  # 累计写入文件的节点数量
for name, cnt in item_list:
    if cnt >= name_cnt_limit:  # 只输出出现较多的人物
        node_file.write(name + ',' + str(cnt) + '\n')
        node_cnt = node_cnt + 1
node_file.close()
print('人物数量：' + str(node_cnt))
print('已写入文件：' + node_file_name)

## 导出连接文件
# 共现数可以看做是连接的权重，只导出权重达到限制数的连接
link_cnt_limit = 10
print('只导出数量达到' + str(link_cnt_limit) + '及以上的连接')

link_file = open(link_file_name, 'w')
# 连接文件，格式：Source,Target,Weight -> 人名1,人名2,共现数量
link_file.write('Source,Target,Weight\n')
link_cnt = 0  # 累计写入文件的连接数量
for name1, link_dict in relation_dict.items():
    for name2, link in link_dict.items():
        if link >= link_cnt_limit:  # 只输出权重较大的连接
            link_file.write(name1 + ',' + name2 + ',' + str(link) + '\n')
            link_cnt = link_cnt + 1
link_file.close()
print('连接数量：' + str(link_cnt))
print('已写入文件：' + link_file_name)