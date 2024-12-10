import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Создание фигуры и осей
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_xlim(-10, 10)  # Границы по оси X
ax.set_ylim(-10, 10)  # Границы по оси Y
ax.set_aspect('equal')  # Сохранение пропорций

# Добавление сетки
ax.grid(True, linestyle='--', alpha=0.5)

# Добавление кнопки "Очистить"
def clear(event):
    ax.cla()  # Очистить текущие оси
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.draw()

ax_button = plt.axes([0.8, 0.02, 0.1, 0.05])  # Положение кнопки
button = Button(ax_button, 'Очистить')
button.on_clicked(clear)

# Отображение окна
plt.show()
