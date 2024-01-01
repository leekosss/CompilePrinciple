import re

# 词法分析
class MyToken:
    def __init__(self, MyType, seman, MyStr):
        self.MyType = MyType
        self.seman = seman
        self.MyStr = MyStr

    def __str__(self):
        s = self.MyStr.replace('\n','')
        return "token.class:  {:5}\t\tstr:  {:10}\tseman:\t{} \t".format(self.MyType, s, self.seman)


# 单词集状态列表
states = ['if', 'else', 'for', 'while', 'break', 'return', 'continue', 'float', 'int', 'char', '标识符',
          '正整数、正实数、零', '+', '-',
          '*', '/', '%', '>', '>=', '<', '<=', '!=', '==', '!', '&', '|', ',', '=', '[', ']', '(', ')', '{', '}', ';',
          '.', '\\', '#']
choiceStatec = [13, 14, 15, 16, 17, 18, 20, 24, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36]  # 用于防止while循环中出现多次elif
inputs = []  # 输入的字符



tokens = []  # 单词表
NameL = []  # 名字表
ConstL = []  # 常数表



i = 0
line = 1



# 将文件内容提取到inputs
def codeToInputs(sourceCodes):
    for line in sourceCodes:
        for char in line:
            inputs.append(char)
            if char == '#':
                return


# 判断是否为字母
def isLetter(char):
    pattern = r"[a-zA-Z]"
    return bool(re.match(pattern, char))


# 判断是否为数字
def isDigit(char):
    pattern = r"[0-9]"
    return bool(re.match(pattern, char))


# 普通的字符识别
def isC(char, state):
    tokens.append(MyToken(state, "^", char))


def choiceState(char):  # 选择单字符对应状态
    state = 0
    if char in states:
        for k in range(len(states)):
            if states[k] == char:  # 判断单个字符
                if char in ['>', '<', '!', '=', '&', '|', '\\'] and inputs[i] in ['=', '&', '|', 'n']:  # 如果是双字符
                    state = 19
                else:
                    state = k + 1
    else:
        state = 0
    return state


def error():
    print(f"第{line}行---未知字符错误")
    exit(0)


# 词法分析
def nextToken():
    global i
    global line
    name = ""
    char = inputs[i]
    i += 1
    while char == ' ' or char == '\n' or char == '\t':  # 如果是空就跳过
        if char == '\n':
            line += 1
        char = inputs[i]
        i += 1
        if char == '#':
            i -= 1
    global state
    state = 0
    while True:

        if state == 0:  # 选择
            if char == '#':
                i -= 1
                state = 38
                continue
            if char == '/' and (inputs[i] == '/' or inputs[i] == '*'):  # 注释
                state = 42
                continue
            if choiceState(char) != 0:  # 判断后面的单字符，获取状态
                state = choiceState(char)
                i -= 1
                continue
            if char == "i":
                state = 1
            elif char == "e":
                state = 2
            elif char == 'f':
                state = 3
            elif char == 'w':
                state = 4
            elif char == 'b':
                state = 5
            elif char == 'r':
                state = 6
            elif char == 'c':
                state = 7
            elif isDigit(char):  # 数字
                state = 12
            elif isLetter(char):  # 字符串
                i -= 1
                state = 11

            else:
                error()  # 非法字符报错
                i -= 1
                state = 38
        elif state == 1:  # if

            if inputs[i] == 'f':  # 判断第二个是否为f
                if isDigit(inputs[i + 1]) or isLetter(inputs[i + 1]):  # 标识符
                    i -= 1
                    state = 11
                else:
                    m = MyToken(1, "^", "if")  # 在单词表和名字表加入
                    tokens.append(m)
                    state = 38

            elif inputs[i] == 'n':  # 判断第二个是否为n
                i += 1
                if inputs[i] == 't':
                    if isDigit(inputs[i + 1]) or isLetter(inputs[i + 1]):  # 标识符
                        i -= 2
                        state = 11
                    else:
                        m = MyToken(9, "^", "int")  # 在单词表和名字表加入
                        tokens.append(m)
                        state = 38
                else:
                    if isDigit(inputs[i]) or isLetter(inputs[i]):  # 标识符
                        i -= 2
                        state = 11
                    else:
                        m = MyToken(11, "^", "in")  # 在单词表和名字表加入
                        tokens.append(m)
                        state = 38
                        i -= 1
            else:  # 以i开头的标识符
                i -= 1
                state = 11

        elif state == 2:  # else
            if ''.join(inputs[i:i + 3]) == 'lse':
                if isDigit(inputs[i + 3]) or isLetter(inputs[i + 3]):
                    i -= 1
                    state = 11
                else:
                    m = MyToken(2, "^", "else")  # 在单词表和名字表加入
                    tokens.append(m)
                    state = 38
                    i += 2
            else:
                i -= 1
                state = 11

        elif state == 3:  # for

            if inputs[i] == 'o':
                if inputs[i + 1] == 'r':
                    if isDigit(inputs[i + 2]) or isLetter(inputs[i + 2]):
                        i -= 1
                        state = 11
                    else:
                        m = MyToken(3, "^", "for")  # 在单词表和名字表加入
                        tokens.append(m)
                        state = 38
                        i += 1
                else:
                    i -= 1
                    state = 11
            elif inputs[i] == 'l':
                if "".join(inputs[i:i + 4]) == 'loat':
                    if isDigit(inputs[i + 4]) or isLetter(inputs[i + 4]):
                        i -= 1
                        state = 11
                    else:
                        m = MyToken(8, "^", "float")  # 在单词表和名字表加入
                        tokens.append(m)
                        state = 38
                        i += 3
                else:
                    i -= 1
                    state = 11
            else:
                i -= 1
                state = 11

        elif state == 4:  # while
            if "".join(inputs[i:i + 4]) == 'hile':
                if isDigit(inputs[i + 4]) or isLetter(inputs[i + 4]):
                    i -= 1
                    state = 11
                else:
                    m = MyToken(4, "^", "while")  # 在单词表和名字表加入
                    tokens.append(m)
                    state = 38
                    i += 3
            else:
                i -= 1
                state = 11


        elif state == 5:  # break
            if "".join(inputs[i:i + 4]) == 'reak':
                if isDigit(inputs[i + 4]) or isLetter(inputs[i + 4]):
                    i -= 1
                    state = 11
                else:
                    m = MyToken(5, "^", "break")  # 在单词表和名字表加入
                    tokens.append(m)
                    state = 38
                    i += 3
            else:
                i -= 1
                state = 11

        elif state == 6:  # return
            if "".join(inputs[i:i + 5]) == 'eturn':
                if isDigit(inputs[i + 5]) or isLetter(inputs[i + 5]):
                    i -= 1
                    state = 11
                else:
                    m = MyToken(6, "^", "return")  # 在单词表和名字表加入
                    tokens.append(m)
                    state = 38
                    i += 4
            else:
                i -= 1
                state = 11

        elif state == 7:  # continue
            if inputs[i] == 'o':
                if "".join(inputs[i + 1:i + 7]) == 'ntinue':
                    if isDigit(inputs[i + 7]) or isLetter(inputs[i + 7]):
                        i -= 1
                        state = 11
                    else:
                        m = MyToken(7, "^", "continue")  # 在单词表和名字表加入
                        tokens.append(m)
                        state = 38
                        i += 6
                else:
                    i -= 1
                    state = 11

            elif inputs[i] == 'h':
                if "".join(inputs[i + 1:i + 3]) == 'ar':
                    if isDigit(inputs[i + 3]) or isLetter(inputs[i + 3]):
                        i -= 1
                        state = 11
                    else:
                        m = MyToken(10, "^", "char")  # 在单词表和名字表加入
                        tokens.append(m)
                        state = 38
                        i += 2
                else:
                    state = 11
                    i -= 1
            else:
                i -= 1
                state = 11
        elif state == 11:  # 标识符
            char = inputs[i]
            i += 1
            name += char
            if isLetter(char):
                state = 39
            else:
                state = 40

        elif state == 12:

            name += char
            char = inputs[i]
            if isDigit(inputs[i]):  # 判断数字
                i += 1
                state = 12
            else:
                if inputs[i] == ' ' or inputs[i] == '\n' or inputs[i] == '\t' or inputs[i] == '#':

                    flag = 0
                    index = -1
                    for ii in range(len(ConstL)):
                        if ConstL[ii].MyStr == name:
                            flag = 1
                            index = ii
                    if flag == 1:
                        tokens.append(MyToken(12, index, name))

                    else:
                        ConstL.append(MyToken(12, len(ConstL), name))
                        tokens.append(MyToken(12, len(ConstL)-1, name))

                else:
                    print(f"第{line}行---标识符错误")
                    char = inputs[i]
                    while char != ' ' and char != '\t' and char != '\n' and char != '#':
                        i += 1
                        char = inputs[i]
                state = 38
                i -= 1

        elif state == 19:  # 处理双字符
            m = ""
            if inputs[i] == '>' and inputs[i + 1] == '=':
                m = MyToken(19, "^", ">=")
            if inputs[i] == '<' and inputs[i + 1] == '=':
                m = MyToken(21, "^", "<=")
            if inputs[i] == '!' and inputs[i + 1] == '=':
                m = MyToken(22, "^", "!=")
            if inputs[i] == '=' and inputs[i + 1] == '=':
                m = MyToken(23, "^", "==")
            if inputs[i] == '&' and inputs[i + 1] == '&':
                m = MyToken(25, "^", "&&")
            if inputs[i] == '|' and inputs[i + 1] == '|':
                m = MyToken(26, "^", "||")
            if inputs[i] == '\\' and inputs[i + 1] == 'n':
                m = MyToken(37, "^", "\\n")
            tokens.append(m)
            i += 1
            return

        elif state == 38:  # 文件结束
            return
        elif state == 39:  # 处理标识符
            char = inputs[i]
            i += 1
            if char == '#':
                i -= 1
                state = 40
                continue

            if isDigit(char) or isLetter(char):
                state = 39
                if char != '\n':
                    name += char
                else:
                    line += 1

            else:  # 不是字母和数字，就不是标识符了
                state = 40
        elif state == 40:
            flag = 0
            index = -1
            for ii in range(len(NameL)):
                if NameL[ii].MyStr == name:
                    flag = 1
                    index = ii
            if flag == 1:
                tokens.append(MyToken(11, index, name))

            else:
                NameL.append(MyToken(11, len(NameL), name))
                tokens.append(MyToken(11, len(NameL)-1, name))


            i -= 2  # 外面的while+1，所以这里要-1
            if char == '#':
                i += 1
            try:
                if states.index(char) and char != '#':  # 如果有字符
                    name = name[:-1]
                    state = 41

            except:
                pass
            return
        elif state == 41:
            st = states.index(char)
            isC(char, st)
            i -= 1
            return
        elif state == 42:  # 处理注释 // /**/
            if inputs[i] == '/':  # //注释
                i += 1
                char = inputs[i]
                while char != '\n':
                    i += 1
                    char = inputs[i]
                i += 1
                state = 0
            pass
        elif state in choiceStatec:
            isC(states[state - 1], state)  # 普通的字符识别
            return
        else:
            pass

def init():
    LLTable['XIANGWEI'][';'] = [('XIANGWEI', 'ε')]
    LLTable['INITIALIZATION'][';'] = [('INITIALIZATION','ε')]


# 从文件读取内容
def readSourceCode(read_path):
    with open(read_path, "r") as file:
        lines = file.readlines()
    return lines







# 语法分析


def calculateFirst(ch):
    # print(ch)
    if ch in grammar['terminals']:
        return set(ch)

    first_sets = {symbol: set() for symbol in grammar['non_terminals']}
    if ch not in first_sets:
        first_sets[ch] = set()
    updated = True

    while updated:
        updated = False

        for production in grammar['productions']:
            left_symbol = production[0]
            right_symbols = production[1:]

            # 处理右部的每个符号
            for right_symbol in right_symbols:
                if right_symbol in grammar['terminals']:
                    # 终结符，将其添加到左部非终结符的 FIRST 集合中
                    if right_symbol not in first_sets[left_symbol]:
                        first_sets[left_symbol].update([right_symbol])
                        updated = True
                    break
                elif right_symbol in grammar['non_terminals']:
                    # 非终结符，将其 FIRST 集合（除去空字符）添加到左部非终结符的 FIRST 集合中
                    symbol_first = first_sets[right_symbol]
                    if 'ε' not in symbol_first:
                        if symbol_first - first_sets[left_symbol]:
                            first_sets[left_symbol].update(symbol_first)
                            updated = True
                        break
                    else:
                        if symbol_first - first_sets[left_symbol]:
                            first_sets[left_symbol].update(symbol_first - {'ε'})
                            updated = True
                        break
            else:
                # 如果右部的所有符号都能推导出空字符，将空字符添加到左部非终结符的 FIRST 集合中
                if 'ε' not in first_sets[left_symbol]:
                    first_sets[left_symbol].add('ε')
                    updated = True

    return first_sets[ch]


# 计算Follow集
def calculateFollow(startSymbol):
    # 初始化非终结符follow集
    follow_sets = {}
    for symbol in grammar['non_terminals']:
        follow_sets[symbol] = set()
    # 文法开始符添加 #
    follow_sets[startSymbol].add('#')
    # update用于观察是否需要继续更新，用于多次循环产生式，防止某个follow集计算不完全
    update = True
    while update:
        update = False
        # 遍历产生式
        for production in grammar['productions']:
            # 左侧非终结符
            non_terminal = production[0]
            # 产生式右侧
            symbols = production[1:]
            # 遍历右侧
            for index, symbol in enumerate(symbols):
                # 只有右侧非终结符才要计算Follow集
                if symbol in grammar['non_terminals']:
                    # 不是右侧最后一个
                    if index < len(symbols) - 1:
                        first_beta = set()
                        # 遍历非终结符后的元素，求它的first集
                        for j in range(index + 1, len(symbols)):
                            currentSymbol = symbols[j]
                            currentFirst = calculateFirst(currentSymbol)
                            first_test = follow_sets[symbol]

                            # 非终结符后面的first集包含ε
                            if 'ε' in currentFirst:
                                # first集还有其他元素
                                if len(currentFirst) != 1:
                                    # 将first集除ε后添加到follow集中
                                    follow_sets[symbol].update(currentFirst - {'ε'})
                                    # 更新了follow集
                                    if first_test != follow_sets[symbol]:
                                        update = True
                                    break
                                else:
                                    # first只有一个ε
                                    first_beta.update({'ε'})
                            else:
                                # first没有ε
                                first_test = follow_sets[symbol]
                                follow_sets[symbol].update(currentFirst - {'ε'})
                                # 更新了follow集
                                if first_test != follow_sets[symbol]:
                                    update = True
                                break
                        # 如果非终结符右侧first为ε，那么加入左侧的follow给它
                        if 'ε' in first_beta:
                            # 这里很坑，不能直接将set集合复制，需要使用copy()函数，
                            # 否则引用first_beta和follow_sets[symbol]同一个地址***
                            first_beta = follow_sets[symbol].copy()
                            follow_sets[symbol].update(follow_sets[non_terminal])
                            if first_beta != follow_sets[symbol]:
                                update = True
                    # 右侧只有一个终结符
                    elif index == len(symbols) - 1:
                        first_beta = follow_sets[symbol].copy()
                        follow_sets[symbol].update(follow_sets[non_terminal])
                        if first_beta != follow_sets[symbol]:
                            update = True

    return follow_sets


# 初始化并填充LL1预测分析表
def initLLTable():
    LLTable = {}
    # 初始化LL1分析表
    for non_terminal in grammar['non_terminals']:
        LLTable[non_terminal] = {}
        for terminal in grammar['terminals']:
            LLTable[non_terminal][terminal] = []
        LLTable[non_terminal]['#'] = []

    # 填充LL(1)分析表
    for production in grammar['productions']:
        non_terminal = production[0]
        right_symbols = production[1:]
        # 遍历产生式右侧的符号
        for symbol in right_symbols:
            # 如果是终结符，说明first集就是该终结符，直接在分析表中添加
            if symbol in grammar['terminals']:
                LLTable[non_terminal][symbol].append(production)
                break
            # 如果是非终结符
            elif symbol in grammar['non_terminals']:
                # 计算first集
                symbol_first = first_sets[symbol]

                for terminal in symbol_first:
                    # 不为空
                    if terminal != 'ε':
                        LLTable[non_terminal][terminal].append(production)
                if 'ε' in symbol_first:
                    for terminal in follow_sets[non_terminal]:
                        LLTable[non_terminal][terminal].append(production)
                break
            # 如果产生式右部只有一个ε，说明需要加入左部follow集
            elif symbol == 'ε':
                for terminal in follow_sets[non_terminal]:
                    LLTable[non_terminal][terminal].append(production)
    # print(LLTable['INITIALIZATION'])

    return LLTable

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

def LLError():
    print("string is false!")
    exit(0)


def vn2int(cc):  # 非终结符定位LL分析表
    for non_terminal in grammar['non_terminals']:
        if non_terminal == cc:
            return non_terminal
    else:
        print("character is false!")
        exit(0)


def vt2int(cc):  # 终结符定位LL分析表
    for terminal in grammar['terminals']:
        if terminal == cc:
            return terminal
    else:
        if cc == '#':
            return '#'
        else:
            print("character is false!")
            exit(0)


# 判断LL1文法的关键函数
def LL_driver():
    global LLStack,strings
    ic = inputs.read()  # 当前识别的字符
    sc = sem.read()  # 文法中的字符

    while sc != '#':
        # print(f"ic {ic}  ----  sc {sc}")
        # 是终结符
        if sc in grammar['terminals']:
            if ic == sc:  # 终结符相等就出栈
                # print(f"ic {ic}  --terminals--  sc {sc}")
                outputStrings = " ".join(strings)
                print(f"{LLStack:20}   {outputStrings:20} '{ic}' 匹配")
                chlen = len(ic)
                LLStack = LLStack[:-1*chlen]
                strings = strings[1:]
                inputs.pop()
                sem.pop()
            else:
                LLError()
        # 非终结符
        elif sc in grammar['non_terminals']:
            # 获得LL1分析表中的数值来执行相应算法
            # print(vn2int(sc) + "---" + vt2int(ic))
            # print(vn2int(sc)+" "+str(LLTable[vn2int(sc)]))
            productions = LLTable[vn2int(sc)][vt2int(ic)]
            # 如果产生式的列表为空，代表源输入串有误

            if not productions:
                print("[语法错误] 类型: " + vt2int(ic) + " 前存在语法错误")
                exit(0)
                # print("产生式为空~~~")
                # LLError()
                # pass
            # 遍历分析表中同一格的多个产生式
            for LLProduction in productions:
                for production in grammar['productions']:
                    # 如果分析表的产生式与文法中产生式相等
                    if LLProduction == production:
                        non_terminal = production[0]
                        right_symbols = production[1:]

                        productionStr = non_terminal+"->"+"".join(right_symbols)
                        outputStrings = " ".join(strings)
                        print(f"{LLStack:20}   {outputStrings:20} {productionStr:20}")
                        chlen = len(non_terminal)
                        LLStack = LLStack[:-1*chlen]

                        sem.pop()
                        for right_symbol in reversed(right_symbols):
                            sem.push(right_symbol)
                            LLStack += right_symbol
                        break
        elif sc == 'ε':
            LLStack = LLStack[:-1]
            outputStrings = " ".join(strings)
            print(f"{LLStack:20}   {outputStrings:20} ε")

            sem.pop()
            sc = sem.read()
            continue
        # else:
        #     LLError()

        ic = inputs.read()  # 当前识别的字符
        sc = sem.read()  # 文法中的字符

    if ic == '#' and sc == '#':
        print("[success]识别成功!")
    else:
        LLError()


# 从文件中读取文法
def read_grammar_from_file(file_path):
    grammar = {'terminals': set(), 'non_terminals': set(), 'productions': []}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith('#'):
                continue  # 跳过空行和注释

            production_parts = line.split('->')
            if len(production_parts) != 2:
                raise ValueError(f"不合法产生式: 第{line}行")

            left_symbol = production_parts[0].strip()
            right_part = production_parts[1].strip()

            # 支持以 '|' 分隔的多个产生式
            right_symbols_list = [symbol.strip().split() for symbol in right_part.split('|')]
            chars = {';', '=', '+', '-', '*', '/', '>', '<', '{', '}', '(', ')', ','}
            # 将每个右侧部分作为单独的产生式添加到 grammar['productions']
            for right_symbols in right_symbols_list:
                grammar['productions'].append((left_symbol, *right_symbols))
                grammar['non_terminals'].add(left_symbol)
                grammar['terminals'].update(symbol for symbol in right_symbols if symbol.isalpha() and symbol.islower() and symbol != 'ε')
                grammar['terminals'].update(
                    symbol for symbol in right_symbols if symbol in chars)

    if grammar['productions']:
        grammar['start_symbol'] = grammar['productions'][0][0]
    else:
        raise ValueError("文法文件为空!")

    return grammar







# 打印First集
def printFirst(grammar):
    # 计算 First 集
    global first_sets
    first_sets = {}
    print("----------------First集----------------")
    for c in grammar['non_terminals']:
        first_sets[c] = calculateFirst(c)
        print("First(" + c + ")=" + str(first_sets[c]))

# 打印Follow集
def printFollow(grammar):
    # 计算 Follow 集
    global follow_sets
    follow_sets = calculateFollow(start_symbol)
    print("----------------Follow集----------------")
    for symbol, follow_set in follow_sets.items():
        formatted_set = ', '.join(sorted(follow_set))  # 将集合排序并转换为逗号分隔的字符串
        print(f"Follow({symbol})={{ {formatted_set} }}")

def printLLTable(LLTable):
    # 获取所有非终结符和终结符
    non_terminals = list(LLTable.keys())
    terminals = set()
    for row in LLTable.values():
        terminals.update(row.keys())

    # 打印表头
    print("-"*50+"LL1预测分析表"+"-"*50)
    print(f"{'非终结符':<10}", end=' ')
    for terminal in terminals:
        print(f"{terminal:<20}", end=' ')
    print()

    # 打印分析表
    for non_terminal in non_terminals:
        print(f"{non_terminal:<10}", end=' ')
        for terminal in terminals:
            productions = LLTable[non_terminal].get(terminal, [])
            if productions:
                leftmost_production = productions[0]  # 取第一个产生式

                leftmost_str = leftmost_production[0]+"->"+"".join(leftmost_production[1:])
                print(f"{leftmost_str:<20}", end=' ')
            else:
                print(f"{'':<20}", end=' ')
        print()


grammarDict = {
    '1': 'if',
    '2': 'else',
    '4': 'while',
    '8': 'float',
    '9': 'int',
    '10': 'char',
    '11': 'identifier',
    '12': 'intconstant',
    '13': '+',
    '14': '-',
    '15': '*',
    '16': '/',
    '18': '>',
    '19': '>=',
    '20': '<',
    '21': '<=',
    '22': '!=',
    '23': '==',
    '24': '!',
    '25': '&&',
    '26': '||',
    '27': ',',
    '28': '=',
    '29': '[',
    '30': ']',
    '31': '(',
    '32': ')',
    '33': '{',
    '34': '}',
    '35': ";",
    '38': '#'
}


if __name__ == '__main__':
    read_path = 'source_code.txt'
    sourceCodes = readSourceCode(read_path)
    codeToInputs(sourceCodes)
    while inputs[i] != '#':
        nextToken()
        i += 1
    tokens.append(MyToken(38, "^", "#"))  # 最后一个
    ch = ""     # 输入串(存储词法分析的结果)
    for token in tokens:
        ch += grammarDict.get(str(token.MyType), "") + " "

    inputs = stack()  # 存储待识别字符串
    sem = stack()  # 存储文法
    index = 0
    # 从文件中读取产生式
    file_path = 'file.txt'  # 替换为你的文件路径
    grammar = read_grammar_from_file(file_path)
    # 存储文法开始符号
    start_symbol = grammar['start_symbol']
    first_sets = {}
    follow_sets = {}
    printFirst(grammar)  # 计算并打印First集
    printFollow(grammar)  # 计算并打印Follow集
    LLTable = initLLTable()

    printLLTable(LLTable)  # 打印预测分析表
    # 存储分析栈
    LLStack = "#" + start_symbol
    # 存储剩余输入串
    input_tokens = ch.split()  # 使用空格分隔字符串，并得到token列表
    # 存储剩余输入串
    strings = input_tokens
    print(" ".join(strings).replace("#",""))
    # 反向入栈
    for token in reversed(input_tokens):
        inputs.push(token)
    sem.push('#')
    sem.push(start_symbol)
    init()
    print("-------------------------------------------------")
    print("|{:16} {:20} {}|".format('分析栈', '剩余串', '产生式'))
    LL_driver()


