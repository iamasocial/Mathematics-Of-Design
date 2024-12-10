# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# import random

# # Генерация случайных параметров
# num_rays = random.randint(5, 15)  # Количество лучей
# inner_radius = 1  # Радиус внутреннего круга
# outer_radius = random.uniform(1.5, 3)  # Радиус внешнего круга
# colors = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(num_rays)]  # Случайные цвета

# # Функция для вычисления координат звезды
# def generate_star(num_rays, inner_radius, outer_radius):
#     angles = np.linspace(0, 2 * np.pi, num_rays * 2, endpoint=False)
#     radii = np.array([outer_radius if i % 2 == 0 else inner_radius for i in range(num_rays * 2)])
#     x = radii * np.cos(angles)
#     y = radii * np.sin(angles)
#     return x, y

# # Генерация координат звезды
# x, y = generate_star(num_rays, inner_radius, outer_radius)

# # Подготовка графика
# fig, ax = plt.subplots()
# ax.set_aspect('equal')
# ax.set_xlim(-outer_radius * 1.5, outer_radius * 1.5)
# ax.set_ylim(-outer_radius * 1.5, outer_radius * 1.5)
# ax.axis('off')  # Убрать оси

# # Добавление цветов к секторам
# polygons = []
# for i in range(0, len(x) - 1, 2):
#     polygon = ax.fill([0, x[i], x[i + 1]], [0, y[i], y[i + 1]], color=colors[i // 2])[0]
#     polygons.append(polygon)

# # Анимация
# def update(frame):
#     for i, poly in enumerate(polygons):
#         if i < frame:
#             poly.set_visible(True)

# ani = FuncAnimation(fig, update, frames=num_rays, interval=300, repeat=False)
# plt.show()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# Генерация случайных параметров
num_rays = random.randint(5, 15)  # Количество лучей (от 5 до 15)
inner_radius = 1  # Радиус внутреннего круга
outer_radius = random.uniform(1.5, 3)  # Радиус внешнего круга (1.5–3)
colors = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(num_rays)]  # Случайные цвета для секторов

# Функция для вычисления координат звезды
def generate_star(num_rays, inner_radius, outer_radius):
    angles = np.linspace(0, 2 * np.pi, num_rays * 2, endpoint=False)
    radii = np.array([outer_radius if i % 2 == 0 else inner_radius for i in range(num_rays * 2)])
    x = radii * np.cos(angles)
    y = radii * np.sin(angles)
    return x, y

# Генерация координат звезды
x, y = generate_star(num_rays, inner_radius, outer_radius)

# Подготовка графика
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.set_xlim(-outer_radius * 1.5, outer_radius * 1.5)
ax.set_ylim(-outer_radius * 1.5, outer_radius * 1.5)
ax.axis('off')  # Убрать оси

# Слои для секторов
polygons = []
for i in range(0, len(x) - 1, 2):
    polygon = ax.fill([0, x[i], x[i + 1]], [0, y[i], y[i + 1]], color=colors[i // 2], visible=False)[0]
    polygons.append(polygon)

# Анимация
def update(frame):
    if frame < len(polygons):
        polygons[frame].set_visible(True)  # Постепенно включать видимость секторов
    return polygons

ani = FuncAnimation(fig, update, frames=num_rays, interval=500, blit=True, repeat=False)

plt.show()
