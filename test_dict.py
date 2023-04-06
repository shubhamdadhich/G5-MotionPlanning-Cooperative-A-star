
d = {(3,4,1): 10, "key2": 23}

print(d)

if (3,4,1) in d:
    print("this will execute")

if "nonexistent key" in d:
    print("this will not")


