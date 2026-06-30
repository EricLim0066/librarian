# %%
class Me300:
    @staticmethod
    def main():
        # 逻辑判断
        # 使用布尔值类型(boolean)表达逻辑关系，即真(True)或假(False)两种结果而已
        # python底层上，True记作数字1，False记作数字0
        True                                            # True表示是"对"
        False                                           # False表示"错"

        # 基础表达关系
        # 使用type查看变量布尔值类型
        result = 10 > 5
        print(f"result is {result},{type(result)}")     # 10大于5是对的，输出True 
        result = 5 > 10
        print(f"result is {result},{type(result)}")     # 5大于10是错的，输出False 
        

# %%
class Me301:
    @staticmethod
    def main():
        # 逻辑表达符
        print(">")                                      # 大于符
        print("<")                                      # 小于符
        print("<=")                                     # 大于等于符
        print(">=")                                     # 小于等于符
        print("==")                                     # 等于符，这才是数学意义上的等于符，单等于的是赋值符
        print("!=")                                     # 不等于符

# %%
class Me302:
    @staticmethod
    def main():
        # if基础逻辑判断语句
        # 进行判断时，只能是布尔值(boolean)类型，即对或错两种答案
        age = 30
        if age > 18:                                    # if 执行条件： 
            print("I'm adult")                          # 条件为对就执行，为错不执行

class Me303:
    @staticmethod
    def main():
        # if else基础逻辑判断语句
        # else是为条件为错时可执行的语句，不可单独使用，必须跟紧if和elif
        age = 30
        if age > 18:                                    # if 执行条件： 
            print("I'm adult")                          # if 条件为对就执行
        else :
            print("I'm not adult")                      # else 条件为错就执行

class Me304:
    @staticmethod
    def main():
        # if elif else基础逻辑判断语句
        # 如果判断条件不止一个，就可以使用elif接上多个
        # 排在最前，并且符合的条件，优先执行，即if符合，elif else不执行, if不符合但elif符合，else不执行，都不满足，才去else
        age = 30
        if age > 18:                                    # if 执行条件： 
            print("I'm adult")                          # if 条件为对就执行
        elif age == 18:
            print("I'm 18 years old")                   # elif 条件不符合上面情况又符合其他情况，可以用elif衔接
        else :
            print("I'm not adult")                      # else 全部条件为错就执行

# %%
class Me304:
    @staticmethod
    def main():
        # if else多层嵌套
        # 如果判断不止一个，并且每个判断还需要再分支判断，需要嵌套
        age = 30
        if age >= 13:                                       # if 执行条件： 
            if age <= 17:                                   # if 外层符合条件时才会执行内部判断
                print("I'm secondary school student")       
            else :
                print("I'm adult")
        else :                                              # else 外层不符合条件时才会执行内部判断
            if age > 6:
                print("I'm primary school student")         
            else :
                print("I'm kids")
        
       

# %%
if __name__ == "__main__":
    Me304.main()

