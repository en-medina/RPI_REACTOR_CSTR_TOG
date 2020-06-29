from collections import deque

a = deque(maxlen = 4)
for i in range(10):
	a.appendleft(i)

print(a.pop())
print(a)

print(len(a))