from formation import AppBuilder
import tkinter as tk
from Converter import Converter
from Predictor import Predictor
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter.messagebox import showerror, showwarning, showinfo
 

app = AppBuilder(path="core\\resources\\main.xml")

#entities
window = app.tk_1
entry = app.entry_label
error_label = app.error_label
photo_label = app.photo_label
list_box = app.list_box
output_box = app.output_box
load_file_button = app.loadfilebutton
picture_name_label = app.picture_name

app.refresh.set('\U0001f5d8')

def get_selected():
    return [list_box.get(idx) for idx in list_box.curselection()]

def convert_image():
    smiles_string = app.entrytext.get() 
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
        app.labeltext.set(smiles_string)
    except Exception:
        showerror(message="Convert error")

def copy_to_entry():
    try:
        clipboard_text = entry.clipboard_get()
        entry.delete(0, "end")
        entry.insert(0, clipboard_text)
    except Exception as e:
        tk.show
        showerror(message="Error with clipboard")

def load_from_file():
    dir_name = filedialog.askopenfile()
    with open(dir_name.name, "r") as file:
        for line in file.readlines():
            list_box.insert("end", line)

def save_to_csv():
    pass

def make_prediction():
    selected_list = get_selected()
    predictor = Predictor(lambda x: (1, 2)) 
    answer = predictor.predict_for_each(selected_list)
    #print(answer)
    for key_smile in answer.keys():
        output_box.insert("end", key_smile)
        output_box.insert("end", f"name1: {answer[key_smile][0]}, name2: {answer[key_smile][1]}")
    pass

def refresh_list():
    output_box.delete(0, output_box.size())
app.connect_callbacks(globals())

if __name__ == "__main__":
    app.mainloop()