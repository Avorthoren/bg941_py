from numbers import Number
import random
from typing import MutableSequence

import utils


A_T = MutableSequence[Number]


def sort_two(array: A_T, i: int, j: int) -> None:
	if array[i] > array[j]:
		array[i], array[j] = array[j], array[i]


def pre_sort(array: A_T, step: int, p: bool = False) -> None:
	assert step >= 0
	if p:
		print(f"pre_sort: {step}")
	width = 1 << step
	n = len(array)
	for i in range(0, n, width << 1):
		for d in range(width):
			j = i + width - d - 1
			k = i + width + d
			if k >= n:
				break
			if p:
				print(j, k)
			sort_two(array, j, k)


def part_sort(array: A_T, width_pow: int, p: bool = False) -> None:
	assert width_pow >= 0
	if p:
		print(f"part_sort: {width_pow}")
	width = 1 << width_pow
	n = len(array)
	for i in range(0, n, width << 1):
		for d in range(width):
			j = i + d
			k = j + width
			if k >= n:
				break
			if p:
				print(j, k)
			sort_two(array, j, k)


def check_piece_bitonic(array: A_T, width_pow: int) -> None:
	width = 1 << width_pow
	for i in range(0, len(array), width):
		j = min(i + width, len(array))
		utils.check_bitonic(array, i, j)


def bitonic_sort_step(array: A_T, step: int, p: bool = False) -> None:
	pre_sort(array, step, p)
	if p:
		print(array)
	for width_pow in reversed(range(step)):
		# try:
		# 	check_piece_bitonic(array, width_pow + 1)
		# except utils.IsNotBitonicError:
		# 	# Placeholder for prints
		# 	raise
		part_sort(array, width_pow, p)
		if p:
			print(array)


def bitonic_sort(array: A_T, p: bool = False) -> None:
	if p:
		print(array)
	n = len(array)
	if n < 2:
		return

	for step in range((n - 1).bit_length()):
		if p:
			print(f"STEP {step}:")
		bitonic_sort_step(array, step, p)
		if p:
			print()


def test(array: A_T) -> None:
	array_copy = list(array)
	bitonic_sort(array_copy)
	for i in range(len(array_copy) - 1):
		if array_copy[i+1] < array_copy[i]:
			print("INITIAL:")
			print(array)
			print("AFTER_SORT:")
			print(array_copy)
			raise RuntimeError(f"array[{i+1}] < array[{i}]")


def test_random() -> None:
	n = random.randint(0, 50)
	array = [random.randint(0, n) for _ in range(n)]
	test(array)


def count_days(n: int) -> int:
	max_step = (n - 1).bit_length()
	return (max_step * max_step + max_step) >> 1


def main():
	random.seed(42)
	for _ in range(10000):
		test_random()

	# n = 32
	# # random.seed(41)
	# array = [i for i in range(n)]
	# random.shuffle(array)
	# # array = list(reversed(range(n)))
	# bitonic_sort(array, p=True)


if __name__ == "__main__":
	main()
