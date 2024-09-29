import tkinter as tk
from tkinter import ttk
from tkinter import font
import tkinter as tk
from Converter import Converter
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter.messagebox import showerror, showwarning, showinfo
 


def get_selected():
    return [list_box.get(idx) for idx in list_box.curselection()]

def convert_image():
    smiles_string : str = entry_label.get() 
    if smiles_string.strip() == "":
        selected_values_list = get_selected()
        if(len(selected_values_list) != 1):
            showinfo(message="Choose 1 formula")
            return
        else:
            smiles_string = selected_values_list[0]
    
    try:
        converter = Converter()
        image = converter.convert(smiles_string, 600, 600)
        photo = ImageTk.PhotoImage(image)
        photo_label.config(image=photo)
        photo_label.image = photo 
    except Exception:
        showerror(message="Convert error")

def copy_to_entry():
    try:
        clipboard_text = entry_label.clipboard_get()
        entry_label.delete(0, "end")
        entry_label.insert(0, clipboard_text)
    except Exception as e:
        tk.show
        showerror(message="Error with clipboard")

def load_from_file():
    dir_name = filedialog.askopenfile()
    with open(dir_name.name, "r") as file:
        for line in file.readlines():
            list_box.insert("end", line)


# Создаем главное окно
root = tk.Tk()
root.title("title")
root.geometry("1600x800+0+0")

# Настройки шрифтов
default_font = font.Font(family='Arial', size=12)
button_font = font.Font(family='Arial', size=12, weight='bold')

# Переменные
entry_text = tk.StringVar()
error_text_var = tk.StringVar()

# Создаем фреймы для компоновки
top_frame = tk.Frame(root, bg='red')
entry_frame = tk.Frame(top_frame, bg="yellow")
button_frame = tk.Frame(top_frame, bg="green")

central_frame = tk.Frame(root, bg="magenta", height=400)
photo_frame = tk.Frame(central_frame, bg="black")
listbox_frame = tk.Frame(central_frame, bg='blue')


# Размещаем фреймы
top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
entry_frame.pack(side=tk.LEFT)
button_frame.pack(side=tk.LEFT, padx=20)

central_frame.pack(side=tk.TOP,fill=tk.Y, fill=tk.X,padx=10, pady=10)
listbox_frame.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.Y)
photo_frame.pack(side=tk.RIGHT, padx=20, pady=20)

# Label "SMILE:"
label_1 = ttk.Label(entry_frame, text="SMILE:", width=6, font=default_font)
label_1.pack(side=tk.LEFT, padx=10, pady=5)

# Entry для ввода
entry_label = ttk.Entry(entry_frame, textvariable=entry_text, cursor="ibeam", width=20, font=default_font)
entry_label.pack(side=tk.LEFT, padx=5, pady=5)

# Кнопка "take picture"
proceed = ttk.Button(button_frame, text="take picture", command=convert_image, width=50)
proceed.pack(side=tk.TOP, padx=5, pady=5)

# Кнопка "Ctrl+V"
copyToButton = ttk.Button(button_frame, text="Ctrl+V", command=copy_to_entry, width=50)
copyToButton.pack(side=tk.TOP, padx=5, pady=5)

# Label для фото
photo_label = ttk.Label(photo_frame, background="#dce3e6", text="", width=60)
photo_label.pack(side=tk.TOP, padx=5, pady=5)

# Кнопка "load from file"
loadfilebutton = ttk.Button(listbox_frame, text="load from file", command=load_from_file, width=30)
loadfilebutton.pack(side=tk.TOP, padx=5, pady=5)

# Listbox
list_box = tk.Listbox(listbox_frame, activestyle="dotbox", selectmode="extended", width=50)
list_box.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.Y)

# Scrollbar для Listbox
formula_scroll = ttk.Scrollbar(listbox_frame, command=list_box.yview)
formula_scroll.pack(side=tk.LEFT, fill=tk.Y)

# Связываем Scrollbar с Listbox
list_box.config(yscrollcommand=formula_scroll.set)


####secondlistbox
# Listbox
list_box2 = tk.Listbox(listbox_frame, activestyle="dotbox", selectmode="extended", width=50)
list_box.pack(side=tk.RIGHT, padx=5, pady=5, fill=tk.Y)

# Scrollbar для Listbox
formula_scroll2 = ttk.Scrollbar(listbox_frame, command=list_box2.yview)
formula_scroll2.pack(side=tk.LEFT, fill=tk.Y)

# Связываем Scrollbar с Listbox
list_box2.config(yscrollcommand=formula_scroll2.set)


# Запускаем цикл событий Tkinter
root.mainloop()
