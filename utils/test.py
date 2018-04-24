import math

# 非递归
def jinz2(key,val):
    arr = []
    while val/key != 0:
        arr.append(val%key )
        val = math.floor(val/key)
    arr = list(reversed(arr))
    if arr[0] == 0:
        arr.pop(0)
    arr = "".join(map(lambda x: str(x), arr))
    return arr
# 递归
def jinz(key,val,arr=None):
    # 这里不能在参赛就arr = [] 原因是在调用销毁不了
    if arr is None:
        arr = [];
    if val == 0:
        arr = list(reversed(arr))
        if arr[0] == 0:
            arr.pop(0)
        arr = "".join(map(lambda x:str(x),arr))
        return arr
    res1 = val%key
    res2 = math.floor(val/key)
    arr.append(res1)
    # 这里一定记得返回 我开始忘记加这个代码调入递归陷阱，每次递归开辟一个栈。如果这里没返回
    # 函数在倒数第二次才有结果后面的，在释放栈以后就没有返回了
    return jinz(key,res2,arr)

