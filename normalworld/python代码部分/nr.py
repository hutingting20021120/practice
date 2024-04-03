"""
@filename:nr.py.py
@author:Hu Tingting
@time:2024-04-02

"""
import jieba.posseg as pseg

txt_filename = './data/平凡的世界.txt'
result_filename = './output/平凡的世界_pseg.csv'

# 从文件读取文本
txt_file = open(txt_filename, 'r', encoding='utf-8')
content = txt_file.read()
txt_file.close()
print('文件读取完成')

# 添加自定义字典
# jieba.load_userdict('./data/userdict_pseg.txt')

# 分词
words = pseg.cut(content)  # peseg.cut返回生成器
print('分词完成')

# 用字典统计每个人物名词的出现次数
word_dict = {}
print('正在统计所有词中的人物名词……')
count = 0  # 用于记录已处理的名词数
for one in words:
    # 为便于处理，用w记录本次循环检查的“词”，f记录对应的“词性”
    w = one.word
    f = one.flag

    if len(w) == 1:  # 忽略单字
        continue

    if 'nr' in f:  # 如果该词的词性中包含'nr'，即这是个人物名词，……
        if w in word_dict.keys():  # 如果该词已经在词典中，……
            word_dict[w] = word_dict[w] + 1
        else:  # 如果该词不在词典中，……
            word_dict[w] = 1

    # 打印进度
    count = count + 1
    count_quo = int(count / 1000)
    count_mod = count % 1000  # 取模，即做除法得到的余数
    if count_mod == 0:  # 每逢整千的数，打印一次进度
        print('---已处理词数（千）：' + str(count_quo))  # 打印进度信息
        # print('\r已处理词数：' + '-'*count_quo + '> '\
        #      + str(count_quo) + '千', end='')  # 自行刷新的进度条

# 循环结束点

print()
print('人物名词统计完成')

# 把字典转成列表，并按原先“键值对”中的“值”从大到小排序
items_list = list(word_dict.items())
items_list.sort(key=lambda x: x[1], reverse=True)
print('排序完成')

# 根据用户需求，打印排名前列的词，同时把统计结果存入文件
total_num = len(items_list)
print('共有' + str(total_num) + '个可能的人名。')
num = input('您想查看前多少个人物？[10]:')
if not num.isdigit() or num == '':
    num = 10
else:
    num = int(num)

if num > total_num:
    num = total_num

result_file = open(result_filename, 'w')
result_file.write('人物,出现次数\n')
for i in range(num):
    word, cnt = items_list[i]
    message = str(i + 1) + '. ' + word + '\t' + str(cnt)
    print(message)
    result_file.write(word + ',' + str(cnt) + '\n')
result_file.close()

print('已写入文件：' + result_filename)