import collections

l = collections.deque(maxlen=5)
l.append('apple')
l.append('orange')
l.append('grape')
l.append('banana')
l.append('mango')
print(l)
l.append('kiwi')
print(l)
print l.count('kiwi')

print 90.0/365
