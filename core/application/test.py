from formation import AppBuilder
import tkinter as tk
from Converter import Converter
from tkinter import filedialog
from PIL import Image, ImageTk


app = AppBuilder(path="core\\resources\\main.xml")



window = app.tk_1
entry = app.entry_label
error_label = app.error_label
photo_label = app.photo_label
list_box = app.list_box
load_file_button = app.loadfilebutton


def get_selected():
    return [list_box.get(idx) for idx in list_box.curselection()]

def convert_image():
    """Преобразует введенную строку в имя файла изображения и отображает его."""
    smiles_string : str = entry.get() 
    if smiles_string.strip() == "":
        selected_values_list = get_selected()
        if(len(selected_values_list) != 1):
            error_label.config(text = "Choose 1 formula")
            return
        else:
            smiles_string = selected_values_list[0]
    
    try:
        converter = Converter()
        image = converter.convert(smiles_string, 600, 600)
        photo = ImageTk.PhotoImage(image)
        photo_label.config(image=photo)
        photo_label.image = photo  # Сохраняем ссылку, чтобы изображение не удалялось
    except Exception:
        error_label.config(text = "Convert error")

def copy_to_entry():
    """Копирует текст из буфера обмена в поле ввода."""
    try:
        clipboard_text = window.clipboard_get()
        entry.delete(0, "end")
        entry.insert(0, clipboard_text)
    except Exception as e:
        error_label.config(text = "Error")

def load_from_file():
    dir_name = filedialog.askopenfile()
    with open(dir_name.name, "r") as file:
        for line in file.readlines():
            list_box.insert("end", line)

app.connect_callbacks(globals())

if __name__ == "__main__":
    app.mainloop()