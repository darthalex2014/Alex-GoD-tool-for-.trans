import tkinter as tk
from tkinter import filedialog, ttk
import json

# --- Функции ---

def browse_trans_file():
    filename = filedialog.askopenfilename(initialdir=".", title="Выберите .trans файл", filetypes=((".trans файлы", "*.trans"), ("Все файлы", "*.*")))
    trans_file_path.set(filename)

def browse_output_file():
    filename = filedialog.askopenfilename(initialdir=".", title="Выберите output файл", filetypes=((".txt файлы", "*.txt"), ("Все файлы", "*.*")))
    output_file_path.set(filename)

def extract_strings():
    try:
        with open(trans_file_path.get(), 'r', encoding='utf-8') as f:
            data = json.load(f)

        output_strings = []

        # Проходим по всем ключам в data['project']['files']
        for file_key in data['project']['files']:
            file_strings = []  # Список строк для текущего файла

            for i, cell_data in enumerate(data['project']['files'][file_key]['data']):
                selected_index = column_var.get() - 1  # Индекс выбранного столбца (0-based)

                if selected_index < len(cell_data) and cell_data[selected_index] is not None:
                    # Сохраняем строки с переносами как есть
                    file_strings.append(cell_data[selected_index].replace('\n', '\\n'))

            # Добавляем имя файла и строки из него в общий список
            if file_strings:
                output_strings.append(f"Файл: {file_key}\n")
                output_strings.extend([f"{s}\n" for s in file_strings])

        with open("output_strings.txt", 'w', encoding='utf-8') as outfile:
            outfile.writelines(output_strings)

        status_label.config(text="Строки успешно извлечены в output_strings.txt")
    except Exception as e:
        status_label.config(text=f"Ошибка: {e}")


def add_strings():
    try:
        with open(trans_file_path.get(), 'r', encoding='utf-8') as f:
            trans_data = json.load(f)

        with open(output_file_path.get(), 'r', encoding='utf-8') as f:
            output_strings = f.readlines()

        current_file_key = None
        string_index = 0
        selected_column = column_add_var.get() - 1  # Индекс выбранного столбца (0-based)

        for line in output_strings:
            line = line.strip()
            if line.startswith("Файл:"):
                current_file_key = line[6:]  # Получаем имя файла
                string_index = 0
            elif current_file_key is not None:
                if current_file_key in trans_data['project']['files']:
                    # Добавляем строку в выбранный столбец, заменяя \n на переносы строк
                    data_list = trans_data['project']['files'][current_file_key]['data'][string_index]
                    while len(data_list) <= selected_column:
                        data_list.append(None)
                    data_list[selected_column] = line.replace('\\n', '\n')
                    string_index += 1

        # Сохраняем измененный .trans файл под новым именем
        new_filename = trans_file_path.get()[:-6] + "_modified.trans"
        with open(new_filename, 'w', encoding='utf-8') as f:
            json.dump(trans_data, f, indent=4)

        status_label.config(text=f"Строки добавлены. Файл сохранен как {new_filename}")
    except Exception as e:
        status_label.config(text=f"Ошибка: {e}")

# --- GUI ---

root = tk.Tk()
root.title("Alex(GoD) tool for .trans")

# --- Темная тема для всего окна ---
root.configure(background='#333')
style = ttk.Style()
style.theme_use('clam')  # Или другая темная тема, например 'alt'
style.configure('.', background='#333', foreground='white')
style.configure('TLabelframe', background='#333', foreground='white')
style.configure('TLabelframe.Label', background='#333', foreground='white')
style.configure('TButton', background='#555', foreground='white')
style.map('TButton', background=[('active', '#777')])  # Изменение цвета кнопки при наведении
style.configure('TEntry', fieldbackground='#444', foreground='white')  # Темный фон и белый текст для полей ввода

# --- Извлечение строк ---
trans_file_frame = ttk.LabelFrame(root, text=".trans File / .trans Файл / .trans 文件")
trans_file_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

trans_file_path = tk.StringVar()
trans_file_label = ttk.Label(trans_file_frame, text="Path:")
trans_file_label.grid(row=0, column=0, padx=5, pady=5)
trans_file_entry = ttk.Entry(trans_file_frame, textvariable=trans_file_path, width=50)
trans_file_entry.grid(row=0, column=1, padx=5, pady=5)
browse_trans_button = ttk.Button(trans_file_frame, text="Browse", command=browse_trans_file)
browse_trans_button.grid(row=0, column=2, padx=5, pady=5)

column_var = tk.IntVar(value=1) # По умолчанию выбран 1 столбец (Original Text)
column_frame = ttk.LabelFrame(root, text="Column to Extract / Столбец для извлечения / 要提取的列")
column_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

for i in range(1, 6):
    radio = ttk.Radiobutton(column_frame, text=f"{i}", variable=column_var, value=i)
    radio.grid(row=0, column=i-1, padx=5, pady=5)

extract_button = ttk.Button(root, text="Extract Strings / Извлечь строки / 提取字符串", command=extract_strings)
extract_button.grid(row=2, column=0, columnspan=3, pady=10)

# --- Добавление строк ---
output_file_frame = ttk.LabelFrame(root, text="Output File / Выходной файл / 输出文件")
output_file_frame.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

output_file_path = tk.StringVar()
output_file_label = ttk.Label(output_file_frame, text="Path:")
output_file_label.grid(row=0, column=0, padx=5, pady=5)
output_file_entry = ttk.Entry(output_file_frame, textvariable=output_file_path, width=50)
output_file_entry.grid(row=0, column=1, padx=5, pady=5)
browse_output_button = ttk.Button(output_file_frame, text="Browse", command=browse_output_file)
browse_output_button.grid(row=0, column=2, padx=5, pady=5)

column_add_var = tk.IntVar(value=2) # По умолчанию выбран 2 столбец (Initial)
column_add_frame = ttk.LabelFrame(root, text="Column to Add / Столбец для добавления / 要添加的列")
column_add_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

for i in range(1, 6):
    radio = ttk.Radiobutton(column_add_frame, text=f"{i}", variable=column_add_var, value=i)
    radio.grid(row=0, column=i-1, padx=5, pady=5)

add_button = ttk.Button(root, text="Add Strings / Добавить строки / 添加字符串", command=add_strings)
add_button.grid(row=5, column=0, columnspan=3, pady=10)

status_label = ttk.Label(root, text="")
status_label.grid(row=6, column=0, columnspan=3, pady=5)

# --- Темная тема ---
style = ttk.Style()
style.theme_use('clam')  # Или другая темная тема, например 'alt'
style.configure('.', background='#333', foreground='white')
style.configure('TLabelframe', background='#333', foreground='white')
style.configure('TLabelframe.Label', background='#333', foreground='white')

root.mainloop()