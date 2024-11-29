"""Класс для определения отслеживаемой точки и её векторов со стрелками"""
import sympy as sp
from matplotlib import use as fix_ui
import numpy as np
from arrow import Arrow


class DrawingHead:
    def __init__(self, radius, phi_angle, variable: sp.Symbol, time_range_limit=10):
        fix_ui('TkAgg')
        # Переход к декартовым координатам
        x = radius * sp.cos(phi_angle)
        y = radius * sp.sin(phi_angle)
        # Получение формулы скорости через производную
        v_x = sp.diff(x, variable)
        v_y = sp.diff(y, variable)
        v = (v_x ** 2 + v_y ** 2) ** 0.5
        # Получение формулы ускорения через производную
        w_x = sp.diff(v_x, variable)
        w_y = sp.diff(v_y, variable)
        w = (w_x ** 2 + w_y ** 2) ** 0.5
        # Получение формулы тангенциального ускорения
        w_tg = sp.diff(v, variable)
        w_tg_x = v_x / v * w_tg
        w_tg_y = v_y / v * w_tg
        # Получение формулы нормального ускорения
        w_normal = (w ** 2 - w_tg ** 2) ** 0.5
        w_normal_x = w_x - w_tg_x
        w_normal_y = w_y - w_tg_y
        # Получение нормали
        n_x = w_normal_x / w_normal
        n_y = w_normal_y / w_normal
        # Получение формулы радиуса кривизны по формуле v^2/w
        curvature_module = (v ** 2 / w_normal)
        curvature_x = curvature_module * n_x
        curvature_y = curvature_module * n_y
        # Определение временного промежутка и деление его на части
        time_range = np.linspace(0, time_range_limit, 100 * time_range_limit)
        # Определение лямбда-функций для каждой из определённых ранее переменных
        x_lambda_function = sp.lambdify(variable, x, "numpy")
        y_lambda_function = sp.lambdify(variable, y, "numpy")
        v_x_lambda_function = sp.lambdify(variable, v_x, "numpy")
        v_y_lambda_function = sp.lambdify(variable, v_y, "numpy")
        w_x_labda_function = sp.lambdify(variable, w_x, "numpy")
        w_y_lambda_function = sp.lambdify(variable, w_y, "numpy")
        curvature_x_labda_function = sp.lambdify(variable, curvature_x, "numpy")
        curvature_y_labda_function = sp.lambdify(variable, curvature_y, "numpy")
        # Подстановка временного промежутка в лямбда-функцию и получение массива значений
        # всех переменных для каждого момента времени
        self.time_range_limit = time_range_limit
        self.x_values = x_lambda_function(time_range)
        self.y_values = y_lambda_function(time_range)
        self.v_x_values = v_x_lambda_function(time_range)
        self.v_y_values = v_y_lambda_function(time_range)
        self.w_x_values = w_x_labda_function(time_range)
        self.w_y_values = w_y_lambda_function(time_range)
        self.curvature_x_values = curvature_x_labda_function(time_range)
        self.curvature_y_values = curvature_y_labda_function(time_range)
        # Определение векторов скорости, ускорения, радиус-вектора и радиуса кривизны, учитывая их направление
        self.velocity_arrow = Arrow(self.x_values, self.y_values, self.v_x_values, self.v_y_values)
        self.acceleration_arrow = Arrow(self.x_values, self.y_values, self.w_x_values, self.w_y_values, arrow_length_coefficient=0.1)
        self.radius_arrow = Arrow(np.zeros_like(self.x_values), np.zeros_like(self.y_values), self.x_values, self.y_values, arrow_length_coefficient=1, arrow_size_coefficient=2)
        self.curvature_arrow = Arrow(self.x_values, self.y_values, self.curvature_x_values, self.curvature_y_values, arrow_length_coefficient=0.5, arrow_size_coefficient=2)