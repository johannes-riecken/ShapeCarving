import numpy as np


def generate_directions() -> np.ndarray[int, 3]:
    ret = np.array([1, 0, 0])
    while True:
        yield ret
        ret = -np.roll(ret, 1)


it = generate_directions()
print([list(next(it)) for _ in range(6)])

# equivalent to this order:
# left
# back
# bottom
# right
# front
# top
