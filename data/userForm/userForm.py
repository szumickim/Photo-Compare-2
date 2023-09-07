from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import csv

import data.photoCompareObj as photoCompareObj
from frames import *


class UserForm:
    def __init__(self):
        self.run: bool = False
        self.screen_width = 500
        self.screen_height = 400
        self.root = tk.Tk()
        self.root.iconbitmap('data/images/icon.ico')
        self.root.geometry(f'{self.screen_width}x{self.screen_height}')
        self.root.configure(background='#f5f6f7')
        self.root.resizable(True, True)
        self.root.title("PhotoCompare")
        self.buttons_width = self.screen_width/20
        self.buttons_height = ""

        self.entry_info: EntryInfo() = EntryInfo()

        self.open_menu()

    def open_menu(self):
        self.clear_frame(self.root)

        compare_button = ttk.Button(self.root, text="Compare", command=lambda: compare_window(self))
        compare_button.pack(fill='both', expand=True)

        all_photos_button = ttk.Button(self.root, text="Show all Photos", command=lambda: self.all_photos_menu())
        all_photos_button.pack(fill='both', expand=True)

        exit_button = ttk.Button(self.root, text="Exit", command=lambda: self.root.destroy())
        exit_button.pack(fill='both', expand=True)

    def all_photos_menu(self):
        self.clear_frame(self.root)

        compare_button = ttk.Button(self.root, text="Local", command=lambda: local_all_photos_window(self))
        compare_button.pack(fill='both', expand=True)

        all_photos_button = ttk.Button(self.root, text="From STEP", command=lambda: step_all_photos_window(self))
        all_photos_button.pack(fill='both', expand=True)

        all_photos_button = ttk.Button(self.root, text="Back", command=lambda: self.open_menu())
        all_photos_button.pack(fill='both', expand=True, side=tk.LEFT)

        exit_button = ttk.Button(self.root, text="Exit", command=lambda: self.root.destroy())
        exit_button.pack(fill='both', expand=True, side=tk.RIGHT)

    def references_window(self, step_references_label, csv_name):
        master = tk.Toplevel()
        # ##################### CheckButtons ##############################

        with open(f'data/references/{csv_name}.csv', 'r') as f:
            references_list = csv.reader(f, delimiter=';')
            references_list = list(references_list)[0]

        references_label = tk.Label(master)
        for reference_name in references_list:
            if reference_name in self.entry_info.references_dict:
                self.entry_info.references_dict[reference_name] = tk.BooleanVar(value=True) if self.entry_info.references_dict[reference_name] else tk.BooleanVar(value=False)
            else:
                self.entry_info.references_dict[reference_name] = tk.BooleanVar(value=False)

            tk.Checkbutton(references_label, text=reference_name,
                           variable= self.entry_info.references_dict[reference_name],
                           onvalue=True, offvalue=False, anchor='w').pack(fill='both')

        references_label.grid(row=0, column=0, sticky=tk.NSEW)

        options_label = tk.Label(master)
        excel_label = tk.Button(options_label, text="Select",
                                command=lambda: self.select_reference(master, step_references_label))
        excel_label.pack(fill='both', expand=True)

        excel_label = tk.Button(options_label, text="Exit",
                                command=lambda: master.destroy())
        excel_label.pack(fill='both', expand=True)
        options_label.grid(row=0, column=1, sticky=tk.NSEW)

    def menu_label(self, menu_frame, back_to_menu=True):
        ttk.Button(menu_frame, text='RUN', command=lambda: self.run_program()).pack(fill='both',
                                                                                         expand=True,
                                                                                         side=tk.LEFT)
        if back_to_menu:
            ttk.Button(menu_frame, text='BACK', command=lambda: self.open_menu()).pack(fill='both',
                                                                                       expand=True,
                                                                                       side=tk.LEFT)
        else:
            ttk.Button(menu_frame, text='BACK', command=lambda: self.all_photos_menu()).pack(fill='both',
                                                                                               expand=True,
                                                                                               side=tk.LEFT)

        ttk.Button(menu_frame, text='EXIT', command=lambda: self.root.destroy()).pack(fill='both',
                                                                                      expand=True,
                                                                                      side=tk.LEFT)

    def select_reference(self, master, step_references_label):
        step_references_label.configure(background="lightgreen", text="Selected")

        for k, v in self.entry_info.references_dict.items():
            if isinstance(v, tk.BooleanVar):
                self.entry_info.references_dict[k] = v.get()
        master.destroy()

    def select_folder_path(self, label_to_paste, attribute_id):
        folder_path = askdirectory(title="Select A Folder")
        if folder_path:
            label_to_paste['text'] = folder_path[folder_path.rfind('/') + 1:]
            setattr(self.entry_info, attribute_id, folder_path)

    def select_excel_path(self, label_to_paste, attribute_id):
        file_path = askopenfilename(title="Select A File")
        if file_path:
            label_to_paste['text'] = file_path[file_path.rfind('/') + 1:]
            setattr(self.entry_info, attribute_id, file_path)

    def run_program(self):
        if self.entry_info.program_type == COMPARE:
            self.entry_info.change_button_variable_to_boolean()
        elif self.entry_info.program_type == ALL_IMAGES:
            self.entry_info.convert_elements_in_show_all()
        if self.entry_info.data_from_step:
            self.entry_info.step_password = self.entry_info.step_password.get()
            self.entry_info.step_login = self.entry_info.step_login.get()
            self.save_entry_data()
            self.entry_info.remove_unused_references_from_dict()
            self.entry_info.add_pim_id_list()
            self.entry_info.convert_context()

        self.open_menu()
        photoCompareObj.main(self.entry_info)
        tk.messagebox.showinfo(title="Photo Compare", message="Finished!")

    def save_entry_data(self):
        with open(CREDENTIALS_PATH, 'w') as f:
            f.write(f"{self.entry_info.step_login};{self.entry_info.step_password}")

    def configue_borders(self, border, row_num, col_num):
        for i in range(row_num):
            border.rowconfigure(i, weight=1)
        for j in range(col_num):
            border.columnconfigure(j, weight=1)

    def clear_frame(self, master):
        for widget in master.winfo_children():
            widget.destroy()


def run():
    user_form = UserForm()
    user_form.root.mainloop()

