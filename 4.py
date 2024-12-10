import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

def koch_snowflake(start, end, iterations):
    """Рекурсивная функция для генерации снежинки Коха."""
    if iterations == 0:
        return [start, end]
    vector = end - start
    one_third = start + vector / 3
    two_third = start + 2 * vector / 3
    angle = np.pi / 3
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    peak = one_third + np.dot(rotation_matrix, two_third - one_third)
    return (koch_snowflake(start, one_third, iterations - 1) + 
            koch_snowflake(one_third, peak, iterations - 1) + 
            koch_snowflake(peak, two_third, iterations - 1) + 
            koch_snowflake(two_third, end, iterations - 1))

def generate_snowflake_sides(center, radius, num_sides, iterations):
    """Генерация сторон снежинки Коха с заданным числом лучей."""
    points = []
    for i in range(num_sides):
        angle1 = 2 * np.pi * i / num_sides
        angle2 = 2 * np.pi * (i + 1) / num_sides
        start = center + np.array([radius * np.cos(angle1), radius * np.sin(angle1)])
        end = center + np.array([radius * np.cos(angle2), radius * np.sin(angle2)])
        points.extend(koch_snowflake(start, end, iterations))
    return np.array(points)

def animate_snowflake():
    """Анимация построения снежинки."""
    # Случайные параметры
    num_sides = random.randint(3, 12)  # Количество лучей (3-12)
    iterations = random.randint(1, 4)  # Глубина снежинки (1-4)
    radius = 1.0  # Радиус снежинки
    angle_offset = random.uniform(0, 360)  # Угол поворота (в градусах)
    color = random.choice(['blue', 'cyan', 'white', 'magenta', 'lightblue'])  # Цвет

    # Отладочная информация
    print(f"Количество лучей: {num_sides}, Глубина: {iterations}, Угол: {angle_offset}, Цвет: {color}")

    # Центр снежинки
    center = np.array([0, 0])

    # Генерация точек снежинки
    points = generate_snowflake_sides(center, radius, num_sides, iterations)
    if points.size == 0:
        print("Ошибка: Точки снежинки не сгенерированы.")
        return

    # Поворот снежинки
    points = np.dot(points - center, 
                    [[np.cos(np.radians(angle_offset)), -np.sin(np.radians(angle_offset))],
                     [np.sin(np.radians(angle_offset)), np.cos(np.radians(angle_offset))]]) + center

    # Проверка границ точек
    print(f"Границы снежинки: x({points[:, 0].min()}, {points[:, 0].max()}), y({points[:, 1].min()}, {points[:, 1].max()})")

    # Анимация
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_xlim(-2, 2)  # Увеличенные границы
    ax.set_ylim(-2, 2)

    line, = ax.plot([], [], lw=1, color=color)

    def update(frame):
        """Обновление линии для анимации."""
        current_points = points[:frame]
        x_vals, y_vals = current_points[:, 0], current_points[:, 1]
        line.set_data(x_vals, y_vals)
        return line,

    ani = FuncAnimation(fig, update, frames=len(points), interval=10, blit=True)
    plt.show()

# Запуск программы
if __name__ == "__main__":
    animate_snowflake()
