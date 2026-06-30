# %%
class Me200:
    @staticmethod
    def main():
        # literial字面量
        "haha"                   # python可以不给变量赋值的情况下，直接孤立设置字面量
        66                       # 定位为，写死在源代码中的固定值，绝对不可改变 （比常量还常量）
        print(66)

# %%
class Me201:
    @staticmethod
    def main():
        # variable变量    
        # Primitive Types基本类型
            # immutable Object不可变类型
            a1 = 66                        # integer数字
            a2 = 44342
             
            b1 = 33.45                     # float小数点
            b2 = 3.2
            
            c1 = "Helo"                    # String字符串
            c2 = "def"
            
            d1 = 4+3j                      # complex复数，带有j字母做结尾
            d2 = 6.1j

            e1 = True                      # boolean，布尔值判断类型，int的子类，
            e2 = False                     # 必须大写，否则报错
 
            f1 = (1,2,3)                   # truple元组，不可变版list，用（）圆括号表示，拿来装和读而已
            f2 = (4j,67,"WEAR")

            g1 = frozenset({1,2})          # frozenset不可变集合，哈希值固定，可以作为dict的key或set的元素
            g2 = frozenset({37j,"bear"})   
            g3 = {                         # dict key：value映射，整个dict(key)与value绑定关系
                 g1: "value"
            }
            g4 = {                         # 集合元素，只存元素
                 g2
            }

            print(d1)
            # mutable Object可变类型    
            h1 = [1,2,2,3.5]               # list列表，有序可重复相同，用[]方括号表示，能随便改，能放任何东西
            h2 = [1j , "we"]

            i1 = {1: "value", "key": 2}    # dictionary字典，用key: value表示映射关系，用名字找东西
            i2 = {1:1 , 2:2}

            j1 = {1,2,3}                   # set去重集合，无序不可重复唯一，用{}花括号表示，自动帮你去重的一堆东西
            j2 = {4j, 8.2,"we"}

# %%
class Me202:
     @staticmethod
     def main():
          # Identifier标识符命名规则
          print("str = 5 ")                # 不可使用或同名系统关键词作为标识符，否则报错
          print("num")                     # 标识符必须先定义其值再使用，否则报错
          print("a = 5")                   # 标识符只能包含"a~z","0~9","_"
          # 开头只能"a~z","_"

          '''
          name
          age
          # 开头a~z, 可以运行

          best_2024
          city1977
          # 虽然后面是数字但前面开头是字母，可以运行

          _first
          _13theme
          # 只要开头是"_",后面可以跟数字或字母

          5th
          81days
          # 开头数字,报错

          price$;
          _we@;
          # 如果包含"_"以外的符号，不管开头是字母还是"_",报错

          '''
          print("a = 5; a = 3")            #同一段域，Java中不可重复定义，Python则允许覆盖赋值
          print("a = 5; A = 3")            #但同段域，标识符可通过大小写区分定义，但可读性变差，不建议
          print("apple = 5")               #变量命名尽量见名知义，增加可读性，详情Me103.py
          #无论python, java还是其他语言，大小写非常敏感，A和a不是一回事

# %%
class Me203:
     @staticmethod
     def main():
        # Comment单行注释
        '''
        多行注释                            # """表示多行注释"""
        多行注释                            # 严格来说这还是字符串对象,如果没有赋值使用,python还是会自动忽略
        '''
        # 多单行ctrl + /快捷注释
        # 根据官方的语法规范和增加可读性，# 号右边和注释内容间隔尽可能空一格

# %%
class Me204:
     @staticmethod
     def main():
          # variable变量
          # 储存计算结果和表示值
          # 也能直接使用字面量，但效率极其拉跨
          # 变量名 = 变量值
          money = 50
          print("i have", money, "dollars")        

          money = money - 10                       # 无需新定义变量，可以直接减去特定值再赋回给原变量
          print("i have", money, "dollars")

          money -= 10                              # 更便捷，可以使用-=累减（自己减去特定的值）
          print("i have", money, "dollars")

# %%
class Me205:
     @staticmethod
     def main():
          # print字符串拼接
          age = 12
          print("Hello, I'm " + "age" + " years old")
          # python拒绝隐式类型转换，+在字符串和数学上分别是拼接与加法，在这个语言不同类型拼接容易造成冲突

          print("Hello, I'm", age , "years old")
          # 方法1，用逗号隔开，最初学，最简单

          print(f"Hello, I'm {age} years old")
          # 方法2，f-string拼接，最现代，最推荐

          print("Hello, I'm " + str(age) + " years old")
          # 方法3，str手动转换，此时可以使用+拼接

          print("Hello, I'm {} years old".format(age))
          # 方法4，format拼接

          print("Hello, I'm %s years old" %age)
          # 方法5，%格式化
          

# %%
class Me206:
     @staticmethod
     def main():
          # %格式化和精度控制
          age = 12
          name = "Ama"
          money = 14324.57

          # %格式化, 也叫占位拼接， 先占个位子，等写完内容才在后面写要插入的内容
          # %s 插入字符串， %d插入整数， %f插入浮点数
          # 多个要插入的内容，变量要括号框起来，按照占位顺序填入，多一个少一个都不行
          # 如果日常简单打印，可以统一使用%s来转换成字符串，如果需要控制整数或小数点，就不能统一使用%s
          print("Hello, my name is %s, I'm %d years old, I have %.2f dollars" % (name, age, money))

          # 精度控制使用 "%m.nf"，只能对数字生效
          # m控制整体最小宽度，n控制小数点后的位数，两个单用相不干涉
          print("%8d" %money)                      # 如果m的宽度大于变量的值的宽度，前面用空格替位
          print("%4d" %money)                      # 反之小于，不生效

          # %.2f控制精度，不限制前面宽度, 2代表小数点数位
          print("%.3f" %money)                     #如果n的精度，大于变量的值的精度，后面用0替位
          print("%.1f" %money)                     #反之小于，会按指定小数位四舍五入，57的小数点变成6

          # "m.n"两个单用相不干涉，但如果同时使用，n的精度会算进m的整体宽度内
          print("%5.2f" %money)                    # 整数5个数字，但同时使用，已算入后面的小数点，这时m小于变量值宽度，不生效
          print("%13.5f" %money)                   
          # mn宽精度大于变量值，n后面用0代替，m把后面0的精度算进宽度，总共11位数，但m还是大于总位数，m前面用空格代替
          # m基本上很少使用，大致了解就行，只需知道n，现在推荐f-string拼接法

# %% 
class Me207:
     @staticmethod
     def main():
          # print表达式
          # print可以再不设置变量的情况下直接输出结果，和字面量类似
          print(1+1)
          print(f"i have {1+1*1} pens")            
          print("the type of \"pen\" is %s" %type("pen"))
          # 通常情况下，还是设置变量为好
          pen = 1 + 1 * 1
          print(f"i have {pen} pens")   

# %%
class Me208:
     @staticmethod
     def main():
          # type基本常用类型
          a1 = 1                                   # int整数类型
          a2 = 2.4                                 # float浮点型，存小数点
          a3 = "pen"                               # str字符串类型，""逗号引起来的都是字符串

          # 使用type()查看数据类型
          print(type(a1))
          print(type(a2))
          print(type(a3),"\n")

          # 直接输入值查看类型
          print(type(1))
          print(type(2.4))
          print(type("pen"),"\n")

          # 变量类型也可以储存类型信息
          name = type(a1)
          print(name)

          # type()查看的是数据类型而不是变量类型，变量本身没有，但它储存的数据有

# %%
class Me209:
     @staticmethod
     def main():
          # 数据类型转换
          # 默认条件下，读取数字可能得到的是字符串类型，需要手动转换成数字类型
          num = "123"
          num = int(num)                           # 转换成数字
          print(type(num))

          num = float(num)                         # 转换成浮点数
          print(type(num))
 
          num = str(num)                           # 转换成字符串
          print(type(num))
          # 和type语句一样，都有带返回值，可以直接print输出或者存进变量

# %%
class Me210:
     @staticmethod
     def main():
          # 强制与自动类型转换
          # 目标类型根据原类型权重，进行自动转换  int < float < str

          result = 1 + 2.5
          print(result)                            # int + float, float大于int, 结果自动转换为float
          # 原类型 < 目标类型，float可以cover整数和小数，int只可以cover整数

          num = 3.4 + 6.8
          num = int(num)                           # int + float, float大于int, 但结果要取整，这时必须取强制转换成int
          print(num)                               # float转换int时，int无法读取小数点，后面的内容会被隐藏
          # 目标类型 < 原类型，int无法cover float，需要从float强制转换成int

          hello = 123      
          hello = str(hello)                       # 字符串转换数字，无法自动转换，必须是手动强制转换
          print(hello)

          world = "45.6"
          world = float(world)                     # 如果字符串为小数点，不可以直接越级转换成int，需要先转换成float再转换成int
          world = int(world)
          print(world)

          word = "你好"
          print(int(word))                         # 错误类型转换
          # 要将字符串转换数字，内容必须是数字，不可以字母字符，否则报错

# %%
class Me211:
     @staticmethod
     def main():
          # 数字运算符 （普通运算）
          num = 1 + 1                              # +号，两个号相加
          print(num)

          num = 1 - 1                              # -号，两个号相减
          print(num)

          num = 2 * 3                              # *号，两个号相乘
          print(num)

          num = 3 / 3                              # /号，两个号正常相除  
          print(num)
          # python普通相除，变量类型自动转换成float，取的结果默认带小数点
          # java中强制规定变量类型，普通相除只能根据原类型取结果，想要另一种结果只能通过强制类型转换

          num = 7 // 3                             # //取整除，取除结果为int整数
          print(num)

          num = 7 % 3                              # %取余除，两个号整除后取无法整除的部分
          print(num)
          # 任何类型的除如果除数为0，报错

          num = 7 ** 3                             # **指数，双乘号，平方乘7^3
          print(num)

# %%
class Me212:
     @staticmethod
     def main():
          # 数字运算符（赋值运算）
          num = 10                                 # =号，赋值符，把右边的特定值赋给左边的变量，不是数学常用的等于符
          print(num)

          num += 1                                 # 累加，等同于 num = num + 1,便捷写法
          print(f"num += 1: {num}")

          num -= 1                                 # 累减，等同于 num = num - 1,便捷写法
          print(f"num -= 1: {num}")

          num *= 1                                 # 累乘，等同于 num = num * 1,便捷写法
          print(f"num *= 1: {num}")

          num /= 1                                 # 累除，等同于 num = num / 1,便捷写法
          print(f"num /= 1: {num}")

          num //= 3                                # 累整除，等同于 num = num // 3,便捷写法
          print(f"num //= 1: {num}")

          num %= 4                                 # 累余除，等同于 num = num % 4,便捷写法
          print(f"num %= 1: {num}")

          num **= 2                                # 累指数，等同于 num = num ** 2,便捷写法
          print(f"num **= 1: {num}")          

# %%
class Me213:
     @staticmethod
     def main():
          # 字符串定义方式
          name = 'hello'                            # 单引号
          name2 = "world"                           # 双引号
          # 底层上，单引和双引没有本质区别，可以根据情况随意切换

          name3 = '''hello 
          world'''                                  # 三引号
          # 和多行注释写法一样，赋给变量就是字符串，不赋就是注释
          print(type(name))
          print(type(name2))
          print(type(name3))

          # 引号嵌套
          mini = "'hello'"                          # 双引号内单引号
          print(mini)
          mini2 = '"world"'                         # 单引号内双引号
          print(mini2)

          # 单双不同类型引号可以直接嵌套

          # 相同类型引号嵌套可以使用"\"转义
          mini3 = """\"hello world\""""             # 三引号内双引号
          print(mini3)
          mini4 = '\'welcome\''                     # 单引号内单引号
          print(mini4)

# %%
class Me214:
     @staticmethod
     def main():
          # input输入内容
          # 使用input可接受用户输入内容
          name = input()            
          print(f"My name is {name}")

          name2 = input("tell me your name: ")      # input内输入字符串，可再单行同时显示字符串和输入光标
          print(f"Your name is {name2}")

          age = input("Tell me your age: ")
          age = int(age)                            # input默认接受类型是str，特定情况需要转换类型
          print(f"your age is {age}，type is {type(age)}")

          height = int(input("Tell me your height: "))   # input也可以一开始就定义类型，类型(input())
          print(f"Your height is {height}, and type is {type(height)}")

# %%
if __name__ == "__main__":
    Me214.main()        
