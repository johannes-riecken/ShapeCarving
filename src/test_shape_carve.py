import unittest
from greedy import *
from shape_carve import *

# views has bhwc format. For simplicity we only allow square faces. For now we assume one color channel that can be 0
# (black) or 1 (white)
# case 0: 1x1x1 cube, all white
views = [
        [[[1]]],  # left
        [[[1]]],  # back
        [[[1]]],  # bottom
        [[[1]]],  # right
        [[[1]]],  # front
        [[[1]]],  # top
        ]

# case 1: 2x2x2 cube. Top half is red, bottom half is blue.
# colors given in comments are from my Rubik's cube.
# the turning in rubik notation is:
# u', f, u', f, u'
views = [
    [
        [[1, 0, 0], [1, 0, 0]],
        [[0, 0, 1], [0, 0, 1]],
    ], # left, blue
    [
        [[1, 0, 0], [1, 0, 0]],
        [[0, 0, 1], [0, 0, 1]],
    ], # back, red
    [
        [[0, 0, 1], [0, 0, 1]],
        [[0, 0, 1], [0, 0, 1]],
    ], # bottom, yellow
    [
        [[1, 0, 0], [0, 0, 1]],
        [[1, 0, 0], [0, 0, 1]],
    ], # right, green
    [
        [[1, 0, 0], [0, 0, 1]],
        [[1, 0, 0], [0, 0, 1]],
    ], # front, orange
    [
        [[1, 0, 0], [1, 0, 0]],
        [[1, 0, 0], [1, 0, 0]],
    ], # top, white
    ]

# case 2: 3x3x3 cube of a 3x1x3 frame in the back.
views = [
    [
        [[1], [0], [0]],
        [[1], [0], [0]],
        [[1], [0], [0]],
    ], # left, blue
    [
        [[1], [1], [1]],
        [[1], [0], [1]],
        [[1], [1], [1]],
    ], # back, red
    [
        [[1], [1], [1]],
        [[0], [0], [0]],
        [[0], [0], [0]],
    ], # bottom, yellow
    [
        [[1], [1], [1]],
        [[0], [0], [0]],
        [[0], [0], [0]],
    ], # right, green
    [
        [[1], [1], [1]],
        [[1], [0], [1]],
        [[1], [1], [1]],
    ], # front, orange
    [
        [[1], [0], [0]],
        [[1], [0], [0]],
        [[1], [0], [0]],
    ], # top, white
    ]

# case 3, 3x3x3 cube of a 3d plus with the Rubik cube's colors, where each color
# wins over the two colors following it (blue > red, blue > yellow, etc.)
# yellow: [1, 1, 0]
# instead of orange we'll use magenta: [1, 0, 1]
# color ring: brygowb
views = [
    [
        [[0, 0, 0], [1, 1, 1], [0, 0, 0]],
        [[0, 0, 1], [0, 0, 0], [1, 0, 1]],
        [[0, 0, 0], [0, 0, 1], [0, 0, 0]],
    ], # left, blue
    [
        [[0, 0, 0], [1, 1, 1], [0, 0, 0]],
        [[1, 0, 0], [0, 0, 0], [0, 0, 1]],
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
    ], # back, red
    [
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[1, 1, 0], [0, 0, 0], [0, 0, 1]],
        [[0, 0, 0], [1, 1, 0], [0, 0, 0]],
    ], # bottom, yellow
    [
        [[0, 0, 0], [1, 0, 0], [0, 0, 0]],
        [[0, 1, 0], [0, 0, 0], [1, 1, 0]],
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
    ], # right, green
    [
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[1, 0, 1], [0, 0, 0], [1, 1, 0]],
        [[0, 0, 0], [1, 0, 1], [0, 0, 0]],
    ], # front, orange
    [
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
        [[1, 1, 1], [0, 0, 0], [1, 0, 1]],
        [[0, 0, 0], [1, 1, 1], [0, 0, 0]],
    ], # top, white
    ]


# class TestMeshFunctions(unittest.TestCase):
#     def test_GreedyMesh(self):
#         volume = [1, 2, 3, 4, 5]
#         dims = [1, 2, 2]
#         result = GreedyMesh(volume, dims)
#         self.assertIsInstance(result, dict)
#         self.assertIn('vertices', result)
#         self.assertIn('faces', result)

#     def test_ShapeCarve(self):
#         dims = [1, 2, 2]
#         views = [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]
#         mask_color = 1
#         skip = [False, False]
#         result = ShapeCarve(dims, views, mask_color, skip)
#         self.assertIsInstance(result, dict)
#         self.assertIn('volume', result)
#         self.assertIn('dims', result)
#         self.assertEqual(result['dims'], dims)

# if __name__ == '__main__':
#     unittest.main()

# Prepare dummy data for GreedyMesh
volume = [1, 2, 3, 4, 5]
dims = [1, 2, 2]

# Run GreedyMesh
result_greedy = GreedyMesh(volume, dims)

# Check the types and keys of the returned object from GreedyMesh
assert isinstance(result_greedy, dict), "The result should be a dictionary."
assert 'vertices' in result_greedy, "The key 'vertices' should be in the result."
assert 'faces' in result_greedy, "The key 'faces' should be in the result."

# Prepare dummy data for ShapeCarve
dims = [1, 2, 2]
views = [[1, 2, 3, 4, 5], [1, 2, 3, 4, 5]]
mask_color = 1
skip = [False, False]

# Run ShapeCarve
# result_shape = ShapeCarve(dims, views, mask_color, skip)

# Check the types and keys of the returned object from ShapeCarve
# assert isinstance(result_shape, dict), "The result should be a dictionary."
# assert 'volume' in result_shape, "The key 'volume' should be in the result."
# assert 'dims' in result_shape, "The key 'dims' should be in the result."
# assert result_shape['dims'] == dims, "The 'dims' value should be equal to the input 'dims'."

