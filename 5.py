import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Polygon
from matplotlib.widgets import Slider

x = np.linspace(0, 10, 1000)

# Рандомный выбор типа волны
wave_functions = {
    'sin': lambda x, shift, amplitude: amplitude * np.sin(x + shift),
    'cos': lambda x, shift, amplitude: amplitude * np.cos(x + shift),
}

wave_derivatives = {
    'sin': lambda x, shift, amplitude: amplitude * np.cos(x + shift),
    'cos': lambda x, shift, amplitude: -amplitude * np.sin(x + shift),
}

wave_types = ['sin', 'cos']
wave_type = np.random.choice(wave_types)

delta_shift = 0.2
frames = int(2 * np.pi / delta_shift)
interval = 50
amplitude = np.random.uniform(-1, 1)

y = wave_functions[wave_type](x, 0, amplitude)

fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.3)
line, = ax.plot(x, y, lw=2, label=f"{wave_type}(x)")

ax.set_xlim(0, 10)
ax.set_ylim(-2, 2)
ax.set_title(f"Анимация волны: {wave_type}(x), амплитуда {amplitude}")
ax.set_xlabel("x")
ax.set_ylabel(f"{wave_type}(x)")
ax.set_aspect('equal')

trapezoid = Polygon([[0, 0], [0, 0], [0, 0], [0, 0]], closed=True, color='brown', alpha=0.5)
ax.add_patch(trapezoid)

perpendicular_line, = ax.plot([], [], color='black', lw=2)

width_top, width_bottom, height, mast_height = 1.0, 0.5, 0.3, 1.0

triangle = Polygon([[0, 0], [0, 0], [0, 0]], closed=True, color='#FFD700', alpha=0.5)
ax.add_patch(triangle)

def update(frame):
    if hasattr(update, "fill_between_patch") and update.fill_between_patch:
        update.fill_between_patch.remove()

    shift = frame * delta_shift
    y_shifted = wave_functions[wave_type](x, shift, amplitude)

    line.set_data(x, y_shifted)
    update.fill_between_patch = ax.fill_between(x, -2, y_shifted, color='lightblue', alpha=0.8)

    tangent_x = 5
    tangent_y = wave_functions[wave_type](tangent_x, shift, amplitude)
    tangent_slope = wave_derivatives[wave_type](tangent_x, shift, amplitude)
    angle = np.arctan(tangent_slope)

    top_left = [-width_top / 2, height / 2]
    top_right = [width_top / 2, height / 2]
    bottom_left = [-width_bottom / 2, -height / 2]
    bottom_right = [width_bottom / 2, -height / 2]

    vertices = np.array([top_left, top_right, bottom_right, bottom_left])
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]])
    rotated_vertices = np.matmul(vertices, rotation_matrix.T)
    translated_vertices = rotated_vertices + np.array([tangent_x, tangent_y])

    trapezoid.set_xy(translated_vertices)

    top_side_center = (translated_vertices[0] + translated_vertices[1]) / 2
    top_side_vector = translated_vertices[1] - translated_vertices[0]
    perpendicular_vector = np.array([-top_side_vector[1], top_side_vector[0]])
    perpendicular_vector /= np.linalg.norm(perpendicular_vector)

    start_point = top_side_center
    end_point = top_side_center + perpendicular_vector * mast_height
    perpendicular_line.set_data([start_point[0], end_point[0]], [start_point[1], end_point[1]])

    triangle_top = end_point
    triangle_vertices = np.array([triangle_top, translated_vertices[0], translated_vertices[1]])
    triangle.set_xy(triangle_vertices)

    return line, trapezoid, perpendicular_line, triangle

update.fill_between_patch = None

def update_size(val):
    global width_top, width_bottom, height, mast_height
    width_top = slider_width_top.val
    width_bottom = slider_width_bottom.val
    height = slider_height.val
    mast_height = slider_mast_height.val

ax_slider_width_top = plt.axes([0.2, 0.01, 0.65, 0.03], facecolor='lightgoldenrodyellow')
ax_slider_width_bottom = plt.axes([0.2, 0.06, 0.65, 0.03], facecolor='lightgoldenrodyellow')
ax_slider_height = plt.axes([0.2, 0.11, 0.65, 0.03], facecolor='lightgoldenrodyellow')
ax_slider_mast_height = plt.axes([0.2, 0.16, 0.65, 0.03], facecolor='lightgoldenrodyellow')

slider_width_top = Slider(ax_slider_width_top, 'Width Top', 0.1, 3.0, valinit=width_top)
slider_width_bottom = Slider(ax_slider_width_bottom, 'Width Bottom', 0.1, 3.0, valinit=width_bottom)
slider_height = Slider(ax_slider_height, 'Height', 0.1, 2.0, valinit=height)
slider_mast_height = Slider(ax_slider_mast_height, 'Mast Height', 0.1, 5.0, valinit=mast_height)

slider_width_top.on_changed(update_size)
slider_width_bottom.on_changed(update_size)
slider_height.on_changed(update_size)
slider_mast_height.on_changed(update_size)

ani = FuncAnimation(fig, update, frames=frames, interval=interval, blit=False, repeat=True)
plt.show()
