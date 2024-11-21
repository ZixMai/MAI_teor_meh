from math import atan2
import numpy as np


class Arrow:
    def __init__(self, x_0, y_0, x, y, arrow_length_coefficient=0.5, arrow_size_coefficient=2.5):
        self.arrow_length_coefficient = arrow_length_coefficient
        self.arrow_size_coefficient = arrow_size_coefficient
        self.x_0_values = x_0
        self.y_0_values = y_0
        self.x_values = x_0 + x * self.arrow_length_coefficient
        self.y_values = y_0 + y * self.arrow_length_coefficient
        self.v_x_values = x
        self.v_y_values = y
        self.arrow_head_x_row = np.array([-0.2 * self.arrow_size_coefficient, 0, -0.2 * self.arrow_size_coefficient])
        self.arrow_head_y_row = np.array([0.1 * self.arrow_size_coefficient, 0, -0.1 * self.arrow_size_coefficient])

    def rotate_arrow_head(self, alpha):
        return (
            self.arrow_head_x_row * np.cos(alpha) - self.arrow_head_y_row * np.sin(alpha),
            self.arrow_head_x_row * np.sin(alpha) + self.arrow_head_y_row * np.cos(alpha)
        )

    def get_rotated_arrow_head_coords(self, frame_number):
        new_head_x_coords, new_head_y_coords = (
            self.rotate_arrow_head(
                atan2(
                    self.v_y_values[frame_number],
                    self.v_x_values[frame_number]
                )
            )
        )

        return (
            new_head_x_coords + self.x_values[frame_number],
            new_head_y_coords + self.y_values[frame_number]
        )