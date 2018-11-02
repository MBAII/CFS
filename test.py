import math
import copy


dic = {"liu":1, "bai": 2, "ma": 3, "zeng":4}
dic["zeng"] = 5
for k in dic:
    print dic[k]


print dic.keys()
print dic.values()

f = open("data.txt", "w")
f.writelines(["123\n","123\n","123\n","123\n","123\n","123"])
f.close()



