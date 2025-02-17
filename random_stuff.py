MAX_RANGE = 100000

for x in range(-MAX_RANGE, MAX_RANGE):
	for y in range(-MAX_RANGE, MAX_RANGE):
		if 1 == 2000 * x + 122 * y:
			print(x, y)
			exit()
	