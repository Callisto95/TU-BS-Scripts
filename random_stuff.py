from tu_bs_scripts.stochastik import multinomialkoeffizient

print(
	(
		multinomialkoeffizient(28, 9, 9, 9, 1) * multinomialkoeffizient(4, 1, 1, 1, 1)
		+
		multinomialkoeffizient(28, 8, 9, 9, 2) * multinomialkoeffizient(4, 2, 1, 1, 0) * 3
	) / multinomialkoeffizient(32, 10, 10, 10, 2)
)
