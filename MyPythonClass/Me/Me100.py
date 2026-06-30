# %%
class Me100:
    @staticmethod
    def main():

        print("Hello World")                #print打印
        #
        print("Hello")                      #print打印默认换行
        print("World")
        #
        print("Hello", end="")              #后缀添加end=可达成不换行效果
        print("World")                      #end=内添加空格可以分离单词
        #

# %%
class Me101:
    @staticmethod
    def main():
        #cmd运行代码 （win+R)
        #输入python
        #输入print("Hello World")
        
        #cmd常见报错原因
           #设备无法初始化                   #未先输入python字样而直接输入代码，确保输入python弹出右指箭头
           #不是内外部命令                   #安装时未勾选add python to path，卸载再重新安装
           #SyntaxError invalid character   #符号使用外语输入，确保输入的符号是原生英语
        print ("")

# %%
class Me102:
    @staticmethod
    def main():
        print("Hello\tworld")               #\t tab空格
        #
        print("hello\nWorld")               #\n字符串内换行，与print两次同等
        #
        print("hello", end="\n")            # end="\n" = normal print
        print("world")
        #
        print("hello World\n")              #print + \n = double change line
        print("hi")

#python没有java便捷的段落/多行注释
#ctrl + /快捷注释

# %%
class Me103:
    @staticmethod
    def main():
        #代码可以脱离class框架下编写，自由度比java高
        print("A");print("B");print("C")    #一行尽量一条语句/指令，还是能运作但可读性变差
        #
        print("D");                         #；分号虽然不报错，但不需要像其他的语言强制分号,不用顺手写
        #
        i = 5
        if i == 5:                          #条件不需要像其他语言用（）
            print ("yes")                   #python使用：代表内部框架，其他语言大多用{}花括号

        # ：冒号很难让程序员知道该变量属于哪个段落哪个框架，而{}会非常清晰代表某段落边界，现有版本可以抵消此问题                                    

# %%
class Me104:
    @staticmethod
    def main():
        print ("hi")
        # ：可以代表一个框架房间，里面：代表还有房间，即房中房

# %%        
if __name__ == "__main__" :
    Me103.main()