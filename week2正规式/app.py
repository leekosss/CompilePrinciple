# -*- coding = utf-8 -*-
# pattern = "b(ab|bb)*ab+"

strings = input("请输入需要判断的字符串:\n")
index = 0
if index == 0 and strings[index] != 'b':  # 判断第一个是否为b
    print("no")
    exit(0)

flag = -1
pos = -1
for i in range(len(strings) - 1, -1, -1):  # 判断最后是否为：ab+
    if i == len(strings) - 1 and strings[i] != 'b':  # 如果最后一个不是b
        flag = -1
        print("no")
        exit(0)
    if i == len(strings) - 1:  # 最后一个是b，就让下标先-1
        continue
    if strings[i] == 'a' and strings[i + 1] == 'b' and i == len(strings) - 2:  # 如果结尾是ab
        pos = i
        break

    if strings[i] == 'b' and strings[i + 1] == 'b':  # 如果从后往前字符全是b，就让flag=1
        flag = 1
    elif flag == 1 and strings[i] == 'a' and strings[i + 1] == 'b':
        # flag=1 时，如果当前字符为a，则满足条件
        pos = i
        break
    else:
        flag = -1

index = 1
while index < pos:
    s1 = strings[index] + strings[index + 1]
    s2 = strings[index] + strings[index + 1]
    if index + 1 < pos:
        if s1 == "ab" or s2 == 'bb':  # 如果中间为(ab|bb)
            index += 2
            continue
        else:
            print("no")  # 不满足就错
            exit(0)
    else:   # 中间为奇数则错
        print("no")
        exit(0)

if index == pos:  # 如果只有三个字符bab，则满足
    print("yes")
    exit(0)

print("no")