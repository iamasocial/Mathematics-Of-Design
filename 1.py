import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Параметры спирали
a = 0.1  # Множитель спирали
theta_step_options = [0.1, 0.2, 0.5]  # Шаг изменения угла

# Выбор шага пользователем
print("Выберите угол изменения (1, 2 или 3):")
print(f"1 - {theta_step_options[0]}, 2 - {theta_step_options[1]}, 3 - {theta_step_options[2]}")
choice = int(input("Введите номер опции: ")) - 1
theta_step = theta_step_options[choice]

# Параметры анимации
theta_max = 10 * np.pi  # Максимальный угол
theta_values = np.arange(0, theta_max, theta_step)
r_values = a * theta_values
x_values = r_values * np.cos(theta_values)
y_values = r_values * np.sin(theta_values)

# Создание графика
fig, ax = plt.subplots()
ax.set_xlim(-a * theta_max, a * theta_max)
ax.set_ylim(-a * theta_max, a * theta_max)
line, = ax.plot([], [], lw=2)

# Функция для анимации
def update(frame):
    line.set_data(x_values[:frame], y_values[:frame])
    return line,

ani = FuncAnimation(fig, update, frames=len(theta_values), interval=50, blit=True)

plt.show()
