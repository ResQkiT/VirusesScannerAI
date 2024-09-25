import tkinter as tk
from Converter import Converter
from tkinter import filedialog
from PIL import Image, ImageTk


def convert_image():
    """Преобразует введенную строку в имя файла изображения и отображает его."""
    smiles_string = entry.get()
    try:
        converter = Converter()
        image = converter.convert(smiles_string)
        photo = ImageTk.PhotoImage(image)
        label.config(image=photo)
        label.image = photo  # Сохраняем ссылку, чтобы изображение не удалялось
    except Exception:
        error_label.config("Произошла ошибка")

def copy_to_entry():
    """Копирует текст из буфера обмена в поле ввода."""
    try:
        clipboard_text = window.clipboard_get()
        entry.delete(0, "end")
        entry.insert(0, clipboard_text)
    except Exception as e:
        error_label.config(text=f"Ошибка копирования: {e}")

window = tk.Tk()
window.title("Smiles converter")
window.geometry("500x600")

# Поле ввода
entry = tk.Entry(window, width=450)
entry.pack()

# Кнопка "Вставить из буфера"
button = tk.Button(window, text="Вставить из буфера", command=copy_to_entry)
button.pack()

# Кнопка "Преобразовать"
button = tk.Button(window, text="Преобразовать", command=convert_image)
button.pack()

# Окно для отображения изображения
label = tk.Label(window)
label.pack()

# Лейбл для сообщения об ошибке
error_label = tk.Label(window, text="", fg="red")
error_label.pack()

if __name__ == "__main__":
    window.mainloop()