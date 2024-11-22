def de_str(coded_str):
    stack = []  
    st = "" 
    num = 0  
    for char in coded_str:
        if char.isdigit():
            num = int(char)
        elif char == '[':
            stack.append((st, num))
            st = ""  
            num = 0  
        elif char == ']':
            s, num = stack.pop()
            st = s + st * num
        else:
            st += char
    return st

coded_str = input("Nhập chuỗi mã hóa : ")
ans = de_str(coded_str)
print(f"Chuỗi giải mã là : {ans}")
