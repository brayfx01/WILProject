class MyObject:
    def __init__(self, value):
        self.value = value
        
obj1 = MyObject(100)

l1 = [obj1]
l2  = []
print(l1[0].value)

obj1.value = 0
    

print(l2[0].value)

l2[0].value = l2[0].value - 50


print(l1[0].value)

print(l2[0].value)