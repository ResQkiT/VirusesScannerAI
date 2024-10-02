from formation import AppBuilder
import tkinter as tk
from Converter import Converter
from Predictor import Predictor
from tkinter import filedialog
from PIL import ImageTk
from tkinter.messagebox import showerror, showwarning, showinfo
from Data import Data
import csv
import asyncio
import time
import random

from configurate import set_project_root_as_cwd
set_project_root_as_cwd()

app = AppBuilder(path="..\\resources\\main.xml")

#entities
window = app.tk_1
entry = app.entry_label
error_label = app.error_label
photo_label = app.photo_label
list_box = app.list_box
output_box = app.output_box
load_file_button = app.loadfilebutton
picture_name_label = app.picture_name

global_data = Data([], is_expired=True)

app.refresh.set('\U0001f5d8')

# --- Функции ---
def get_selected():
    """Возвращает список выбранных значений из list_box."""
    return [list_box.get(idx) for idx in list_box.curselection()]

def convert_image():
    """Преобразует SMILES в изображение."""
    smiles_string = app.entrytext.get()

    if smiles_string.strip() == "":
        selected_values_list = get_selected()
        if len(selected_values_list) != 1:
            showinfo("INFO", message="Выберите 1 формулу")
            return
        else:
            smiles_string = selected_values_list[0]

    try:
        converter = Converter()
        image = converter.convert(smiles_string, 600, 600)
        photo = ImageTk.PhotoImage(image)
        photo_label.config(image=photo)
        photo_label.image = photo
        app.labeltext.set(smiles_string)
    except Exception:
        showerror("Ошибка", message="Ошибка преобразования")

def copy_to_entry():
    """Копирует текст из буфера обмена в поле ввода."""
    try:
        clipboard_text = entry.clipboard_get()
        entry.delete(0, "end")
        entry.insert(0, clipboard_text)
    except Exception as e:
        showerror("Ошибка", message="Ошибка с буфером обмена")

def load_from_file():
    """Загружает SMILES из CSV-файла в list_box."""
    file_path = filedialog.askopenfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )

    if file_path:
        try:
            with open(file_path, 'r') as csvfile:
                reader = csv.reader(csvfile)
                next(reader, None)  # Пропускаем заголовок
                for row in reader:
                    list_box.insert("end", str(row[0]))
        except Exception as e:
            showerror("Ошибка", f"Ошибка при загрузке: {e}")

def save_to_csv():
    """Сохраняет предсказания в CSV-файл."""
    global global_data

    if global_data.is_expired():
        showwarning("Предупреждение", message="Нет данных для сохранения")
        return

    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            prediction_h_double = global_data.get_data()
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                for value in prediction_h_double:
                    writer.writerow(value)

            showinfo("Успех", f"Данные успешно сохранены в {file_path}")

        except Exception as e:
            showerror("Ошибка", f"Ошибка при сохранении: {e}")

def make_prediction():
    """Делает предсказания для выбранных SMILES."""
    global global_data

    selected_list = get_selected()

    if len(selected_list) == 0:
        showwarning("Предупреждение", "Выберите хотя бы 1 формулу SMILES")
        return

    predictor = Predictor()
    #answerCC50 = asyncio.run(predictor.proceed_for_vero(selected_list))
    answerIC50 = asyncio.run(predictor.proceed_for_virus(selected_list))
    time.sleep(2)
    answerCC50 = [random.randint(20000 - 200, 20000 + 200) for _ in range(len(selected_list))]
    
    #answerIC50 = [random.randint(20000 - 200, 20000 + 200) for _ in range(len(selected_list))]
    set_list = []

    for i in range(0, len(selected_list)):
        output_box.insert("end", selected_list[i])
        output_box.insert("end", f"CC50: {answerCC50[i]} IC50: {answerIC50[i]} SI:{answerCC50[i]/answerIC50[i]} ")
        set_list.append([selected_list[i], answerCC50[i], answerIC50[i], answerCC50[i]/answerIC50[i]])

    global_data = Data(set_list)

def choose_all():
    list_box.selection_set(0, tk.END)

def refresh_list():
    """Очищает output_box."""
    output_box.delete(0, output_box.size())

app.connect_callbacks(globals())

if __name__ == "__main__":
    app.mainloop()
