import tkinter as tk
from tkinter import messagebox
import random
import pulsectl
import string
import os  # Для выполнения команды выключения

# Класс для кнопки с капчей
class ButtonWithCaptcha:
    def __init__(self, root):
        self.root = root
        self.display = True  # Поле для управления отображением кнопки
        self.button = tk.Button(root, text="Нажми меня", command=self.show_captcha)
        self.button.place(x=150, y=100)
        self.button.bind("<Enter>", self.move_button_with_delay)

        # Элементы для капчи
        self.captcha_label = tk.Label(root)
        self.captcha_entry = tk.Entry(root)
        self.captcha_submit = tk.Button(root, text="Проверить", command=self.check_captcha)

        # Генерация капчи
        self.correct_captcha = self.generate_captcha()

    # Функция для генерации капчи
    def generate_captcha(self):
        characters = string.ascii_letters + string.digits  # Все буквы и цифры
        captcha = ''.join(random.choice(characters) for _ in range(6))  # Генерируем строку из 8 символов
        return captcha

    # Функция для проверки капчи
    def check_captcha(self):
        user_input = self.captcha_entry.get()
        if user_input == self.correct_captcha:
            self.change_volume()
            messagebox.showinfo("Успех", "Капча введена верно! Громкость изменена.")
            self.reset_interface()  # Сбрасываем интерфейс для нового цикла
        else:
            messagebox.showerror("Ошибка", "Неверная капча. Компьютер будет выключен.")
            self.shutdown_computer()  # Выключаем компьютер

    # Функция для изменения громкости
    def change_volume(self):
        try:
            with pulsectl.Pulse('volume-changer') as pulse:
                # Получаем основное аудиоустройство (по умолчанию)
                sink = pulse.sink_default_get()
                if not sink:
                    messagebox.showerror("Ошибка", "Не удалось найти основное аудиоустройство.")
                    return

                # Генерируем случайный уровень громкости (от 0 до 1)
                new_volume = random.uniform(0.0, 1.0)

                # Устанавливаем громкость
                pulse.volume_set_all_chans(sink, new_volume)

                # Показ уведомления
                messagebox.showinfo("Громкость изменена", f"Новый уровень громкости: {new_volume:.2f}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось изменить громкость: {e}")

    # Функция для перемещения кнопки с задержкой
    def move_button_with_delay(self, event=None):
        if self.display:  # Перемещаем кнопку, только если она отображается
            # Задержка в 0.1 секунды
            self.root.after(400, self.move_button)

    # Функция для перемещения кнопки
    def move_button(self):
        if self.display:  # Перемещаем кнопку, только если она отображается
            # Генерируем случайные координаты для кнопки
            x = random.randint(0, self.root.winfo_width() - self.button.winfo_width())
            y = random.randint(0, self.root.winfo_height() - self.button.winfo_height())
            self.button.place(x=x, y=y)

    # Функция для отображения капчи после нажатия на кнопку
    def show_captcha(self):
        self.display = False  # Скрываем кнопку
        self.button.place_forget()
        self.captcha_label.config(text=f"Введите капчу: {self.correct_captcha}")
        self.captcha_label.pack()
        self.captcha_entry.pack()
        self.captcha_submit.pack()

    # Функция для сброса интерфейса
    def reset_interface(self):
        self.correct_captcha = self.generate_captcha()  # Обновляем капчу
        self.captcha_label.config(text=f"Введите капчу: {self.correct_captcha}")
        self.captcha_entry.delete(0, tk.END)  # Очищаем поле ввода
        self.captcha_label.pack_forget()
        self.captcha_entry.pack_forget()
        self.captcha_submit.pack_forget()
        self.button.place(x=150, y=100)  # Показываем кнопку снова
        self.display = True  # Показываем кнопку

    # Функция для выключения компьютера
    def shutdown_computer(self):
        if os.name == 'posix':
            os.system("shutdown -h now")

# Создание окна
root = tk.Tk()
root.title("Неудобное изменение громкости")
root.geometry("400x300")

# Создание объекта кнопки с капчей
button_with_captcha = ButtonWithCaptcha(root)

# Запуск приложения
root.mainloop()