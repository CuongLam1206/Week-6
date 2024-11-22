def gt(n):
    res = 1
    for i in range(1, n + 1):
        res *= i
    return res

def exp_y(x, y):
    res = 1 
    
    for i in range(1, y+1):
        res += (x ** i) / gt(i) 
    
    return res

x = float(input("Nhập giá trị x: "))
y = int(input("Nhập số lượng phần tử n: "))

ans = exp_y(x, y)
print(f"Giá trị xấp xỉ của e^{x} là: {ans}")
