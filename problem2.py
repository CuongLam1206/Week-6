def count_char(st):
    dic = {} 
    for char in st:   
        if char.isalpha():   
            if char in dic:
                dic[char] += 1
            else:
                dic[char] = 1
    return dic

in_st = input("Nhập vào một từ: ")
ans = count_char(in_st)
print(ans)
