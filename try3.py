def practice1() :
    # list
    original_list = [1,2,3]

    new_list = original_list
    # 不是复制！只是多一个名字指向同一个 list
    new_list1 = original_list[:]
    new_list2 = list(original_list)
    new_list3 = original_list.copy()
    # 都是浅复制 

    print(new_list)
    print(new_list1)
    print(new_list2)
    print(new_list3)   

def practice2() :
    # set
    a = {"Ali","Sarah","John"}
    b = {"John","Elena","Mei"}
    
    c = a.intersection(b)
    # 交集，拿重复的 {John}
    print(c)
    c = a.union(b)
    print(c)
    # 并集，拿所有，去除重复的 {John}
    c = a.difference(b)
    print(c)
    # 差集，拿只有a有的

    my_set = {}
    print(type(my_set))
    # set空的情况下，默认为dict，type查看输出结果为dict
    my_set = set()
    print(type(my_set))
    # 这才是空set

    my_set = {101,102,101,103,104}
    print(my_set)
    my_dict = {101 :"a",102 : "b",101 : "a",103: "c",104: "d"}
    print(my_dict)
    # set会自动去重,
    # dict只看key唯一性，重复key后者覆盖前者，虽然效果和set去重一样但不是一回事，只有value重复不去重

def practice3() :
    # dict
    grades ={"Quiz": 85, "Quiz2" : 90}

    print(grades.get("Quiz3", 3))
    # key不存在，返回默认值, 3
    
    # grades["Quiz3"]
    # key不存在，报错 

    print(grades.keys())
    # 打印key
    print(grades.values())
    # 打印value
    print(grades.items())
    #打印所有

    for k, v in grades.items():
        print(k, v)
        # 用于打印遍历
    
    record = {1: "a",90: "b"}
    90 in record
    # in 只会检查key,不检查value
    # "b" in record
      

def practice4() :
    # turple
    point = (10,20,30)
    point[1] = 25
    # 不可变，东西是死的

    info = ("diploma", "fci", 2026)
    program,faculty,year = info
    print(f"{program},{faculty},{year}")
    #快速拆包/赋值

# practice4()    
def practice5() :
    # list insert remove pop
    number = [10,20,30,40]
    number.insert(1,10)
    # (index, value)index 1位置插入 10

    number.remove(30)
    # 删除value 30

    number.pop(1)
    # pop带参，删除index位置的元素
    number.pop()
    # pop不带参，默认删除最后位置的元素
    print(number)

    items = [1,2,3,4,5]
    print(items[1:4])
    # item[1:4]为半开区间，包含index 1不包含index 4
    # 数学不等式写法为(1 <= x < 4)
    
def practice6():
    # loop for continue break
    arr = [1,2,3,4,5]
    target = 3
    index = 0
    while index < len(arr):
        if arr[index] == target:
            found_at = index
            print(found_at)
            break          
        # break 找到立刻跳出，index 不会再 +1
        # continue 跳过本次循环，继续下一轮循环
        print(index)
        index += 1

    values = [1, 2, 3, 4]
    for i in range(len(values)):
        values[i] = values[i] * i
    # range(len(list)),循环同等list长度的次数，如果只有len(list)，默认i从0开始循环 
    # 拿index或修改list1

def practice7() :
    # 2d list
    matrix = [[1,2,3], [4,5,6], [7,8,9]]
    print(matrix[1][2])
    #抽取精准元素，抽取index[1]的数组，再抽取里面为index[2]的数组

def practice8():
    # find max value
    dataset = [-12,-3,-2]
    highest = dataset[0]
    # dataset 找最大值
    # 初始值不可以设成0,如果list数字为负数会出错
    # 换个说法，dataset loop前没有关联到highest，loop出来的答案不是list里面的
    for val in dataset:
        if val > highest:
            highest = val
        print(highest)        
            
    # i in list, 拿里面的值一个个迭代循环，循环次数为list长度
    # i in range()，普通循环，如果只有一个参数，默认为从0开始循环


def practice9():

    def calculate_total():
        x = 6
        print(f"max num is {x}")
    # 普通写法，函数内部说了算，外部无法干预

    def calculate_total1(x = 6):
        print(f"max num is {x}")
    # 传参默认写法，函数外部说了算，外部不传值时使用参数默认值



    def calculate_total2(items, tax_rate=0.06):   
        subtotal = sum(items)
        # sum 求数组总和
        return subtotal * (1 + tax_rate)

    result = calculate_total2([10, 20, 30])
    print(result)
    # 如果没有传参第二个，用默认 tax_rate
    result2 = calculate_total2([10, 20, 30], 0.1)  
    print(result2)
    # 有传参第二个，覆盖默认值

    #有return，返回/传出该值，没有或有空return默认返回nope
    # return传出来的东西，给变量或拿来传参

    def add_item(lst):
        lst.append(99)
        return lst
    
    my_list = [1,2,3]
    add_item(my_list)
    print(my_list)
    # 传参后，外面一并被更改
    
practice6()        