import itertools
from numbers import Number
from typing import Iterable, MutableSequence


A_T = MutableSequence[Number]
P_T = list[int]


def bitonic_permutations(n: int) -> Iterable[P_T]:
	for p in itertools.permutations(range(n)):
		try:
			check_bitonic(p, 0, len(p))
		except IsNotBitonicError:
			continue
		else:
			yield list(p)


def sort_two(array: A_T, i: int, j: int) -> None:
	if array[j] < array[i]:
		array[i], array[j] = array[j], array[i]


def sort_part(array: A_T) -> None:
	step = len(array) >> 1
	for i in range(step):
		sort_two(array, i, i + step)


def diff_sign(a: Number, b: Number):
	if a == b:
		return 0
	elif a < b:
		return 1
	else:
		return -1


class IsNotBitonicError(Exception):
	pass


def check_bitonic_wrong(array: A_T, i: int, j: int) -> None:
	if j - i <= 3:
		return

	cnt = 0
	last_s = 0
	for k in range(i, j-1):
		s = diff_sign(array[k], array[k + 1])
		if s == 0:
			continue
		if s != last_s:
			last_s = s
			cnt += 1
			if cnt > 2:
				raise IsNotBitonicError


def check_bitonic(array: A_T, left: int, right: int) -> None:
	"""Check if array[left:right] is bitonic.
	There should be descending sequence to the right of the max element
	(cyclically) and ascending sequence to the left (cyclically). For example:
	1 0 1 2 3 4 5 4 3 2
	            5 4 3 2 ... 1 0 - right descending sequence
	    1 2 3 4 5               - left ascending sequence
	"""
	n = right - left
	if n <= 3:
		# Every short sequence is bitonic.
		return

	# find max element.
	max_i = left
	max_v = array[max_i]
	for i in range(left + 1, right):
		v = array[i]
		if v > max_v:
			max_i, max_v = i, v

	# Find the longest descending cyclic sequence to the right of the max_i.
	i = left if max_i + 1 == right else max_i + 1
	while i != max_i:
		next_i = left if i + 1 == right else i + 1
		if array[i] < array[next_i]:
			break
		i = next_i

	# Ensure, that array[next_i : max_i] is cyclic ascending sequence.
	# There at least 1 iteration above (n > 3), so next_i will be defined.
	i = next_i
	while i != max_i:
		next_i = left if i + 1 == right else i + 1
		if array[i] > array[next_i]:
			raise IsNotBitonicError(f"array[{left}:{right}] is not bitonic: {array[left:right]}")
		i = next_i


def check(array: P_T) -> None:
	n = len(array)
	step = n >> 1
	lower_max = max(array[i] for i in range(step))
	higher_min = min(array[i] for i in range(step, n))
	if lower_max > higher_min:
		raise ValueError(f"{lower_max} > {higher_min}")

	check_bitonic(array, 0, step)
	check_bitonic(array, step, n)


def test(n: int = 10) -> None:
	for i, p in enumerate(bitonic_permutations(n)):
		check_bitonic(p, 0, len(p))
		sort_part(p)
		try:
			check(p)
		except (ValueError, IsNotBitonicError):
			print(i)
			print(p)
			raise


def main():
	test()


if __name__ == "__main__":
	main()
