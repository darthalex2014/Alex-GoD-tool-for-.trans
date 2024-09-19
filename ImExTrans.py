import tkinter as tk
from tkinter import filedialog, ttk
import json

class TransExtractor:
    def __init__(self, master):
        self.master = master
        master.title("Alex(GoD) tool for .trans")

        # --- Темная тема для всего окна ---
        master.configure(background='#333')
        self.style = ttk.Style()
        self.style.theme_use('clam')  # Или другая темная тема, например 'alt'
        self.style.configure('.', background='#333', foreground='white')
        self.style.configure('TLabelframe', background='#333', foreground='white')
        self.style.configure('TLabelframe.Label', background='#333', foreground='white')
        self.style.configure('TButton', background='#555', foreground='white')
        self.style.map('TButton', background=[('active', '#777')])  # Изменение цвета кнопки при наведении
        self.style.configure('TEntry', fieldbackground='#444', foreground='white')  # Темный фон и белый текст для полей ввода

        # --- Извлечение строк ---
        self.trans_file_frame = ttk.LabelFrame(master, text=".trans File / .trans Файл / .trans 文件")
        self.trans_file_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        self.trans_file_path = tk.StringVar()
        self.trans_file_label = ttk.Label(self.trans_file_frame, text="Path:")
        self.trans_file_label.grid(row=0, column=0, padx=5, pady=5)
        self.trans_file_entry = ttk.Entry(self.trans_file_frame, textvariable=self.trans_file_path, width=50)
        self.trans_file_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_trans_button = ttk.Button(self.trans_file_frame, text="Browse", command=self.browse_trans_file)
        self.browse_trans_button.grid(row=0, column=2, padx=5, pady=5)

        self.column_var = tk.IntVar(value=1)  # По умолчанию выбран 1 столбец (Original Text)
        self.column_frame = ttk.LabelFrame(master, text="Column to Extract / Столбец для извлечения / 要提取的列")
        self.column_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        for i in range(1, 6):
            radio = ttk.Radiobutton(self.column_frame, text=f"{i}", variable=self.column_var, value=i)
            radio.grid(row=0, column=i - 1, padx=5, pady=5)

        # --- Кнопки ---
        self.preview_button = ttk.Button(master, text="Preview / Предпросмотр / 预览", command=self.preview_trans_file)
        self.preview_button.grid(row=2, column=0, columnspan=3, pady=5)  # Перемещено выше

        self.select_files_button = ttk.Button(master, text="Select Files to Extract / Выбрать файлы для извлечения / 选择要提取的文件", command=self.select_files_to_extract)
        self.select_files_button.grid(row=3, column=0, columnspan=3, pady=5)  # Перемещено выше

        self.extract_button = ttk.Button(master, text="Extract All Strings / Извлечь все строки из файла / 提取文件中的所有字符串", command=self.extract_strings)
        self.extract_button.grid(row=4, column=0, columnspan=3, pady=10)

        # --- Добавление строк ---
        self.output_file_frame = ttk.LabelFrame(master, text="Output File / Выходной файл / 输出文件")
        self.output_file_frame.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        self.output_file_path = tk.StringVar()
        self.output_file_label = ttk.Label(self.output_file_frame, text="Path:")
        self.output_file_label.grid(row=0, column=0, padx=5, pady=5)
        self.output_file_entry = ttk.Entry(self.output_file_frame, textvariable=self.output_file_path, width=50)
        self.output_file_entry.grid(row=0, column=1, padx=5, pady=5)
        self.browse_output_button = ttk.Button(self.output_file_frame, text="Browse", command=self.browse_output_file)
        self.browse_output_button.grid(row=0, column=2, padx=5, pady=5)

        self.column_add_var = tk.IntVar(value=2)  # По умолчанию выбран 2 столбец (Initial)
        self.column_add_frame = ttk.LabelFrame(master, text="Column to Add / Столбец для добавления / 要添加的列")
        self.column_add_frame.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="ew")

        for i in range(1, 6):
            radio = ttk.Radiobutton(self.column_add_frame, text=f"{i}", variable=self.column_add_var, value=i)
            radio.grid(row=0, column=i - 1, padx=5, pady=5)

        self.add_button = ttk.Button(master, text="Add Strings / Добавить строки / 添加字符串", command=self.add_strings)
        self.add_button.grid(row=7, column=0, columnspan=3, pady=10)

        self.status_label = ttk.Label(master, text="")
        self.status_label.grid(row=8, column=0, columnspan=3, pady=5)

        # Listbox для выбора файлов
        self.listbox = None

    def browse_trans_file(self):
        filename = filedialog.askopenfilename(initialdir=".", title="Select .trans file",
                                              filetypes=((".trans files", "*.trans"), ("All files", "*.*")))
        self.trans_file_path.set(filename)

    def browse_output_file(self):
        filename = filedialog.askopenfilename(initialdir=".", title="Select output file",
                                              filetypes=((".txt files", "*.txt"), ("All files", "*.*")))
        self.output_file_path.set(filename)

    def extract_strings(self, selected_files=None):  # Принимаем список выбранных файлов
        try:
            with open(self.trans_file_path.get(), 'r', encoding='utf-8') as f:
                data = json.load(f)

            output_strings = []

            # Проходим по всем ключам в data['project']['files']
            for file_key in data['project']['files']:
                # Проверяем, выбран ли текущий файл
                if selected_files and file_key not in selected_files:
                    continue

                file_strings = []  # Список строк для текущего файла

                for i, cell_data in enumerate(data['project']['files'][file_key]['data']):
                    selected_index = self.column_var.get() - 1  # Индекс выбранного столбца (0-based)

                    if selected_index < len(cell_data) and cell_data[selected_index] is not None:
                        # Сохраняем строки с переносами как есть
                        file_strings.append(cell_data[selected_index].replace('\n', '\\n'))

                # Добавляем имя файла и строки из него в общий список
                if file_strings:
                    output_strings.append(f"File: {file_key}\n")
                    output_strings.extend([f"{s}\n" for s in file_strings])

            with open("output_strings.txt", 'w', encoding='utf-8') as outfile:
                outfile.writelines(output_strings)

            self.status_label.config(text="Strings successfully extracted to output_strings.txt")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")

    def add_strings(self):
        try:
            with open(self.trans_file_path.get(), 'r', encoding='utf-8') as f:
                trans_data = json.load(f)

            with open(self.output_file_path.get(), 'r', encoding='utf-8') as f:
                output_strings = f.readlines()

            current_file_key = None
            string_index = 0
            selected_column = self.column_add_var.get() - 1  # Индекс выбранного столбца (0-based)

            for line in output_strings:
                line = line.strip()
                if line.startswith("File:"):
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
            new_filename = self.trans_file_path.get()[:-6] + "_modified.trans"
            with open(new_filename, 'w', encoding='utf-8') as f:
                json.dump(trans_data, f, indent=4)

            self.status_label.config(text=f"Strings added. File saved as {new_filename}")
        except Exception as e:
            self.status_label.config(text=f"Error: {e}")

    def preview_trans_file(self):
        try:
            with open(self.trans_file_path.get(), 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Создаем новое окно для предпросмотра
            preview_window = tk.Toplevel(self.master)
            preview_window.title(".trans File Preview")
            preview_window.configure(background='#333')  # Темный фон для окна

            # Создаем Frame для Treeview и Scrollbar
            tree_frame = ttk.Frame(preview_window)
            tree_frame.pack(fill=tk.BOTH, expand=True)

            # Создаем Treeview widget
            tree = ttk.Treeview(tree_frame, columns=("Original Text", "Initial", "Machine translation", "Better translation", "Best translation"),
                                show="headings")
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            # Создаем вертикальный Scrollbar
            scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            # Привязываем Treeview к Scrollbar
            tree.configure(yscrollcommand=scrollbar.set)

            # Настраиваем заголовки столбцов
            for col in tree["columns"]:
                tree.heading(col, text=col)

            # Заполняем Treeview данными из .trans файла
            for file_key in data['project']['files']:
                for row in data['project']['files'][file_key]['data']:
                    tree.insert("", tk.END, values=row)

            # --- Темная тема для Treeview ---
            style = ttk.Style(preview_window)  # Создаем стиль для нового окна
            style.configure("Treeview", background="#444", foreground="white", fieldbackground="#444")
            style.map("Treeview", background=[('selected', '#555')])  # Изменение цвета выбранной строки

        except Exception as e:
            self.status_label.config(text=f"Error: {e}")

    def select_files_to_extract(self):
        try:
            with open(self.trans_file_path.get(), 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Создаем новое окно для выбора файлов
            select_window = tk.Toplevel(self.master)
            select_window.title("Select Files to Extract / Выбор файлов для извлечения / 选择要提取的文件")
            select_window.configure(background='#333')  # Темный фон для окна

            # Создаем Frame для кнопок
            buttons_frame = ttk.Frame(select_window)
            buttons_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

            # Создаем список файлов
            self.listbox = tk.Listbox(select_window, selectmode=tk.MULTIPLE, background="#444", foreground="white")
            self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

            # Заполняем список файлами из .trans файла
            for file_key in data['project']['files']:
                self.listbox.insert(tk.END, file_key)

            # Функция для обработки выбранных файлов
            def process_selection():
                selected_files = [self.listbox.get(i) for i in self.listbox.curselection()]
                self.extract_strings(selected_files)  # Вызываем extract_strings с выбранными файлами
                select_window.destroy()  # Закрываем окно после вызова extract_strings

            # Кнопка "Select All / Выбрать все / 全选"
            def select_all():
                self.listbox.select_set(0, tk.END)

            # Кнопка "Deselect All / Снять выделение / 取消全选"
            def deselect_all():
                self.listbox.selection_clear(0, tk.END)

            # Кнопка "Except Plugins / Кроме плагинов / 除插件外"
            def select_except_plugins():
                deselect_all()
                for i, file_key in enumerate(data['project']['files']):
                    if not file_key.startswith("js/"):
                        self.listbox.select_set(i)

            # Кнопка "All Maps / Все карты / 所有地图"
            def select_all_maps():
                deselect_all()
                for i, file_key in enumerate(data['project']['files']):
                    if "/Map" in file_key and file_key.endswith(".json"):  # Проверяем наличие "/Map" и расширение .json
                        self.listbox.select_set(i)

            select_all_button = ttk.Button(buttons_frame, text="Select All / Выбрать все / 全选", command=select_all,
                                          width=30)
            select_all_button.pack(side=tk.LEFT, padx=5)

            deselect_all_button = ttk.Button(buttons_frame, text="Deselect All / Снять выделение / 取消全选", command=deselect_all,
                                            width=30)
            deselect_all_button.pack(side=tk.LEFT, padx=5)

            select_except_plugins_button = ttk.Button(buttons_frame, text="Except Plugins / Кроме плагинов / 除插件外",
                                                      command=select_except_plugins, width=30)
            select_except_plugins_button.pack(side=tk.LEFT, padx=5)

            select_all_maps_button = ttk.Button(buttons_frame, text="All Maps / Все карты / 所有地图", command=select_all_maps,
                                                width=30)
            select_all_maps_button.pack(side=tk.LEFT, padx=5)

            # Кнопка "OK"
            ok_button = ttk.Button(select_window, text="Extract Selected Files / Извлечь выделенные файлы / 提取所选文件", command=process_selection)
            ok_button.pack(pady=10)

        except Exception as e:
            self.status_label.config(text=f"Error: {e}")

root = tk.Tk()
app = TransExtractor(root)
root.mainloop()
