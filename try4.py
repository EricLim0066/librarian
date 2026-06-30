def num_calc():
    nums = [3,1,4,1,5,9,2]
    num = nums[1:5]
    print(num)

    num = nums.copy()
    num[0] = 100
    print(num)
    print(nums)

    evens = []
    for i in nums :
        if i % 2 == 0:
            evens.append(i)

    print(evens)

def num_calc2():    
    class_a = {"Tom","Mary","Ali"}
    class_b = {"Ali","Wei","Mary"}

    print(class_a.intersection(class_b))
    print(class_a.union(class_b))
    print(class_b.difference(class_a))
    print(class_a.difference(class_b))

    inventory = {"pen": 10, "book": 5}
    print(inventory.get("eraser",0))

    for i,j in inventory.items():
        print(f"{i} is RM{j}")

def num_calc3():
    for i in range(1,31) :
        if i % 3 == 0:
            continue
        print(i)       

    lista = [7,2,9,4,11,6]
    i = 0
    target = 11
    while i < len(lista):
        if lista[i] == target: 
            print(i)
            break
        else :
            print(f"index{i} Not Found")    
        i += 1
    
def num_calc4() :
    matrix = [[1,2,3],[4,5,6],[7,8,9]]    
    x = 0

    for i in matrix:
        for j in i :
            x += j
            print(j)

    print(x)

def num_calc5() :
    def find_max(numbers):
        if not numbers :
            return None
    
        max_val = numbers[0]

        for i in numbers:
            if i > max_val:
                max_val = i

        return max_val        

    b = find_max([1,3,2,1])
    print(b)

    def count_vowels(word):
        we = 0
        for i in word:
            if i in "aeiou":
                we += 1
        return we        

    wo = count_vowels("weird")
    print(wo)

    def filter_events(nums):
        we = []
        for i in nums:
            if i % 2 == 0:
                we.append(i)

        return we        

    wa = filter_events([1,2,3,4,5,6])
    print(wa)

def num_calc6() :
    pass


def borrow_book(books,title) :
    if title in books and books[title] > 0 :
        book[title] -= 1
        return True
    else :
        return False

book = {"Python101": 3,"JavaBasics": 0,"WebDev": 5}
we = borrow_book(book,"Python101")
print(we)