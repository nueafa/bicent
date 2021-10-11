num = []
while len(num) != 10 :
    num.append(int(input(": ")))

def sortn(x):
    x.sort()
    return x

print(sortn(num)[0],sortn(num)[-1])
