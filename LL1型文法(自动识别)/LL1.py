calculated = {}


# 递归计算first集
def calculate_first(symbol):
    first_set = set()

    # 如果该符号已经计算过了，直接返回其First集
    if symbol in calculated:
        return calculated[symbol]

    # 遍历每个产生式
    for production in grammar['productions']:
        left_symbol = production[0]
        right_symbols = production[1:]

        # 找到以当前非终结符为左部的产生式
        if left_symbol == symbol:
            # 处理右部的每个符号
            for right_symbol in right_symbols:
                # 处理终结符，将其添加到当前非终结符的First集中
                if right_symbol in grammar['terminals']:
                    first_set.add(right_symbol)
                    break
                # 递归处理非终结符，
                elif right_symbol in grammar['non_terminals']:
                    symbol_first = calculate_first(right_symbol)
                    # 将其First集（除去空符号ε）添加到当前非终结符的First集中
                    first_set.update(symbol_first - {'ε'})

                    # 如果该非终结符的First集有一个不包含空符号ε，说明已经推导出终结符了
                    # 此时应该break，防止for执行后面的else添加ε到first集
                    if 'ε' not in symbol_first:
                        break
            else:
                # 如果右部所有符号都能推导出空符号ε，将空符号ε添加到当前非终结符的First集中
                first_set.add('ε')

    calculated[symbol] = first_set
    return first_set


# 使用迭代求first集
def calculateFirst(ch):
    if ch in grammar['terminals']:
        return set(ch)

    first_sets = {symbol: set() for symbol in grammar['non_terminals']}
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
                        first_sets[left_symbol].update(right_symbol)
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

def error():
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
        # 是终结符
        if sc in grammar['terminals']:
            if ic == sc:  # 非终结符相等就出栈
                print(f"{LLStack:20} {strings:20} '{ic}' 匹配")
                LLStack = LLStack[:-1]
                strings = strings[1:]


                inputs.pop()
                sem.pop()
            else:
                error()
        # 非终结符
        elif sc in grammar['non_terminals']:
            # 获得LL1分析表中的数值来执行相应算法
            productions = LLTable[vn2int(sc)][vt2int(ic)]
            # 如果产生式的列表为空，代表源输入串有误
            if not productions:
                error()
            # 遍历分析表中同一格的多个产生式
            for LLProduction in productions:
                for production in grammar['productions']:
                    # 如果分析表的产生式与文法中产生式相等
                    if LLProduction == production:
                        non_terminal = production[0]
                        right_symbols = production[1:]

                        productionStr = non_terminal+"->"+"".join(right_symbols)
                        print(f"{LLStack:20} {strings:20} {productionStr:20}")
                        LLStack = LLStack[:-1]

                        sem.pop()
                        for right_symbol in reversed(right_symbols):
                            sem.push(right_symbol)
                            LLStack += right_symbol
                        break
        elif sc == 'ε':
            LLStack = LLStack[:-1]
            print(f"{LLStack:20} {strings:20} ε")

            sem.pop()
            sc = sem.read()
            continue
        # else:
        #     error()

        ic = inputs.read()  # 当前识别的字符
        sc = sem.read()  # 文法中的字符

    if ic == '#' and sc == '#':
        print("accept!")
    else:
        error()


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
            right_symbols = [symbol.strip() for symbol in production_parts[1]]

            grammar['productions'].append((left_symbol, *right_symbols))
            grammar['non_terminals'].add(left_symbol)
            grammar['terminals'].update(symbol for symbol in right_symbols if symbol.isalpha() and symbol.islower() and symbol != 'ε')
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
        print(f"{terminal:<30}", end=' ')
    print()

    # 打印分析表
    for non_terminal in non_terminals:
        print(f"{non_terminal:<10}", end=' ')
        for terminal in terminals:
            productions = LLTable[non_terminal].get(terminal, [])
            if productions:
                leftmost_production = productions[0]  # 取第一个产生式
                # leftmost_str = '->'.join(leftmost_production)  # 拼接最左边箭头产生式
                leftmost_str = leftmost_production[0]+"->"+"".join(leftmost_production[1:])
                print(f"{leftmost_str:<30}", end=' ')
            else:
                print(f"{'':<30}", end=' ')
        print()


if __name__ == '__main__':

    inputs = stack()  # 存储待识别字符串
    sem = stack()  # 存储文法
    index = 0
    ch = input('请输入字符串:')  # 待识别的字符串
    ch += '#'
    # 从文件中读取产生式
    file_path = 'file.txt'  # 替换为你的文件路径
    grammar = read_grammar_from_file(file_path)
    # 存储文法开始符号
    start_symbol = grammar['start_symbol']
    first_sets = {}
    follow_sets = {}
    printFirst(grammar)     # 计算并打印First集
    printFollow(grammar)    # 计算并打印Follow集
    LLTable = initLLTable()
    printLLTable(LLTable)   # 打印预测分析表

    # 存储分析栈
    LLStack = "#" + start_symbol
    # 存储剩余输入串
    strings = ch

    # 反向入栈
    for c in reversed(ch):
        inputs.push(c)
    sem.push('#')
    sem.push(start_symbol)
    print("-------------------------------------------------")
    print("|{:16} {:20} {}|".format('分析栈','剩余串','产生式'))
    LL_driver()


