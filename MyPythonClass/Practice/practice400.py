
import random
# %%
class practice400:
    @staticmethod
    def main():
        # 使用while求1 ~ 100的总和
        num = 1
        temp = 0

        while num <= 100 :
            temp += num
            num += 1
        print(temp)

# %%
class practice401:
    @staticmethod
    def main():
        # 使用while制作猜数字游戏，次数不限直到猜中,需要记录猜测次数
        num = random.randint(1, 100)
        min_num = 1
        max_num = 100
        time = 0
        flag = True                                                   # 添加布尔值变量判断是否继续下去
        while flag :
            time += 1
            guess_num = int(input(f"Pleass guess the number between {min_num} and {max_num}: "))
            if guess_num > num :
                max_num = guess_num
                print(f"Continue guess! It's between {min_num} and {max_num}")
            elif guess_num < num :
                min_num = guess_num
                print(f"Continue guess! It's between {min_num} and {max_num}")
            else :
                print(f"congratulations! answer is {guess_num}, total of guess is {time}")
                flag = False

# %%
if __name__ == "__main__" :
    practice401.main()