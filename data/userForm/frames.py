import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

from data.entryInfo import EntryInfo
from data.constants import *


def step_all_photos_window(user_form):
    user_form.entry_info = EntryInfo()
    user_form.entry_info.program_type = ALL_IMAGES
    user_form.entry_info.data_from_step = True

    user_form.clear_frame(user_form.root)
    border = ttk.LabelFrame(user_form.root, border=0, width=user_form.screen_width, height=user_form.screen_height)

    user_form.configue_borders(border, 6, 3)

    _add_credentials(user_form=user_form, master=border, first_row=0)

    _add_excel(user_form=user_form, master=border, row=2, text="Select Excel with product list")

    _add_images_references(user_form=user_form, master=border, row=3)

    _add_pdfs_references(user_form=user_form, master=border, row=4)

    _add_number_of_elements(user_form=user_form, master=border, row=5)

    _add_gather_data_type(user_form=user_form, master=border, row=6)

    _add_menu(user_form=user_form, master=border, row=7)

    border.pack(fill='both', expand=True)


def local_all_photos_window(user_form):
    user_form.entry_info = EntryInfo()
    user_form.entry_info.program_type = ALL_IMAGES

    user_form.clear_frame(user_form.root)
    border = ttk.LabelFrame(user_form.root, border=0, width=user_form.screen_width, height=user_form.screen_height)

    user_form.configue_borders(border, 3, 3)

    _add_folder_with_photos(user_form=user_form, master=border, row=0)

    _add_excel(user_form=user_form, master=border, row=1, text="Select Excel Path")

    _add_number_of_elements(user_form=user_form, master=border, row=2)

    _add_menu(user_form=user_form, master=border, row=3)

    border.pack(fill='both', expand=True)


def compare_window(user_form):
    user_form.entry_info = EntryInfo()
    user_form.entry_info.program_type = COMPARE

    user_form.clear_frame(user_form.root)
    border = ttk.LabelFrame(user_form.root, border=0, width=user_form.screen_width, height=user_form.screen_height)

    user_form.configue_borders(border, 3, 3)

    _add_folder_with_photos(user_form=user_form, master=border, row=0)

    _add_excel(user_form=user_form, master=border, row=1, text="Select Excel Path")

    _compare_checkbutons(user_form, border, 2)

    _add_menu(user_form=user_form, master=border, row=3, back_to_menu=True)

    border.pack(fill='both', expand=True)


def _compare_checkbutons(user_form, master, row):
    check_buttons_label = ttk.LabelFrame(master)

    # ##################### CheckButtons ##############################
    user_form.entry_info.live_preview = tk.BooleanVar()
    live_preview_check_box = tk.Checkbutton(check_buttons_label, text="Live preview",
                                            variable=user_form.entry_info.live_preview,
                                            onvalue=True,
                                            offvalue=False, anchor='w')
    live_preview_check_box.pack(fill='both')

    user_form.entry_info.resize_photo = tk.BooleanVar()
    resize_photo_check_box = tk.Checkbutton(check_buttons_label, text="Resize photos to 200x200",
                                            variable=user_form.entry_info.resize_photo,
                                            onvalue=True, offvalue=False, anchor='w')
    resize_photo_check_box.pack(fill='both')

    check_buttons_label.grid(row=row, column=0, sticky=tk.NSEW)


def _add_credentials(user_form, master, first_row):
    login_label = tk.Label(master, text="Login", relief="groove")
    login_label.grid(row=first_row, column=0, sticky=tk.NSEW, ipadx=user_form.buttons_width)
    user_form.entry_info.step_login = tk.Entry(master)
    user_form.entry_info.step_login.grid(row=first_row, column=1, columnspan=3, sticky=tk.NSEW)

    password_label = tk.Label(master, text="Password", relief="groove")
    password_label.grid(row=first_row + 1, column=0, sticky=tk.NSEW, ipadx=user_form.buttons_width)
    user_form.entry_info.step_password = tk.Entry(master, show="*")
    user_form.entry_info.step_password.grid(row=first_row + 1, column=1, columnspan=3, sticky=tk.NSEW)


def _add_excel(user_form, master, row, text):
    excel_path_label = tk.Label(master, text="", width=32, relief="groove")
    excel_path_label.grid(row=row, column=1, columnspan=3, sticky=tk.NSEW, ipadx=user_form.buttons_width)
    excel_button = tk.Button(master, text=text,
                             command=lambda: user_form.select_excel_path(excel_path_label, EXCEL_PATH))
    excel_button.grid(row=row, column=0, sticky=tk.NSEW)


def _add_images_references(user_form, master, row):
    step_references_label = tk.Label(master, text="", width=32, relief="groove")
    step_references_label.grid(row=row, column=1, columnspan=3, sticky=tk.NSEW)
    references_button = tk.Button(master, text="Select Images References",
                                  command=lambda: user_form.references_window(step_references_label, 'image_ids'))
    references_button.grid(row=row, column=0, ipadx=user_form.buttons_width, sticky=tk.NSEW)


def _add_pdfs_references(user_form, master, row):
    step_pdfs_label = tk.Label(master, text="", width=32, relief="groove")
    step_pdfs_label.grid(row=row, column=1, columnspan=3, sticky=tk.NSEW)
    pdfs_button = tk.Button(master, text="Select Documents References",
                            command=lambda: user_form.references_window(step_pdfs_label, 'pdf_ids'))
    pdfs_button.grid(row=row, column=0, ipadx=user_form.buttons_width, sticky=tk.NSEW)


def _add_number_of_elements(user_form, master, row):
    tk.Label(master, text="Number of elements in show all: ").grid(row=row, column=0, sticky=tk.NSEW)
    user_form.entry_info.elements_on_screen = tk.Entry(master, width=2, justify='center')
    user_form.entry_info.elements_on_screen.insert(0, "3")
    user_form.entry_info.elements_on_screen.grid(row=row, column=1, sticky=tk.W)


def _add_gather_data_type(user_form, master, row):
    tk.Label(master, text="Gather all images before start: ").grid(row=row, column=0, sticky=tk.NSEW)
    on_img = ImageTk.PhotoImage(Image.open('data/images/on.png'))
    off_img = ImageTk.PhotoImage(Image.open('data/images/off.png'))

    def _switch_on_off_button():
        if user_form.entry_info.gather_data_before_start:
            button_on_off.config(image=off_img)
            user_form.entry_info.gather_data_before_start = False
        else:
            button_on_off.config(image=on_img)
            user_form.entry_info.gather_data_before_start = True

    button_on_off = tk.Button(master, image=on_img,
                              command=_switch_on_off_button, bd=0)

    button_on_off.grid(row=6, column=1, sticky=tk.W)


def _add_menu(user_form, master, row, back_to_menu=False):
    menu_frame = ttk.LabelFrame(master)
    user_form.menu_label(menu_frame, back_to_menu=back_to_menu)
    menu_frame.grid(row=row, column=0, columnspan=3, sticky=tk.NSEW)


def _add_folder_with_photos(user_form, master, row):
    folder_path_label = tk.Label(master, text="", width=32, relief="groove")
    folder_path_label.grid(row=row, column=1, columnspan=3, sticky=tk.NSEW)

    folder_button = tk.Button(master, text="Select folder Path",
                              command=lambda: user_form.select_folder_path(folder_path_label, PHOTO_PATH))
    folder_button.grid(row=row, column=0, ipadx=user_form.buttons_width, sticky=tk.NSEW)
