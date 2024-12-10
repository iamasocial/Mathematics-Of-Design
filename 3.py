import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Функции для генерации фракталов
# def koch_curve(start, end, iterations):
#     if iterations == 0:
#         return [start, end]
#     vector = end - start
#     one_third = start + vector / 3
#     two_third = start + 2 * vector / 3
#     angle = np.pi / 3
#     rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
#     peak = one_third + np.dot(rotation_matrix, two_third - one_third)
#     return koch_curve(start, one_third, iterations - 1) + koch_curve(one_third, peak, iterations - 1) + \
#            koch_curve(peak, two_third, iterations - 1) + koch_curve(two_third, end, iterations - 1)
def koch(start, end, iterations, angle_degrees=60):
    """
    Генерация кривой Коха.

    :param start: Начальная точка.
    :param end: Конечная точка.
    :param iterations: Количество итераций.
    :param angle_degrees: Угол поворота в градусах.
    :return: Список точек.
    """
    if iterations == 0:
        return [start, end]

    # Конвертация угла из градусов в радианы
    angle = np.radians(angle_degrees)

    vector = end - start
    one_third = start + vector / 3
    two_third = start + 2 * vector / 3

    # Матрица поворота на заданный угол
    rotation_matrix = np.array([
        [np.cos(angle), -np.sin(angle)],
        [np.sin(angle), np.cos(angle)]
    ])

    # Вычисляем "пик"
    peak = one_third + np.dot(rotation_matrix, two_third - one_third)

    # Рекурсивная генерация для каждой части
    return (
        koch(start, one_third, iterations - 1, angle_degrees) +
        koch(one_third, peak, iterations - 1, angle_degrees) +
        koch(peak, two_third, iterations - 1, angle_degrees) +
        koch(two_third, end, iterations - 1, angle_degrees)
    )

def tree(start, angle, length, iterations):
    if iterations == 0:
        return []

    # Конечная точка текущей ветви
    start = np.array(start, dtype=float)
    end = start + np.array([length * np.cos(angle), length * np.sin(angle)], dtype=float)

    # Рекурсивно добавляем ветви
    left_branch = tree(end, angle + np.pi / 6, length * 0.7, iterations - 1)
    right_branch = tree(end, angle - np.pi / 6, length * 0.7, iterations - 1)

    result = [(start, end)] + left_branch + right_branch
    
    # print(f"generate_tree(start={start}, angle={angle}, length={length}, iterations={iterations}) -> {len(result)} segments")

    return result

def sierpinski(points, iterations):
    if iterations == 0:
        return points
    mid1 = (points[0] + points[1]) / 2
    mid2 = (points[1] + points[2]) / 2
    mid3 = (points[2] + points[0]) / 2
    return sierpinski([points[0], mid1, mid3], iterations - 1) + \
           sierpinski([mid1, points[1], mid2], iterations - 1) + \
           sierpinski([mid3, mid2, points[2]], iterations - 1)



def mandelbrot(width, height, max_iter=256):
    # Диапазоны для осей x и y
    x_min, x_max = -2.5, 1.0
    y_min, y_max = -1.5, 1.5

    # Создание пустой матрицы для изображения
    image = np.zeros((height, width))

    for y in range(height):
        for x in range(width):
            # Преобразование пикселей в координаты на комплексной плоскости
            c = complex(x_min + (x / width) * (x_max - x_min),
                        y_min + (y / height) * (y_max - y_min))
            z = 0
            iteration = 0

            # Итерации для проверки, уходит ли точка за пределы
            while abs(z) <= 2 and iteration < max_iter:
                z = z*z + c
                iteration += 1

            # Сохраняем количество итераций
            image[y, x] = iteration

    return image


def julia(width, height, x_min, x_max, y_min, y_max, c, max_iter):
    # Создаём сетку комплексной плоскости
    x = np.linspace(x_min, x_max, width)
    y = np.linspace(y_min, y_max, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    # Итерации
    iteration_counts = np.zeros(Z.shape, dtype=int)
    mask = np.ones(Z.shape, dtype=bool)

    for i in range(max_iter):
        Z[mask] = Z[mask] ** 2 + c
        mask = np.abs(Z) < 2  # Проводим проверку, не вышли ли точки за пределы
        iteration_counts += mask

    return iteration_counts

def levy(p1, p2, iterations):
    # Начальные точки
    points = np.array([p1, p2])

    for _ in range(iterations):
        # Генерируем новые точки
        new_points = []
        for i in range(len(points) - 1):
            a, b = points[i], points[i + 1]

            # Середина отрезка
            mid = (a + b) / 2

            # Смещение на 90 градусов (по часовой стрелке)
            offset = np.array([-(b[1] - a[1]), b[0] - a[0]]) / 2
            new_point = mid + offset

            # Добавляем текущую точку и новую точку
            new_points.extend([a, new_point])
        new_points.append(points[-1])  # Добавляем последнюю точку

        points = np.array(new_points)

    return points

def generate_dragon_instructions(iterations):
    old = 'r'
    for _ in range(iterations):
        new = old + 'r' + old[::-1].translate(str.maketrans('rl', 'lr'))
        old = new
    return old

def dragon(length, iterations):
    instructions = generate_dragon_instructions(iterations)
    points = [np.array([0, 0])]
    direction = np.array([length, 0])  # Вектор направления

    for instruction in instructions:
        # Добавляем новую точку, повернув направление
        last_point = points[-1]
        if instruction == 'r':  # Правый поворот
            direction = np.array([direction[1], -direction[0]])
        elif instruction == 'l':  # Левый поворот
            direction = np.array([-direction[1], direction[0]])
        new_point = last_point + direction
        points.append(new_point)

    return np.array(points)

# Функция для анимации
def animate_fractal(fractal_name, max_iterations=10, angle_degrees=None):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_aspect('equal')
    ax.set_axis_off()

    width, height = 400, 400
    x_min, x_max, y_min, y_max = -2, 2, -2, 2
    c = complex(-0.7, 0.27015)

    def update(frame):
        ax.clear()
        ax.set_aspect('equal')
        ax.set_axis_off()

        # Генерация фрактала в зависимости от его типа
        if fractal_name == 'koch':
            points = koch(np.array([0, 0]), np.array([1, 0]), frame, angle_degrees)
            x_vals, y_vals = zip(*points)
            ax.plot(x_vals, y_vals, lw=0.5, color='blue')
            ax.set_title(f"Koch curve set Iteration {frame}")

        elif fractal_name == 'tree': 
            segments = tree(np.array([0.5, 0]), np.pi / 2, 0.2, frame)

            for segment in segments:
                if len(segment) == 2:  # Проверяем, что это пара (start, end)
                    start, end = segment
                    if isinstance(start, np.ndarray) and isinstance(end, np.ndarray):  # Убеждаемся, что это массивы
                        # print(f"Segment: start={start}, end={end}, type(start)={type(start)}, type(end)={type(end)}")
                        ax.plot([start[0], end[0]], [start[1], end[1]], color='green', lw=0.5)
                        ax.set_title(f"Tree set Iteration {frame}")
                    else:
                        print(f"Invalid segment: start={start}, end={end}")
                else:
                    print(f"Invalid segment format: {segment}")

        elif fractal_name == 'sierpinski':
            points = sierpinski([np.array([0, 0]), np.array([1, 0]), np.array([0.5, np.sqrt(3)/2])], frame)
            x_vals, y_vals = zip(*points)
            ax.plot(x_vals, y_vals, lw=0.5, color='red')

        elif fractal_name == 'levy':
            points = levy(np.array([0, 0]), np.array([1, 0]), frame)
            x_vals, y_vals = points[:, 0], points[:, 1]
            ax.plot(x_vals, y_vals, lw=0.5, color='magenta')
            ax.set_title(f"Levy Curve - Iteration {frame}")

        elif fractal_name == 'dragon':
            # points = dragon_curve_points(1, frame, angle=90)

            points = dragon(1, frame)  # Длина сегмента = 1
            x_vals, y_vals = points[:, 0], points[:, 1]
            ax.plot(x_vals, y_vals, lw=0.5, color='blue')
            ax.set_title(f"Dragon Curve - Iteration {frame}")
            # ax.set_title(f"Dragon set Iteration {frame}")

        elif fractal_name == 'mandelbrot':
            points = mandelbrot(width, height, frame)
            ax.imshow(points, cmap='inferno', extent=(-2.5,1.0,-1.5,1.5))
            ax.set_title(f"Mandelbrot set Iteration {frame}")

        elif fractal_name == 'julia':
            data = julia(width, height, x_min, x_max, y_min, y_max, c, frame)
            ax.imshow(data, extent=(x_min, x_max, y_min, y_max), cmap='twilight', origin='lower')
            ax.set_title(f"Julia Set - Iteration {frame}")

    ani = FuncAnimation(fig, update, frames=max_iterations, interval=200)
    plt.show()

# Вызов функции с фракталом "koch_curve"
# animate_fractal('koch', max_iterations=100)

def main():
    print("Добро пожаловать в генератор фракталов!")
    print("Доступные фракталы:")
    print("1. Кривая Коха")
    print("2. Дракон Хартера-Хейтуэя")
    print("3. Треугольник Серпинского")
    print("4. Множество Мандельброта")
    print("5. Дерево (веточка)/(ковыль)")
    print("6. Множество Жюлиа")
    print("7. Кривая Леви")
    
    # Выбор фрактала
    fractal_map = {
        '1': 'koch',
        '2': 'dragon',
        '3': 'sierpinski',
        '4': 'mandelbrot',
        '5': 'tree',
        '6': 'julia',
        '7': 'levy'
    }
    choice = input("Введите номер фрактала для генерации: ")
    if choice not in fractal_map:
        print("Ошибка: некорректный выбор.")
        return
    
    fractal_name = fractal_map[choice]

    # Запрос параметров
    iterations = int(input("Введите количество итераций (например, 5): "))
    angle_degrees = None
    if fractal_name in ['koch', 'dragon', 'tree']:
        angle_degrees = float(input("Введите угол в градусах (например, 60): "))

    # Анимация выбранного фрактала
    print(f"Генерация фрактала: {fractal_name}")
    animate_fractal(fractal_name, iterations, angle_degrees)
    print("Генерация завершена!")

main()
