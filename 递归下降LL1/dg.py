"""
递归下降分析LL1文法
S->a
S->^
S->(T)
T->SE
E->,SE
E->
"""
# inputs = "(a,(a,a))#"
# inputs = "(((a,a),^,(a)),a)#"
inputs = input("请输入字符串,以#结束:")
index = 0


def error():
    print("error!")
    exit(0)


def match(c):
    global ch,index

    if c == ch:
        index += 1
        ch = inputs[index]
    else:
        error()

def S():
    if ch == 'a':
        match('a')
    elif ch == '^':
        match('^')
    elif ch == '(':
        match('(')
        T()
        match(')')
    else:
        error()

def T():
    S()
    E()

def E():
    if ch == ',':
        match(',')
        S()
        E()



if __name__ == '__main__':
    ch = inputs[0]
    S()
    if ch == '#':
        print("Accept!")
    else:
        print("err")



