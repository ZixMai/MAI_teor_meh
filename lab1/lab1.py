"""Lab work 1"""
import sympy as sp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from math import hypot
from drawing_head import DrawingHead

t = sp.Symbol('t')

R = 2 + sp.sin(8 * t)
phi = t + 0.2 * sp.cos(6 * t)

drawing_head = DrawingHead(R, phi, t, time_range_limit=20)

velocity_arrow = drawing_head.velocity_arrow
velocity_arrow_head_coords = velocity_arrow.get_rotated_arrow_head_coords(0)
velocity_arrow_coords_x0 = velocity_arrow.x_0_values
velocity_arrow_coords_y0 = velocity_arrow.y_0_values
velocity_arrow_coords_x = velocity_arrow.x_values
velocity_arrow_coords_y = velocity_arrow.y_values

acceleration_arrow = drawing_head.acceleration_arrow
acceleration_arrow_head_coords = acceleration_arrow.get_rotated_arrow_head_coords(0)
acceleration_arrow_coords_x0 = acceleration_arrow.x_0_values
acceleration_arrow_coords_y0 = acceleration_arrow.y_0_values
acceleration_arrow_coords_x = acceleration_arrow.x_values
acceleration_arrow_coords_y = acceleration_arrow.y_values

radius_arrow = drawing_head.radius_arrow
radius_arrow_head_coords = radius_arrow.get_rotated_arrow_head_coords(0)
radius_arrow_coords_x0 = radius_arrow.x_0_values
radius_arrow_coords_y0 = radius_arrow.y_0_values
radius_arrow_coords_x = radius_arrow.x_values
radius_arrow_coords_y = radius_arrow.y_values

curvature_arrow = drawing_head.curvature_arrow
curvature_arrow_coords_x0 = curvature_arrow.x_0_values
curvature_arrow_coords_y0 = curvature_arrow.y_0_values
curvature_arrow_coords_x = curvature_arrow.x_values
curvature_arrow_coords_y = curvature_arrow.y_values

ui = plt.figure()
ui.canvas.manager.set_window_title("Жуховицкий А. Д. М8О-203Б-23 Вариант 8 ЛР 1")
ui_plot = ui.add_subplot(1, 1, 1)
ui_plot.axis("equal")
ui_plot.set(xlim=[-11, 11], ylim=[-15, 15])
ui_plot.plot(drawing_head.x_values, drawing_head.y_values)

velocity_vector, = ui_plot.plot(
    [velocity_arrow_coords_x0[0], velocity_arrow_coords_x[0]],
    [velocity_arrow_coords_y0[0], velocity_arrow_coords_y[0]],
    "m",
    label="Скорость"
)
velocity_vector_head, = ui_plot.plot(velocity_arrow_head_coords[0], velocity_arrow_head_coords[1], "m")

acceleration_vector, = ui_plot.plot(
    [acceleration_arrow_coords_x0[0], acceleration_arrow_coords_x[0]],
    [acceleration_arrow_coords_y0[0], acceleration_arrow_coords_y[0]],
    "g",
    label="Ускорение"
)
acceleration_vector_head, = ui_plot.plot(acceleration_arrow_head_coords[0], acceleration_arrow_head_coords[1], "g")

curvature_vector, = ui_plot.plot(
    [curvature_arrow_coords_x0[0], curvature_arrow_coords_x[0]],
    [curvature_arrow_coords_y0[0], curvature_arrow_coords_y[0]],
    "black",
    label='Радиус кривизны',
    linestyle='--'
)

drawer_head, = ui_plot.plot(drawing_head.x_values[0], drawing_head.y_values[0], color="black", marker="o")

radius_vector, = ui_plot.plot(
    [radius_arrow_coords_x0[0], radius_arrow_coords_x[0]],
    [radius_arrow_coords_y0[0], radius_arrow_coords_y[0]],
    "c",
    label="Радиус-вектор"
)
radius_vector_head, = ui_plot.plot(radius_arrow_head_coords[0], radius_arrow_head_coords[1], "c")

raw_text = "X = {:.5f}, Y = {:.5f}, V = {:.5f}, W = {:.5f}, Curvature = {:.5f}"
text = ui_plot.text(
    0.03,
    0.03,
    raw_text.format(
        drawing_head.x_values[0],
        drawing_head.y_values[0],
        hypot(velocity_arrow.v_x_values[0], velocity_arrow.v_y_values[0]),
        hypot(acceleration_arrow.v_x_values[0], acceleration_arrow.v_y_values[0]),
        hypot(curvature_arrow.v_x_values[0], curvature_arrow.v_y_values[0])
    ),
    transform=ui_plot.transAxes,
    fontsize=8
)


def animate_plot(frame_number):
    """Function that animates plot

    :param frame_number: Plot frame to update
    """
    drawer_head.set_data([drawing_head.x_values[frame_number]], [drawing_head.y_values[frame_number]])

    velocity_vector.set_data(
        [velocity_arrow_coords_x0[frame_number], velocity_arrow_coords_x[frame_number]],
        [velocity_arrow_coords_y0[frame_number], velocity_arrow_coords_y[frame_number]]
    )
    velocity_arrow_head_coords = velocity_arrow.get_rotated_arrow_head_coords(frame_number)
    velocity_vector_head.set_data(velocity_arrow_head_coords)

    acceleration_vector.set_data(
        [acceleration_arrow_coords_x0[frame_number], acceleration_arrow_coords_x[frame_number]],
        [acceleration_arrow_coords_y0[frame_number], acceleration_arrow_coords_y[frame_number]]
    )
    acceleration_arrow_head_coords = acceleration_arrow.get_rotated_arrow_head_coords(frame_number)
    acceleration_vector_head.set_data(acceleration_arrow_head_coords)

    radius_vector.set_data(
        [radius_arrow_coords_x0[frame_number], radius_arrow_coords_x[frame_number]],
        [radius_arrow_coords_y0[frame_number], radius_arrow_coords_y[frame_number]]
    )
    radius_arrow_head_coords = radius_arrow.get_rotated_arrow_head_coords(frame_number)
    radius_vector_head.set_data(radius_arrow_head_coords)

    curvature_vector.set_data(
        [curvature_arrow_coords_x0[frame_number], curvature_arrow_coords_x[frame_number]],
        [curvature_arrow_coords_y0[frame_number], curvature_arrow_coords_y[frame_number]]
    )

    text.set_text(
        raw_text.format(
            drawing_head.x_values[frame_number],
            drawing_head.y_values[frame_number],
            hypot(velocity_arrow.v_x_values[frame_number], velocity_arrow.v_y_values[frame_number]),
            hypot(acceleration_arrow.v_x_values[frame_number], acceleration_arrow.v_y_values[frame_number]),
            hypot(curvature_arrow.v_x_values[frame_number], curvature_arrow.v_y_values[frame_number])
        )
    )

    return (
        drawer_head,
        velocity_vector,
        velocity_vector_head,
        acceleration_vector,
        acceleration_vector_head,
        radius_vector,
        radius_vector_head,
        curvature_vector
    )


animation = FuncAnimation(
    ui,
    animate_plot,
    frames=drawing_head.time_range_limit * 100,
    interval=drawing_head.time_range_limit * 2
)

ui_plot.legend(fontsize=7)
plt.show()