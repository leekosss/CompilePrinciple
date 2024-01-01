# -*- coding = utf-8 -*-
# pattern = (a|b)*abb
"""
->  0   1   2   3   4(终止)
0(开始)  a   b
1       a       b
2       a   b
3       a           b
4       a   b
"""
# 例如: aaabb
strings = input("请输入字符串:\n")
collection = [0, 1, 2, 3, 4]  # 状态集
road = {
    0:{'a':1,'b':2},
    1:{'a':1,'b':3},
    2:{'a':1,'b':2},
    3:{'a':1,'b':4},
    4:{'a':1,'b':2}
}
state = 0  # 初始状态

def fun(i,state):
    dic = road.get(state)
    if strings[i] not in dic:
        print("第{}个字母出错了!0".format(i + 1))
        exit(0)
    else:
        print(str(state) + "->" + str(dic[strings[i]]))
        state = dic[strings[i]]
        return state
i = 0
while i < len(strings):
    state = fun(i, state)
    if i == len(strings) - 1 and state != 4:
        print("出错了！")
    i += 1
