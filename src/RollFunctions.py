import random

def d(die,num = 1):
    num = int(num)
    ans = 0
    for i in range(num):
        ans += random.randint(1,die)
    return ans
