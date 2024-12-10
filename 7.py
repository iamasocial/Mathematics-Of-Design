import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import threading

# Параметры
speed = 0.02  # начальная скорость шариков
min_speed = 0.005  # минимальная скорость, чтобы предотвратить застревание
angle_deviation_range = (-0.1, 0.1)  # Диапазон отклонений угла в радианах

# Начальные параметры
initial_num_balls = 5  # начальное количество шариков

# Начальные позиции, скорости и размеры
positions = np.random.rand(initial_num_balls, 2) * 0.8 + 0.1  # случайные начальные позиции
velocities = np.random.randn(initial_num_balls, 2) * speed  # случайные начальные скорости
colors = np.random.rand(initial_num_balls, 3)  # случайные цвета, генерация RGB
radii = np.ones(initial_num_balls) * 0.05  # все шарики изначально одного размера

# Минимальное расстояние между шариками
min_distance = 2 * np.min(radii)

# Флаг завершения работы
exit_flag = False

# Функция для генерации случайного отклонения угла
def random_angle_deviation():
    return np.random.uniform(angle_deviation_range[0], angle_deviation_range[1])

# Функция для обновления позиций шариков
def update(frame):
    global positions, velocities, radii

    if exit_flag:  # Если флаг завершения установлен, анимация останавливается
        plt.close()
        return []

    # Обновление позиций
    positions += velocities

    # Проверка на столкновения с границами и корректировка
    for i in range(len(positions)):
        hit_boundary = False

        if positions[i, 0] <= radii[i]:  # Левый край
            velocities[i, 0] = np.abs(velocities[i, 0])  # скорость по X положительная
            hit_boundary = True
        if positions[i, 0] >= 1 - radii[i]:  # Правый край
            velocities[i, 0] = -np.abs(velocities[i, 0])  # скорость по X отрицательная
            hit_boundary = True
        if positions[i, 1] <= radii[i]:  # Нижний край
            velocities[i, 1] = np.abs(velocities[i, 1])  # скорость по Y положительная
            hit_boundary = True
        if positions[i, 1] >= 1 - radii[i]:  # Верхний край
            velocities[i, 1] = -np.abs(velocities[i, 1])  # скорость по Y отрицательная
            hit_boundary = True

        # Если шарик оказался на границе (практически на границе), слегка сдвигаем его внутрь
        if hit_boundary:
            if positions[i, 0] <= radii[i]:  # Левый край
                positions[i, 0] = radii[i]
            if positions[i, 0] >= 1 - radii[i]:  # Правый край
                positions[i, 0] = 1 - radii[i]
            if positions[i, 1] <= radii[i]:  # Нижний край
                positions[i, 1] = radii[i]
            if positions[i, 1] >= 1 - radii[i]:  # Верхний край
                positions[i, 1] = 1 - radii[i]

            # Случайное отклонение угла от границы
            angle_deviation = random_angle_deviation()
            velocity_angle = np.arctan2(velocities[i, 1], velocities[i, 0])  # текущий угол скорости
            new_angle = velocity_angle + angle_deviation  # новое направление с отклонением
            speed_magnitude = np.linalg.norm(velocities[i])  # сохраняем текущую скорость
            velocities[i] = speed_magnitude * np.array([np.cos(new_angle), np.sin(new_angle)])

    # Проверка столкновений между шариками
    for i in range(len(positions)):
        for j in range(i + 1, len(positions)):  # Сравниваем каждую пару шариков
            dist = np.linalg.norm(positions[i] - positions[j])
            if dist < radii[i] + radii[j]:  # Если расстояние меньше суммы радиусов, происходит столкновение
                # Вектор от одного шарика к другому
                direction = positions[i] - positions[j]
                direction /= np.linalg.norm(direction)  # Нормализуем

                # Вектор вдоль направления столкновения
                relative_velocity = velocities[i] - velocities[j]
                speed_in_direction = np.dot(relative_velocity, direction)

                # Если скорость вдоль направления столкновения положительная, меняем скорости
                if speed_in_direction < 0:
                    # Перераспределяем скорости в зависимости от массы (для одинаковых масс просто меняем)
                    velocities[i] -= speed_in_direction * direction
                    velocities[j] += speed_in_direction * direction

                    # Корректируем их позиции, чтобы избежать наложения
                    overlap = radii[i] + radii[j] - dist
                    correction_vector = direction * overlap / 2
                    positions[i] += correction_vector
                    positions[j] -= correction_vector

                    # Добавляем случайное отклонение угла после столкновения
                    angle_deviation = random_angle_deviation()
                    velocity_angle_i = np.arctan2(velocities[i, 1], velocities[i, 0])  # текущий угол скорости
                    velocity_angle_j = np.arctan2(velocities[j, 1], velocities[j, 0])

                    new_angle_i = velocity_angle_i + angle_deviation
                    new_angle_j = velocity_angle_j + angle_deviation

                    speed_magnitude_i = np.linalg.norm(velocities[i])
                    speed_magnitude_j = np.linalg.norm(velocities[j])

                    velocities[i] = speed_magnitude_i * np.array([np.cos(new_angle_i), np.sin(new_angle_i)])
                    velocities[j] = speed_magnitude_j * np.array([np.cos(new_angle_j), np.sin(new_angle_j)])

    # Очистка экрана и отрисовка новых позиций
    plt.clf()
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.gca().set_aspect('equal', adjustable='box')

    # Отображение шариков
    for i, pos in enumerate(positions):
        circle = plt.Circle(pos, radii[i], color=colors[i], ec="black")  # Используем размер для каждого шарика
        plt.gca().add_artist(circle)

    return []

# Функция для добавления новых шариков
def add_new_balls(num_new_balls):
    global positions, velocities, colors, radii
    new_positions = np.random.rand(num_new_balls, 2) * 0.8 + 0.1
    new_velocities = np.random.randn(num_new_balls, 2) * speed  # Генерация случайных начальных скоростей
    new_colors = np.random.rand(num_new_balls, 3)  # Генерация случайных цветов для новых шариков
    new_radii = np.full_like(np.zeros(num_new_balls), radii[0])  # Новые шарики такого же размера, что и старые

    positions = np.vstack((positions, new_positions))
    velocities = np.vstack((velocities, new_velocities))  # Добавляем скорости для новых шариков
    colors = np.vstack((colors, new_colors))  # Добавляем новые случайные цвета
    radii = np.hstack((radii, new_radii))

# Функция для удаления шариков
def remove_balls(num_remove_balls):
    global positions, velocities, colors, radii
    positions = positions[:-num_remove_balls]
    velocities = velocities[:-num_remove_balls]
    colors = colors[:-num_remove_balls]
    radii = radii[:-num_remove_balls]

# Функция для изменения размера шариков
def set_balls_size():
    global radii
    while True:
        try:
            new_size = float(input("Введите размер шариков (например, 0.05): "))
            if new_size > 0:
                radii = np.full_like(radii, new_size)
                break
            else:
                print("Размер должен быть положительным числом.")
        except ValueError:
            print("Пожалуйста, введите корректное значение.")

# Функция для пользовательского ввода
def user_input():
    global exit_flag
    while True:
        print("1. Изменить количество шариков")
        print("2. Изменить размер шариков")
        print("3. Завершить")
        choice = input("Введите номер опции: ")

        if choice == '1':
            try:
                new_num_balls = int(input("Введите новое количество шариков: "))
                if new_num_balls > 0:
                    # Добавление или удаление шариков
                    if new_num_balls > len(positions):
                        add_new_balls(new_num_balls - len(positions))
                    elif new_num_balls < len(positions):
                        remove_balls(len(positions) - new_num_balls)
                    initial_num_balls = new_num_balls
                else:
                    print("Количество шариков должно быть положительным числом.")
            except ValueError:
                print("Пожалуйста, введите целое число.")
        elif choice == '2':
            set_balls_size()
        elif choice == '3':
            exit_flag = True
            break
        else:
            print("Неверный ввод. Пожалуйста, попробуйте снова.")

# Функция для запуска анимации с возможностью взаимодействия
def run_animation():
    fig = plt.figure()
    ani = FuncAnimation(fig, update, frames=100, interval=50, blit=False)

    # Запуск в отдельном потоке для обработки пользовательского ввода
    input_thread = threading.Thread(target=user_input)
    input_thread.daemon = True
    input_thread.start()

    plt.show()

run_animation()
