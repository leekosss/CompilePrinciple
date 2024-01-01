# -*- coding = utf-8 -*-
# LR0文法分析

class Stack:  # 定义栈
    def __init__(self):
        self.data = []  # 存储数据

    def size(self):  # 返回栈中元素个数
        return len(self.data)

    def push(self, item):  # 入栈
        self.data.append(item)

    def pop(self):  # 出栈
        return self.data.pop()

    def read(self):  # 读取栈顶元素
        return self.data[-1]

    def copy(self):  # 用于复制一个新的栈，与当前栈一样
        new_stack = Stack()
        for i in range(self.size()):
            new_stack.push(self.data[i])
        return new_stack

    def bottomOutput(self):  # 从栈底开始排列输出
        strings = ""
        for i in range(self.size()):
            strings += str(self.data[i])
        return strings

    def topOutput(self):  # 从栈顶开始排列输出
        strings = ""
        for i in range(self.size() - 1, -1, -1):
            strings += str(self.data[i])
        return strings


# LR0分析表
LR0_Table = {
    0: {'a': 'S2', 'b': 'S3', 'c': None, 'd': None, '#': None, 'E': 1, 'A': None, 'B': None},
    1: {'a': None, 'b': None, 'c': None, 'd': None, '#': 'acc', 'E': None, 'A': None, 'B': None},
    2: {'a': None, 'b': None, 'c': 'S4', 'd': 'S10', '#': None, 'E': None, 'A': 6, 'B': None},
    3: {'a': None, 'b': None, 'c': 'S5', 'd': 'S11', '#': None, 'E': None, 'A': None, 'B': 7},
    4: {'a': None, 'b': None, 'c': 'S4', 'd': 'S10', '#': None, 'E': None, 'A': 8, 'B': None},
    5: {'a': None, 'b': None, 'c': 'S5', 'd': 'S11', '#': None, 'E': None, 'A': None, 'B': 9},
    6: {'a': 'r1', 'b': 'r1', 'c': 'r1', 'd': 'r1', '#': 'r1', 'E': None, 'A': None, 'B': None},
    7: {'a': 'r2', 'b': 'r2', 'c': 'r2', 'd': 'r2', '#': 'r2', 'E': None, 'A': None, 'B': None},
    8: {'a': 'r3', 'b': 'r3', 'c': 'r3', 'd': 'r3', '#': 'r3', 'E': None, 'A': None, 'B': None},
    9: {'a': 'r5', 'b': 'r5', 'c': 'r5', 'd': 'r5', '#': 'r5', 'E': None, 'A': None, 'B': None},
    10: {'a': 'r4', 'b': 'r4', 'c': 'r4', 'd': 'r4', '#': 'r4', 'E': None, 'A': None, 'B': None},
    11: {'a': 'r6', 'b': 'r6', 'c': 'r6', 'd': 'r6', '#': 'r6', 'E': None, 'A': None, 'B': None},
}

# 测试句子: acd acccd bcd bccccd
# 产生式
production = {
    0: {'S': 'E'},
    1: {'E': 'aA'},
    2: {'E': 'bB'},
    3: {'A': 'cA'},
    4: {'A': 'd'},
    5: {'B': 'cB'},
    6: {'B': 'd'},
}

# 终结符
VT = ['a', 'b', 'c', 'd', '#']
# 非终结符
VN = ['S', 'A', 'B', 'E']
result = False  # 分析结果
step = 0  # 分析步骤的次数

stateStack = Stack()  # 状态栈
symbolStack = Stack()  # 符号栈
stringsStack = Stack()  # 字符串栈


# 检查输入串的合法性
def check(strings):
    flag = True
    if len(strings) == 0:
        print("[error]输入串为空!")
        flag = False
    for i in range(len(strings)):
        if strings[i] not in VT:
            print("[error]输入串只能由终结符组成!")
            flag = False
            break
    return flag


def initStack(ss):
    global stringsStack
    stateStack.push(0)      # 状态栈初始化0
    symbolStack.push('#')   # 符号栈入栈#
    # 输入串逆序入栈
    for i in range(len(ss)-1,-1,-1):
        stringsStack.push(ss[i])


# LR0分析
def LR0_Analyze():
    global result,step
    step += 1
    stateTop = stateStack.read()        # 获取状态栈栈顶元素
    stringsTop = stringsStack.read()    # 获取输入串栈顶元素
    current = LR0_Table[stateTop][stringsTop]   # 获取LR0表中的值
    if current is None:     # 没找到就报错
        print(
            "|{:^5}|{:^20}|{:^20}|{:^20}|{:^10}|{:^10}|".format(step, stateStack.bottomOutput(),
                                                                symbolStack.bottomOutput(), stringsStack.topOutput(),
                                                                'None', ''))
        print("[error]ACTION值为None!")
        result = False
        return
    if current == 'acc':    # 接受
        print(
            "|{:^5}|{:^20}|{:^20}|{:^20}|{:^10}|{:^10}|".format(step, stateStack.bottomOutput(),
                                                                symbolStack.bottomOutput(), stringsStack.topOutput(),
                                                                'acc', ''))
        result = True
        return
    elif current[0] == 'S':     # 移进
        print(
            "|{:^5}|{:^20}|{:^20}|{:^20}|{:^10}|{:^10}|".format(step, stateStack.bottomOutput(),
                                                                symbolStack.bottomOutput(), stringsStack.topOutput(),
                                                                current, ''))

        current = current.replace("S","")
        stateStack.push(int(current))           # 将状态栈移入S的下标
        symbolStack.push(stringsStack.pop())    # 将字符栈顶元素入栈符号栈
        LR0_Analyze()   # 递归分析
    elif current[0] == 'r':     # 规约
        # 保存一下数据,用于后面输出
        sCurrent = current
        sStateStack = stateStack.copy()
        sSymbolStack = symbolStack.copy()
        # 根据r下标,寻找规约所用产生式的key:value
        current = current.replace("r","")
        key = list(production[int(current)].keys())[0]
        value = list(production[int(current)].values())[0]
        # 根据产生式右部的value长度,对状态栈和符号栈弹栈
        vLen = len(value)
        for i in range(vLen):
            stateStack.pop()
            symbolStack.pop()
        # 根据状态栈当前栈顶元素和产生式左部key，寻找GOTO值
        stateTop = stateStack.read()
        goto = LR0_Table[stateTop][key]
        if goto is None:
            print(
                "|{:^5}|{:^20}|{:^20}|{:^20}|{:^10}|{:^10}|".format(step, sStateStack.bottomOutput(),
                                                                    sSymbolStack.bottomOutput(),
                                                                    stringsStack.topOutput(),
                                                                    sCurrent, 'None'))
            print("[error]GOTO值为None!")
            result = False
            return
        else:
            print(
                "|{:^5}|{:^20}|{:^20}|{:^20}|{:^10}|{:^10}|".format(step, sStateStack.bottomOutput(),
                                                                    sSymbolStack.bottomOutput(),
                                                                    stringsStack.topOutput(),
                                                                    sCurrent, goto))
            stateStack.push(goto)   # 将goto值入状态栈
            symbolStack.push(key)   # 将key入符号栈
            LR0_Analyze()



if __name__ == '__main__':
    string = input("请输入待分析字符串: ")
    string = string.replace(" ", "")  # 去掉空格
    string += '#'  # 加上#代表结束
    if not check(string):  # 输入串没有通过输入检查
        exit(0)
    else:
        print("|{:^5}|{:^20}|{:^20}|{:^20}|{:^10}|{:^10}|".format('step', 'stateStack', 'symbolStack', 'stringsStack',
                                                                  'ACTION', 'GOTO'))
        initStack(string)
        LR0_Analyze()
        if result:
            print("[success]该文法句子合法!")
        else:
            print("[error]该文法句子不合法!")
