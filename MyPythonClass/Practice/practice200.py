class practice200:
    @staticmethod
    def main():
        # 使用print把变量用不同方法拼接起来，并计算最高股价
        name = "AR pte community"
        stock_price = 19.99
        stock_code = 114514
        stock_code_daily_growth_factor = 1.2
        growth_days = 7
        stock_most_growth = stock_price * stock_code_daily_growth_factor ** growth_days

        print(f"The company : {name}, the stock code: {stock_code}, current price: {stock_price}")
        print("The daily growth factor is %f, the stock at the top price is %.2f after growing around %d days" %(stock_code_daily_growth_factor,stock_most_growth,growth_days))

# %%
class practice201:
    @staticmethod
    def main():
        # 定义两个变量，获取用户输入内容，并给提示信息
        user_name = input("Welcome user, please enter your name: ")
        user_type = input("Please enter your current level: ")
        
        print(f"Welcome {user_name}, your are current level {user_type}")
# %%
if __name__ == "__main__":
    practice201.main()     