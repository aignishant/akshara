# `make` is not used in this project; ./m is the driver (plan §25.9, Day 0).
# This shim exists only so that muscle memory and `make check` still work.
check:
	@bash ./m check
