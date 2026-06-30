from tkinter import *

# 创建窗口
root = Tk()
root.title("Ultimate Calculator")
root.geometry("350x500")
root.config(bg="black")

# 输入框
entry = Entry(root, font=("Arial", 28), bd=10, relief=RIDGE, justify="right")
entry.pack(fill=BOTH, ipadx=8, pady=20, padx=10)

# 按钮点击

def click(num):
    current = entry.get()
    entry.delete(0, END)
    entry.insert(0, current + str(num))

# 清空

def clear():
    entry.delete(0, END)

# 计算

def calculate():
    try:
        result = eval(entry.get())
        entry.delete(0, END)
        entry.insert(0, str(result))
    except:
        entry.delete(0, END)
        entry.insert(0, "Error")

# 按钮布局
buttons = [
    ['7', '8', '9', '/'],
    ['4', '5', '6', '*'],
    ['1', '2', '3', '-'],
    ['0', '.', '=', '+']
]

for row in buttons:
    frame = Frame(root, bg="black")
    frame.pack(expand=True, fill=BOTH)

    for btn in row:
        if btn == '=':
            b = Button(frame, text=btn, font=("Arial", 22), bg="orange", fg="white",
                       command=calculate)
        else:
            b = Button(frame, text=btn, font=("Arial", 22), bg="gray20", fg="white",
                       command=lambda x=btn: click(x))

        b.pack(side=LEFT, expand=True, fill=BOTH, padx=2, pady=2)

# Clear按钮
Button(root, text="CLEAR", font=("Arial", 20), bg="red", fg="white",
       command=clear).pack(fill=BOTH, padx=10, pady=10)

root.mainloop()   

