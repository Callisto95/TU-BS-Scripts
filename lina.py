from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Matrix:
	a11: int
	a12: int
	a21: int
	a22: int
	
	def __add__(self, other) -> Matrix:
		if not isinstance(other, Matrix):
			return NotImplemented
		return Matrix(self.a11 + other.a11, self.a12 + other.a12, self.a21 + other.a21, self.a22 + other.a22)
	
	def __mul__(self, other):
		if not isinstance(other, Matrix):
			return NotImplemented
		return Matrix(
			self.a11 * other.a11 + self.a12 * other.a21,
			self.a11 * other.a12 + self.a12 * other.a22,
			self.a21 * other.a11 + self.a22 * other.a21,
			self.a21 * other.a21 + self.a22 * other.a22
		)
	
	def __str__(self):
		return f"[{self.a11:2d}|{self.a12:2d}]\n[{self.a21:2d}|{self.a22:2d}]"


def det(m: Matrix):
	return (m.a11 * m.a22) - (m.a12 * m.a21)


ma = Matrix(1, 2, 3, 4)
mb = Matrix(3, 5, 7, 9)

print(ma + mb)
print()
print(ma * mb)
print(det(ma))
print(det(mb))

print("-" * 20)

print(det(ma) + det(mb))
print(det(ma + mb))

print("-" * 20)

print(det(ma) * det(mb))
print(det(ma * mb))
