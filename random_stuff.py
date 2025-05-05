# print(
# 	(
# 		multinomialkoeffizient(28, 9, 9, 9, 1) * multinomialkoeffizient(4, 1, 1, 1, 1)
# 		+
# 		multinomialkoeffizient(28, 8, 9, 9, 2) * multinomialkoeffizient(4, 2, 1, 1, 0) * 3
# 	) / multinomialkoeffizient(32, 10, 10, 10, 2)
# )
from itertools import product, repeat

c = 0
counter = 0
all_ = 0
arr = [1, 2, 3]
n = len(arr)
for x in product(*(repeat(arr, n))):
	all_ += 1
	# if x[0] != 1:
	# 	c += 1
	if x[0] != 1:
		counter += 1
		if x[1] == 2:
			c += 1
	# print(x)

print("C : 1XXXX", c, c / all_)
print("CO: 12XXX", counter, counter / all_)
print("diff", c / counter)
print("all", all_)

print((pow(n, n - 1) - pow(n, n - 2)) / (pow(n, n - 1) * (n - 1)))
print((n - 1) / (n * (n - 1)))
