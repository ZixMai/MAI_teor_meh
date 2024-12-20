"""Lab work 3"""
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import use as fix_ui
import numpy as np
from scipy.integrate import odeint

# Начальные параметры
fix_ui('TkAgg')
available_time = 20
g = 9.81
m1 = 2
m2 = 3
m3 = 1
L = 1
R = 0.5
c = 10
phi_0, psi_0, d_phi_0, d_psi_0 = 0, 0, 0.5, -0.5
Nv = 3
time_range = np.linspace(0, available_time, 100 * available_time)


def rotate_2d(x, y, alpha):
    """Поворот в двухмерном пространстве"""
    return x * np.cos(alpha) - y * np.sin(alpha), x * np.sin(alpha) + y * np.cos(alpha)


def odesys(y, t):
    """Функция для численного решения системы ДУ"""
    a11 = (m1 / 3 + m2 + m3) * L
    a12 = m3 * R * np.cos(y[0] + y[1])
    a21 = m3 * L * np.cos(y[0] + y[1])
    a22 = (m2 / 2 + m3) * R

    b1 = (y[3] ** 2) * m3 * R * np.sin(y[0] + y[1]) - (m1 / 2 + m2 + m3) * g * np.sin(y[0]) - c / L * (y[0] + y[1])
    b2 = (y[2] ** 2) * m3 * L * np.sin(y[0] + y[1]) - m3 * g * np.sin(y[1]) - c / R * (y[0] + y[1])

    dy = np.zeros(4)
    dy[0] = y[2]
    dy[1] = y[3]
    dy[2] = (b1 * a22 - b2 * a12) / (a11 * a22 - a12 * a21)
    dy[3] = (b2 * a11 - b1 * a21) / (a11 * a22 - a12 * a21)

    return dy


# Численное решение системы ДУ
equation_start_values = [phi_0, psi_0, d_phi_0, d_psi_0]
equation_values = odeint(odesys, equation_start_values, time_range)

# Получение значений
phi = np.array(equation_values[:, 0])
psi = np.array(equation_values[:, 1])
d_phi = np.array(equation_values[:, 2])
d_psi = np.array(equation_values[:, 3])
d_d_phi = np.array([odesys(y, t)[2] for y, t in zip(equation_values, time_range)])
d_d_psi = np.array([odesys(y, t)[3] for y, t in zip(equation_values, time_range)])

# Вычисление реакции шарнира
R_x = (
        - (m1 / 2 + m2 + m3) * L * (d_d_phi * np.sin(phi) + (d_phi ** 2) * np.cos(phi))
        + m3 * R * (d_d_psi * np.sin(psi) + (d_psi ** 2) * np.cos(psi)) + (m1 + m2 + m3) * g
)
R_y = (
    (m1 / 2 + m2 + m3) * L * (d_d_phi * np.cos(phi) - (d_phi ** 2) * np.sin(phi))
    + m3 * R * (d_d_psi * np.cos(psi) - (d_psi ** 2) * np.sin(psi))
)

# Задаём все параметры для спиральной пружины
spring_r0 = 0.005
spring_r = 0.15
circle_angle = np.linspace(0, np.pi * 2 * Nv, available_time * 100)
x_spiral_spring = -(spring_r0 + circle_angle * (spring_r - spring_r0) / circle_angle[-1]) * np.sin(circle_angle)
y_spiral_spring = (spring_r0 + circle_angle * (spring_r - spring_r0) / circle_angle[-1]) * np.cos(circle_angle)

# Определяем все параметры для диска
x_disk = R * np.cos(circle_angle)
y_disk = R * np.sin(circle_angle)
y_disk_middle = -L
x_disk_middle = 0

# Создание плота и добавление на него начального состояние системы
ui = plt.figure()
ui.canvas.manager.set_window_title("Жуховицкий А. Д. М8О-203Б-23 Вариант 9 ЛР 3")
ui_plot = ui.add_subplot(1, 1, 1)
ui_plot.axis("equal")
ui_plot.set(xlim=[-3, 3], ylim=[-3, 3])

# Рисуем оси и диск
ui_plot.axhline(0, color='black', linewidth=1)  # Горизонтальная ось
ui_plot.axvline(0, color='black', linewidth=1)  # Вертикальная ось
disk, = ui_plot.plot(x_disk + x_disk_middle, y_disk + y_disk_middle, color='black')

# Рисуем стержень и радиус к материальной точке
rod_oc, = ui_plot.plot([x_disk_middle, x_disk_middle], [y_disk_middle, 0], color='black', linewidth=3)
rod_ca, = ui_plot.plot([x_disk_middle, x_disk_middle], [y_disk_middle, y_disk_middle + R], color='blue')

# Рисуем материальную точку
point_a, = ui_plot.plot(x_disk_middle, y_disk_middle + R, color="red", marker="o")

# Рисуем пружину
spiral_spring, = ui_plot.plot(
    x_spiral_spring + x_disk_middle,
    y_spiral_spring + y_disk_middle,
    color="green"
)

# Рисуем шарнир
hinge, = ui_plot.plot(x_disk_middle, y_disk_middle, color="purple", marker="o")

# Создаём окно с графиками
graph_ui, graph_ui_fields = plt.subplots(2, 2, figsize=(15, 7))
graph_ui.canvas.manager.set_window_title('Вариант 9')

# График 1: Фи от времени
graph_ui_fields[0, 0].plot(time_range, phi, color='blue')
graph_ui_fields[0, 0].set_title('Phi (t)')
graph_ui_fields[0, 0].set_ylabel('phi')
graph_ui_fields[1, 0].set_xlabel('Time')
graph_ui_fields[0, 0].grid(True)

# График 2: Пси от времени
graph_ui_fields[0, 1].plot(time_range, psi, color='green')
graph_ui_fields[0, 1].set_title('Psi (t)')
graph_ui_fields[0, 1].set_ylabel('psi')
graph_ui_fields[1, 0].set_xlabel('Time')
graph_ui_fields[0, 1].grid(True)

# График 3: Rx от времени
graph_ui_fields[1, 0].plot(time_range, R_x, color='red')
graph_ui_fields[1, 0].set_title('Rx (t)')
graph_ui_fields[1, 0].set_ylabel('Rx')
graph_ui_fields[1, 0].set_xlabel('Time')
graph_ui_fields[1, 0].grid(True)

# График 4: Ry от времени
graph_ui_fields[1, 1].plot(time_range, R_y, color='purple')
graph_ui_fields[1, 1].set_title('Ry (t)')
graph_ui_fields[1, 1].set_ylabel('Ry')
graph_ui_fields[1, 1].set_xlabel('Time')
graph_ui_fields[1, 1].grid(True)

def animate_plot(frame_number):
    """Функция отвечающая за анимацию плота.

    :param frame_number: Кадр.
    """
    x_disk_middle_rotated, y_disk_middle_rotated = rotate_2d(x_disk_middle, y_disk_middle, phi[frame_number])
    disk.set_data([x_disk + x_disk_middle_rotated], [y_disk + y_disk_middle_rotated])
    rod_oc.set_data([x_disk_middle, x_disk_middle_rotated], [0, y_disk_middle_rotated])
    ca_rotated_x, ca_rotated_y = rotate_2d(0, R, psi[frame_number])
    rod_ca.set_data(
        [x_disk_middle_rotated, ca_rotated_x + x_disk_middle_rotated],
        [y_disk_middle_rotated, ca_rotated_y + y_disk_middle_rotated]
    )
    point_a.set_data([ca_rotated_x + x_disk_middle_rotated], [ca_rotated_y + y_disk_middle_rotated])
    hinge.set_data([x_disk_middle_rotated], [y_disk_middle_rotated])
    x_spiral_spring_rotated, y_spiral_spring_rotated = rotate_2d(x_spiral_spring, y_spiral_spring, psi[frame_number])
    spiral_spring.set_data(
        x_spiral_spring_rotated + x_disk_middle_rotated,
        y_spiral_spring_rotated + y_disk_middle_rotated
    )

    return (
        disk,
        rod_oc,
        rod_ca,
        point_a,
        hinge,
        spiral_spring,
    )

# Воспроизведение анимации и показ плота
animation = FuncAnimation(
    ui,
    animate_plot,
    frames=available_time * 100,
    interval=1/60
)

plt.show()
