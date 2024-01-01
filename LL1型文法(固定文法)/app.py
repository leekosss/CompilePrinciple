"""
1.S->a
2.S->^
3.S->(T)
4.T->SE
5.E->,SE
6.E->
"""

# 栈
class stack:
    def __init__(self):
        self.top = 0
        self.data = []
        self.ch = ''  # 存储出栈的字符

    # 入栈
    def push(self, c):
        self.data.append(c)
        self.top += 1

    # 出栈
    def pop(self):
        if self.top == 0:
            print("stack is empty!")
        self.top -= 1
        self.ch = self.data.pop()

    # 读取栈顶元素
    def read(self):
        return self.data[self.top-1]

def error():
    print("error")
    exit(0)

# 判断是否为终结符
def is_vt(cc):
    flag = -1
    if cc == 'S' or cc == 'T' or cc == 'E':
        flag = 0
    if cc == 'a' or cc == '^' or cc == '(' or cc == ')' or cc == ',':
        flag = 1
    if flag != -1:
        return flag
    else:
        print("character is false!")
        exit(0)


def vn2int(cc):  # 非终结符定位LL分析表
    # flag = -1
    if cc == 'S':
        flag = 0
    elif cc == 'T':
        flag = 1
    elif cc == 'E':
        flag = 2
    else:
        print("character is false!")
        exit(0)
    return flag


def vt2int(cc):  # 终结符定位LL分析表
    if cc == 'a':
        flag = 0
    elif cc == '^':
        flag = 1
    elif cc == '(':
        flag = 2
    elif cc == ')':
        flag = 3
    elif cc == ',':
        flag = 4
    else:
        print("character is false!")
        exit(0)
    return flag


# 判断LL1文法的关键函数
def LL_driver():
    ic = inputs.read()  # 当前识别的字符
    sc = sem.read()  # 文法中的字符

    while sc != '#':
        if is_vt(sc):
            if ic == sc:  # 非终结符相等就出栈
                inputs.pop()
                sem.pop()
            else:
                error()
        else:
            flag = LL[vn2int(sc)][vt2int(ic)]  # 获得LL1分析表中的数值来执行相应算法
            if flag == 1:
                sem.pop()
                sem.push('a')
            elif flag == 2:
                sem.pop()
                sem.push('^')
            elif flag == 3:
                sem.pop()
                sem.push(')')
                sem.push('T')
                sem.push('(')
            elif flag == 4:
                sem.pop()
                sem.push('E')
                sem.push('S')
            elif flag == 5:
                sem.pop()
                sem.push('E')
                sem.push('S')
                sem.push(',')
            elif flag == 6:
                sem.pop()

            else:
                error()

        ic = inputs.read()  # 当前识别的字符
        sc = sem.read()  # 文法中的字符

    if ic == '#' and sc == '#':
        print("accept!")
    else:
        error()


# LL分析表
LL = [
    [1,2,3,-1,-1],
    [4,4,4,-1,-1],
    [-1,-1,-1,6,5]
]



if __name__ == '__main__':
    inputs = stack()  # 存储待识别字符串
    sem = stack()  # 存储文法
    index = 0
    ch = input('请输入字符串:')  # 待识别的字符串
    ch += '#'

    # 反向入栈
    for c in reversed(ch):
        print(c,end="")
        inputs.push(c)
    print()
    sem.push('#')
    sem.push('S')
    LL_driver()





