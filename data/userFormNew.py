import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from entryInfo import EntryInfo
from tkinter.filedialog import askdirectory
import photoCompareObj
from constants import *
from PIL import ImageTk, Image
import csv


TAG_TO_DELETE_KEY: str = 'To delete'
BME_CAT_DICT_KEY: str = 'BME_CAT'
EXCEL_DICT_KEY: str = 'Excel'
PROGRAM_DELETE_TAG: str = 'Delete'
PROGRAM_MFPNR: str = 'MFPNR'
PROGRAM_BME_TO_EXCEL: str = 'BME2EXCEL'



class UserForm:
    def __init__(self):
        self.run: bool = False
        self.screen_width = 400
        self.screen_height = 200
        self.root = tk.Tk()
        self.root.iconbitmap('data/images/icon.ico')
        self.root.geometry(f'{self.screen_width}x{self.screen_height}')
        self.root.configure(background='#f5f6f7')
        self.root.resizable(True, True)
        self.root.title("PhotoCompare")
        self.buttons_width = self.screen_width/20
        self.buttons_height = ""
        self.entry_info: EntryInfo()

        self.open_menu()

    def open_menu(self):
        clear_frame(self.root)

        compare_button = ttk.Button(self.root, text="Compare", command=lambda: self.compare_window())
        compare_button.pack(fill='both', expand=True)

        all_photos_button = ttk.Button(self.root, text="Show all Photos", command=lambda: self.all_photos_window())
        all_photos_button.pack(fill='both', expand=True)

        exit_button = ttk.Button(self.root, text="Exit", command=lambda: self.root.destroy())
        exit_button.pack(fill='both', expand=True)

    def all_photos_window(self):
        clear_frame(self.root)

        compare_button = ttk.Button(self.root, text="Local", command=lambda: self.local_all_photos_window())
        compare_button.pack(fill='both', expand=True)

        all_photos_button = ttk.Button(self.root, text="From STEP", command=lambda: self.step_all_photos_window())
        all_photos_button.pack(fill='both', expand=True)

        all_photos_button = ttk.Button(self.root, text="Back", command=lambda: self.open_menu())
        all_photos_button.pack(fill='both', expand=True, side=tk.LEFT)

        exit_button = ttk.Button(self.root, text="Exit", command=lambda: self.root.destroy())
        exit_button.pack(fill='both', expand=True, side=tk.RIGHT)

    def local_all_photos_window(self):
        self.entry_info = EntryInfo()
        self.entry_info.program_type = ALL_IMAGES

        clear_frame(self.root)
        border = ttk.LabelFrame(self.root, border=0, width=self.screen_width, height=self.screen_height)

        configue_borders(border, 3, 3)

        folder_path_label = tk.Label(border, text="", width=32, relief="groove")
        folder_path_label.grid(row=0, column=1, columnspan=3, sticky=tk.NSEW)

        folder_button = tk.Button(border, text="Select folder Path",
                                  command=lambda: self.select_folder_path(folder_path_label, PHOTO_PATH))
        folder_button.grid(row=0, column=0, ipadx=self.buttons_width, sticky=tk.NSEW)

        excel_path_label = tk.Label(border, text="", width=32, relief="groove")
        excel_path_label.grid(row=1, column=1, columnspan=3, sticky=tk.NSEW)

        excel_button = tk.Button(border, text="Select Excel Path",
                                 command=lambda: self.select_excel_path(excel_path_label, EXCEL_PATH))
        excel_button.grid(row=1, column=0, ipadx=self.buttons_width, sticky=tk.NSEW)

        tk.Label(border, text="Number of elements in show all: ").grid(row=2, column=0, sticky=tk.NSEW)
        self.entry_info.elements_on_screen = tk.Entry(border, width=2, justify='center')
        self.entry_info.elements_on_screen.insert(0, "3")
        self.entry_info.elements_on_screen.grid(row=2, column=1, sticky=tk.W)

        menu_frame = ttk.LabelFrame(border)
        self.menu_label(menu_frame, back_to_menu=False)
        menu_frame.grid(row=3, column=0, columnspan=3, sticky=tk.NSEW)

        border.pack(fill='both', expand=True)

    def step_all_photos_window(self):
        self.entry_info = EntryInfo()
        self.entry_info.program_type = ALL_IMAGES
        self.entry_info.data_from_step = True

        clear_frame(self.root)
        border = ttk.LabelFrame(self.root, border=0, width=self.screen_width, height=self.screen_height)

        configue_borders(border, 3, 3)

        excel_path_label = tk.Label(border, text="", width=32, relief="groove")
        excel_path_label.grid(row=0, column=1, columnspan=3, sticky=tk.NSEW)
        excel_button = tk.Button(border, text="Select Excel with product list",
                                command=lambda: self.select_excel_path(excel_path_label, EXCEL_PATH))
        excel_button.grid(row=0, column=0, ipadx=self.buttons_width, sticky=tk.NSEW)

        step_references_label = tk.Label(border, text="", width=32, relief="groove")
        step_references_label.grid(row=1, column=1, columnspan=3, sticky=tk.NSEW)
        references_button = tk.Button(border, text="Select references",
                                      command=lambda: self.references_window(step_references_label))
        references_button.grid(row=1, column=0, ipadx=self.buttons_width, sticky=tk.NSEW)

        tk.Label(border, text="Number of elements in show all: ").grid(row=2, column=0, sticky=tk.NSEW)
        self.entry_info.elements_on_screen = tk.Entry(border, width=2, justify='center')
        self.entry_info.elements_on_screen.insert(0, "3")
        self.entry_info.elements_on_screen.grid(row=2, column=1, sticky=tk.W)

        tk.Label(border, text="Gather all images before start: ").grid(row=3, column=0, sticky=tk.NSEW)
        on_img = ImageTk.PhotoImage(Image.open('data/images/on.png'))
        off_img = ImageTk.PhotoImage(Image.open('data/images/off.png'))

        def switch_on_off_button():
            if self.entry_info.gather_data_before_start:
                button_on_off.config(image=off_img)
                self.entry_info.gather_data_before_start = False
            else:
                button_on_off.config(image=on_img)
                self.entry_info.gather_data_before_start = True

        button_on_off = tk.Button(border, image=on_img,
                                command= switch_on_off_button, bd=0)

        button_on_off.grid(row=3, column=1, sticky=tk.W)

        menu_frame = ttk.LabelFrame(border)
        self.menu_label(menu_frame, back_to_menu=False)
        menu_frame.grid(row=4, column=0, columnspan=3, sticky=tk.NSEW)

        border.pack(fill='both', expand=True)


    def references_window(self, step_references_label):
        master = tk.Toplevel()
        # ##################### CheckButtons ##############################

        # references_list = ['Product Image', 'Product Image further', 'BMEcat_MIME_INFO_safety_data_sheet',
        #                    'BMEcat_MIME_INFO_deep_link_data_sheet', 'BMEcat_MIME_INFO_deep_link_reach_data_sheet',
        #                    'Energy label', 'Circuit Diagram', 'MeasurementDrawing', 'Symbol',
        #                    'BMEcat_MIME_INFO_user_manual', 'Light Distribution Curve', 'EnvironmentImage',
        #                    'MIME_INFO_federation_link', 'BMEcat_MIME_INFO_FDV']
        with open('data/references/image_ids.csv', 'r') as f:
            references_list = csv.reader(f, delimiter=';')
            references_list = list(references_list)[0]


        references_label = tk.Label(master)
        for reference_name in references_list:
            self.entry_info.references_dict[reference_name] = tk.BooleanVar()
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

    def select_reference(self, master, step_references_label):
        step_references_label.configure(background="lightgreen", text="Selected")

        for k, v in self.entry_info.references_dict.items():
            self.entry_info.references_dict[k] = v.get()
        master.destroy()

    def compare_window(self):
        self.entry_info = EntryInfo()
        self.entry_info.program_type = COMPARE

        clear_frame(self.root)
        border = ttk.LabelFrame(self.root, border=0, width=self.screen_width, height=self.screen_height)

        configue_borders(border, 4, 3)

        folder_path_label = tk.Label(border, text="", width=32, relief="groove")
        folder_path_label.grid(row=0, column=1, columnspan=3, sticky=tk.NSEW)

        folder_label = tk.Button(border, text="Select folder Path",
                                 command=lambda: self.select_folder_path(folder_path_label, PHOTO_PATH))
        folder_label.grid(row=0, column=0, ipadx=self.buttons_width, sticky=tk.NSEW)

        excel_path_label = tk.Label(border, text="", width=32, relief="groove")
        excel_path_label.grid(row=1, column=1, columnspan=3, sticky=tk.NSEW)

        excel_label = tk.Button(border, text="Select Excel Path",
                                command=lambda: self.select_excel_path(excel_path_label, EXCEL_PATH))
        excel_label.grid(row=1, column=0, ipadx=self.buttons_width, sticky=tk.NSEW)

        check_buttons_label = ttk.LabelFrame(border)
        self.compare_checkbutons(check_buttons_label)
        check_buttons_label.grid(row=3, column=0, sticky=tk.NSEW)

        menu_frame = ttk.LabelFrame(border)
        self.menu_label(menu_frame)
        menu_frame.grid(row=4, column=0, columnspan=3, sticky=tk.NSEW)

        border.pack(fill='both', expand=True)

    def compare_checkbutons(self, master):

        # ##################### CheckButtons ##############################
        self.entry_info.live_preview = tk.BooleanVar()
        live_preview_check_box = tk.Checkbutton(master, text="Live preview", variable= self.entry_info.live_preview, onvalue=True,
                                                offvalue=False, anchor='w')
        live_preview_check_box.pack(fill='both')

        self.entry_info.resize_photo = tk.BooleanVar()
        resize_photo_check_box = tk.Checkbutton(master, text="Resize photos to 200x200", variable=self.entry_info.resize_photo,
                                                onvalue=True, offvalue=False, anchor='w')
        resize_photo_check_box.pack(fill='both')

        self.entry_info.continue_work = tk.BooleanVar()
        resize_photo_check_box = tk.Checkbutton(master, text="Continue work", variable=self.entry_info.continue_work, onvalue=True,
                                                offvalue=False, anchor='w')
        resize_photo_check_box.pack(fill='both')

    def menu_label(self, menu_frame, back_to_menu=True):
        ttk.Button(menu_frame, text='RUN', command=lambda: self.run_program()).pack(fill='both',
                                                                                         expand=True,
                                                                                         side=tk.LEFT)
        if back_to_menu:
            ttk.Button(menu_frame, text='BACK', command=lambda: self.open_menu()).pack(fill='both',
                                                                                       expand=True,
                                                                                       side=tk.LEFT)
        else:
            ttk.Button(menu_frame, text='BACK', command=lambda: self.all_photos_window()).pack(fill='both',
                                                                                               expand=True,
                                                                                               side=tk.LEFT)

        ttk.Button(menu_frame, text='EXIT', command=lambda: self.root.destroy()).pack(fill='both',
                                                                                      expand=True,
                                                                                      side=tk.LEFT)

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
            self.entry_info.remove_unused_references_from_dict()
            self.entry_info.add_pim_id_list()
        self.open_menu()
        photoCompareObj.main(self.entry_info)
        tk.messagebox.showinfo(title="Photo Compare", message="Finished!")


def configue_borders(border, row_num, col_num):
    for i in range(row_num):
        border.rowconfigure(i, weight=1)
    for j in range(col_num):
        border.columnconfigure(j, weight=1)


def clear_frame(master):
    for widget in master.winfo_children():
        widget.destroy()

def run():
    user_form = UserForm()
    user_form.root.mainloop()



if __name__ == "__main__":
    user_form = UserForm()
    user_form.root.mainloop()
