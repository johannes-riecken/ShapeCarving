# This shape carver works and I assume it behaves like the first step in the
# Java shape carver
import numpy as np

class ShapeCarver:
    def __init__(self, projections):
        # Projections should be a dictionary with keys "front", "side", "top" and numpy arrays as values.
        self.projections = projections
        self.shape = projections["front"].shape + (projections["side"].shape[1],)
        self.model = np.ones(self.shape, dtype=np.int32)
        self.carve()

    def carve(self):
        # Carve along each axis using the provided projections.
        for i in range(self.shape[0]):
            self.model[i, :, :] &= self.projections["front"]
        for j in range(self.shape[1]):
            self.model[:, j, :] &= self.projections["side"]
        for k in range(self.shape[2]):
            self.model[:, :, k] &= self.projections["top"]

    def get_model(self):
        return self.model

def test_shape_carver():
    # Define projections for a 3D plus sign.
    front_projection = np.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 1, 0]
    ])
    side_projection = front_projection
    top_projection = front_projection

    # Create a ShapeCarver object using the projections.
    projections = {
        "front": front_projection,
        "side": side_projection,
        "top": top_projection
    }
    carver = ShapeCarver(projections)

    # Get the carved 3D model.
    model = carver.get_model()

    # Define the expected voxel model for a 3D plus sign.
    # The expected_model is a 3D numpy array where:
    # - The first dimension represents the depth (along the front-to-back axis).
    # - The second dimension represents the height (along the bottom-to-top axis).
    # - The third dimension represents the width (along the left-to-right axis).
    # A value of 1 in expected_model[0][1][2] means that the voxel at depth 0, height 1, and width 2 is present (opaque).
    expected_model = np.array([
        [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ],
        [
            [0, 1, 0],
            [1, 1, 1],
            [0, 1, 0]
        ],
        [
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ]
    ])

    # Assert that the carved model matches the expected 3D plus sign.
    if not np.array_equal(model, expected_model):
        diff = model - expected_model
        raise AssertionError(f"The carved model does not match the expected 3D plus sign.\nDifference:\n{diff}")

# Run the test
test_shape_carver()
