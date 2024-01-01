# -*- coding = utf-8 -*-
"""
1.S->A
2.A->Ab
3.A->bBa
4.B->aAc
5.B->a
6.B->aAb
"""

class Stack:
    def __init__(self):
        self.top = 0
        self.data = []
        self.ch = ''  # 存储出栈的字符

    # 入栈
    def push(self, myStr):
        self.data.append(myStr)
        self.top += 1

    # 出栈
    def pop(self):
        if self.top == 0:
            print("stack is empty!")
        self.top -= 1
        self.ch = self.data.pop()

    # 读取栈顶元素
    def read(self):
        return self.data[self.top - 1]

def error():
    print("string is false!")
    exit(0)

# 产生式
class Production:
    def __init__(self,left,length):
        self.left = left
        self.length = length


# 创建产生式
def createProduction():
    l = []
    l.append(Production('S',1))
    l.append(Production('A',2))
    l.append(Production('A',3))
    l.append(Production('B',3))
    l.append(Production('B',1))
    l.append(Production('B',3))
    return l



# 将输入符号转化为整数
def charToInt(myStr):
    if myStr == 'b':
        i = 0
    elif myStr == 'a':
        i = 1
    elif myStr == 'c':
        i = 2
    elif myStr == '#':
        i = 3
    elif myStr == 'A':
        i = 4
    elif myStr == 'B':
        i = 5
    else:
        print("字符错误!")
        exit(0)
    return i



def SLRDriver():
    global state,inputs,action,goto,production
    # 读取当前状态和输入符号
    s = state.read()
    myChr = inputs.read()
    print(f"1.s: {s}, ch: {myChr}")
    while True:
        k = charToInt(myChr)  # 将输入符号转换为整数
        cc = action[s][k]   # 获取action表中的值
        if cc == 's':    # 移进
            state.push(goto[s][k])  # 状态栈执行移入操作
            inputs.pop()
        elif cc == 'r':  # 规约
            m = goto[s][k]  # 获取规约对应的产生式编号
            for i in range(production[m].length):
                state.pop()
            state.push(goto[state.read()][charToInt(production[m].left)])
            print(f"3.s: {s}, ch: {myChr}")

        elif cc == 'a':  # 接受
            print("accept!")
            exit(0)
        else:
            error()

        # 读取当前状态和输入符号
        s = state.read()    # 更新状态
        myChr = inputs.read()  # 更新输入符号
        print(f"2.s: {s}, ch: {myChr}")


# action表: b a c #
action = [
    ['s','0','0','0'],
    ['s','0','0','a'],
    ['s','0','0','0'],
    ['s','r','0','0'],
    ['r','0','r','r'],
    ['0','s','0','0'],
    ['r','0','r','r'],
    ['s','0','0','0'],
    ['r','r','r','r'],
]

# goto表: b a c # A B
goto = [
    [2,-1,-1,-1,1,-1],
    [4,-1,-1,-1,-1,-1],
    [3,-1,-1,-1,-1,5],
    [2,5,-1,-1,7,-1],
    [2,-1,2,2,-1,-1],
    [-1,6,-1,-1,-1,-1],
    [3,-1,3,3,-1,-1],
    [8,-1,-1,-1,-1,-1],
    [2,6,2,2,-1,-1],
]




if __name__ == '__main__':
    # 产生式
    production = createProduction()
    # 待输入字符
    inputs = Stack()
    # 状态
    state = Stack()
    ch = input("请输入字符串: ")
    ch += '#'
    print(ch[::-1])
    for c in reversed(ch):
        # 将待输入字符入栈
        inputs.push(c)
    # 状态入栈
    state.push(0)
    # SLR分析
    SLRDriver()




