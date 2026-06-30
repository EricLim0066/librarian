import random

class practice300:
    @staticmethod
    def main():
        # 演示输出结果和类型
        boo1 = True
        boo2 = False
        print(f"content of boo1 is {boo1}, the type is {type(boo1)}")
        print(f"content of boo2 is {boo2}, the type is {type(boo2)}")

        # 使用运算符进行打印比较
        num = 10
        num1 = 10
        num2 = 15
        print(f"the result of num == num1 is {num == num1}")
        print(f"the result of num != num2 is {num != num2}")

        # 字符串也可使用==比较
        # python的str类内部已实现__eq__魔法方法，所以可以直接使用==比较
        name = "hello"
        name1 = "hello"
        print(f"the result of name == name1 is {name == name1}")

        # 使用比较符进行打印比较
        num = 10
        num1 = 10
        num2 = 15
        print(f"the result of num > num1 is {num > num1}")
        print(f"the result of num < num2 is {num < num2}")
        print(f"the result of num >= num1 is {num >= num1}")
        print(f"the result of num <= num2 is {num <= num2}")

# %%
class practice301:
    @staticmethod
    def main():
        # 使用if，在特定条件达成时，执行语句
        age = int(input("Plese enter your age: "))

        print(f"I'm {age} years old")
        if age >= 18:
            print("I'm ready my university life")

        print("Time is fast")    

# %%
class practice302:
    @staticmethod
    def main():
        #使用input语句，为age赋值，判断是否成年人
        print("Welcome to Fun Fair")

        age = int(input("Please enter your age: "))        
        if age >= 18:
            print("You're adult, need to pay more 10 dollars for extra")
        else :
            print("You're not adult, can play for free")    

        print("Have a fun time !")    

# %%
class practice303:
    @staticmethod
    def main():
        #使用input，判断身高是否超过120厘米
        print("Welcome to zoo!")
        height = int(input("Please enter your height (cm): "))
        if height >= 120 :
            print("Your height is above 120cm, need to pay extra 10 dollars")
        else :
            print("Your height is below 120cm, can visit for free")
        print("have a nice day")        

# %%
class practice304:
    @staticmethod
    def main():
        #使用input，同时判断身高是否少于120厘米或vip等级高于5
        print("Welcome to zoo !")
        height = int(input("Please enter your height (cm): "))
        vip_level = int(input("Please enter your vip level: "))

        if height < 120:
            print("Your height is below 120cm, can play for free")
        elif vip_level >= 5:    
            print("Your vip level is above 5, can play for free")
        else:
            print("Sorry your conditions not met, need to pay extra 10 dollars")    
        print("Have a great time !")    

# %%
class practice305:
    @staticmethod
    def main():
        # 使用if elif else制作猜数字游戏
        num = 10
        
        print("Guess what number i think, range is 1 ~ 10")
        if int(input("First try: ")) == num :
            print(f"You're correct! It's {num}")
        elif int(input("Incorrect! second try : ")) == num :
            print(f"You're correct! It's {num}")
        elif int(input("Incorrect again! last try : ")) == num :
           print(f"You're correct! It's {num}")
        else :
            print(f"Sorry, all are incorrect! Answer is {num}")

# %%
class practice306:
    @staticmethod
    def main():
        # 使用嵌套，身高是否少于120厘米或vip等级高于5
        print("Welcome to zoo !")
        height = int(input("Please enter your height (cm): "))
        
        if height > 120:
            print("Your height is above 120cm, cannot play for free")
            print("but if have vip more than 5, can play for free")

            vip_level = int(input("Please enter your vip level: "))
            if vip_level >= 5:    
                print("Your vip level is above 5, can play for free")
            else :
                print("Sorry you all conditions not met, need to pay extra 10 dollars")    

        else:
            print("Your height is below 120cm, can play for free")    

        print("Have a great time !")    

# %%
class practice307:
    @staticmethod
    def main():
        # 公司发放礼物，条件为
        # 必须大于等于18或30岁，并且入职超过两年或级别大于3才可领取
        print("Our company will send a gift to all employees who's age between 18 and 30")
        age = int(input("Please enter your age: "))

        if age >= 18 :
            if age <= 30:
                print("Your age is above 18 and below 30, but must work in here above 2 years or level more than 3")

                work_years = int(input("Please enter how many years you work here:"))
                level = int(input("Please enter how many level:"))
                if work_years > 2:
                    print("Your work years more than 2, can take the gift now")
                elif level > 3:
                    print("Your level more than 3, can take the gift now")    
                else :
                    print("Sorry your work years not above 2 or level not above 3, cannot take the gift") 

            else :
                print("Sorry your age is not below 30, cannot take the gift")    

        else :
            print("Sorry your age is not above 18, cannot take the gift")    

# %%
class practice308:
    @staticmethod
    def main():
        # random随机数，通过导包加入
        # 通过random随机数，用三次判断猜出数字
        print("We play a game to guess a number is between 1 ~ 10")
        num = random.randint(1,10)                   # randint(最小范围，最大范围)
        guess_num = int(input("Guess the first number: "))

        if guess_num == num:
            print(f"You're correct! answer is {num}")
        else :
            if guess_num < num:
                print(f"Guess bigger!")
            else :
                print(f"Guess smaller!")

            guess_num = int(input("Continue guess! The second number: "))    
            if  guess_num == num:
                print(f"You're correct! answer is {num}")
            else :
                if guess_num < num:
                    print(f"Guess bigger!")
                else :
                    print(f"Guess smaller!")   

                guess_num = int(input("Continue guess! The last number: "))  
                if  guess_num == num:
                    print(f"You're correct! answer is {num}")
                else :
                    print(f"Oh no! You're worng! answer is {num}")


            

# %%
if __name__ == "__main__":
    practice308.main()        

