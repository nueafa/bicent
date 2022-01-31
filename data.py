import math
r = []
for i in range(-1500,1500):
    for j in range(-1500,1500):
        if pow(i,2)*j == 16:
            r.append(i)

print(min(r))
