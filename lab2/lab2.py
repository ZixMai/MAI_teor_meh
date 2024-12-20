"""Lab work 2"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import use as fix_ui
import numpy as np

fix_ui('TkAgg')

def rotate_2d(x, y, alpha):
    """Поворот в двухмерном пространстве"""
    return x * np.cos(alpha) - y * np.sin(alpha), x * np.sin(alpha) + y * np.cos(alpha)

# Задаём начальные параметры
L = 1
R = 0.5
phi = np.linspace(0, 2 * np.pi, 1000)
Nv = 2

# Задаём все параметры для спиральной пружины
spring_r0 = 0.05
spring_r = 0.2
psi = np.linspace(0, np.pi * 2 * Nv, 1000)
x_spiral_spring = -(spring_r0 + psi * (spring_r - spring_r0) / psi[-1]) * np.sin(psi)
y_spiral_spring = (spring_r0 + psi * (spring_r - spring_r0) / psi[-1]) * np.cos(psi)

# Определяем все параметры для диска
x_disk = R * np.cos(phi)
y_disk = R * np.sin(phi)
y_disk_middle = -L
x_disk_middle = 0

# Создание плота и добавление на него начального состояние системы
ui = plt.figure()
ui.canvas.manager.set_window_title("Жуховицкий А. Д. М8О-203Б-23 Вариант 9 ЛР 2")
ui_plot = ui.add_subplot(1, 1, 1)
ui_plot.axis("equal")
ui_plot.set(xlim=[-11, 11], ylim=[-15, 15])

# Рисуем оси и диск
ui_plot.axhline(0, color='black', linewidth=1)  # Горизонтальная ось
ui_plot.axvline(0, color='black', linewidth=1)  # Вертикальная ось
disk, = ui_plot.plot(x_disk + x_disk_middle, y_disk + y_disk_middle, color='black')

# Рисуем стержень и радиус к материальной точке
rod_oc, = ui_plot.plot([x_disk_middle, x_disk_middle], [y_disk_middle, 0], color='black', linestyle='--', linewidth=3)
rod_ca, = ui_plot.plot([x_disk_middle, x_disk_middle], [y_disk_middle, y_disk_middle + R], color='blue')

# Рисуем материальную точку
point_a, = ui_plot.plot(x_disk_middle, y_disk_middle + R, color="red", marker="o")

# Рисуем пружину
spiral_spring, = ui_plot.plot(
    x_spiral_spring + x_disk_middle,
    y_spiral_spring + y_disk_middle,
    color="green"
)

def animate_plot(frame_number):
    """Функция отвечающая за анимацию плота.

    :param frame_number: Кадр.
    """
    x_disk_middle_rotated, y_disk_middle_rotated = rotate_2d(x_disk_middle, y_disk_middle, phi[frame_number])
    disk.set_data([x_disk + x_disk_middle_rotated], [y_disk + y_disk_middle_rotated])
    rod_oc.set_data([x_disk_middle, x_disk_middle_rotated], [0, y_disk_middle_rotated])
    ca_rotated_x, ca_rotated_y = rotate_2d(0, R, -psi[frame_number])
    rod_ca.set_data([x_disk_middle_rotated, ca_rotated_x + x_disk_middle_rotated], [y_disk_middle_rotated, ca_rotated_y + y_disk_middle_rotated])
    point_a.set_data([ca_rotated_x + x_disk_middle_rotated], [ca_rotated_y + y_disk_middle_rotated])
    x_spiral_spring_rotated, y_spiral_spring_rotated = rotate_2d(x_spiral_spring, y_spiral_spring, -psi[frame_number])
    spiral_spring.set_data(
        x_spiral_spring_rotated + x_disk_middle_rotated,
        y_spiral_spring_rotated + y_disk_middle_rotated
    )

    return (
        disk,
        rod_oc,
        rod_ca,
        point_a,
        spiral_spring,
    )

time_range = np.linspace(0, 10, 100 * 10)

# Воспроизведение анимации и показ плота
animation = FuncAnimation(
    ui,
    animate_plot,
    frames=1000,
    interval=1/60
)

plt.show()