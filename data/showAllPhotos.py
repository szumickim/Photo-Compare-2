from tkinter import ttk
import tkinter as tk
from PIL import Image, ImageTk
from consts import ButtonConst
from progressBar import ClsProgress
from tkinter import messagebox
from dataFromStep import create_product_collection_from_step
from constants import *
from pdf2image import convert_from_path
from pathlib import Path

global next_product_id

def show_all_photos(products_list, photo_path, progress_counter: dict, entry_info):
    IMAGE_WIDTH: int = 200
    IMAGE_HEIGHT: int = 200

    MAX_IMAGES_IN_LINE: int = 5
    LAST_COLUMN_POSITION: int = 1600

    root = tk.Toplevel()
    root.title('All photos')

    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    root.geometry("{}x{}+0+0".format(screen_width - 5, screen_height - 80))

    # Create A Main frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=1, side=tk.LEFT)

    # Create A Canvas
    my_canvas = tk.Canvas(main_frame)
    my_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    # Create Another Frame INSIDE the Canvas
    second_frame = tk.Frame(my_canvas)

    add_scroll_bar(main_frame, my_canvas, second_frame)

    # Create visible window
    my_canvas.create_window((0, 0), window=second_frame, anchor="nw")
    # my_canvas.create_line(100, 0, 100, 100)

    x_position, y_position = 0, 0
    photos_names_dict = {}
    image_list = []
    counter = 0
    products_list = create_product_collection_from_step(products_list, list(entry_info.references_dict.keys()),
                                                        entry_info) \
        if entry_info.data_from_step and not entry_info.gather_data_before_start else products_list

    for product in products_list:

        # Nazwa produktu
        product_name = tk.Text(second_frame, height=0, width=25)
        product_name.grid(row=y_position, column=0, pady=1, padx=10)
        product_name.insert(tk.END, product.product_id)
        product_name.config(state='disabled')

        for photo in product.all_photos:
            if entry_info.data_from_step and not entry_info.download_data_before_start:
                image = photo.asset_data
            elif entry_info.download_data_before_start:
                image = get_image(photo)
            else:
                image = Image.open(f"{photo_path}/{photo.name}")
            image = image.resize((IMAGE_WIDTH, IMAGE_HEIGHT))
            my_img = ImageTk.PhotoImage(image)
            image_list.append(my_img)

        def click_check_box(checkbnt):
            if checkbnt.var.get():
                checkbnt.var.set(0)
            else:
                checkbnt.var.set(1)

        for i, photo in enumerate(product.all_photos):

            dict_key = f"{product.product_id};{photo.name}"

            # tk.Label(second_frame, image=image_list[i + counter]).grid(row=y_position + 1, column=x_position, pady=1, padx=10)

            # Nazwa referencji
            tk.Label(second_frame, text=f"{photo.asset_type[:35]}").grid(row=y_position + 2, column=x_position, pady=1,
                                                                         padx=10)

            # Rozmiary
            tk.Label(second_frame, text=f"W: {photo.width}/ H:{photo.height}").grid(row=y_position + 3,
                                                                                    column=x_position, pady=1, padx=10)

            # Set the text for each checkbutton
            photos_names_dict[dict_key] = tk.Checkbutton(second_frame, text=photo.name)

            if photo.selected_photo:
                # Create a new instance of IntVar() for each checkbutton
                photos_names_dict[dict_key].var = tk.IntVar(value=1)
            else:
                # Create a new instance of IntVar() for each checkbutton
                photos_names_dict[dict_key].var = tk.IntVar()

            # Set the variable parameter of the checkbutton
            photos_names_dict[dict_key]['variable'] = photos_names_dict[dict_key].var

            # Arrange the checkbutton in the window
            photos_names_dict[dict_key].grid(row=y_position + 4, column=x_position, pady=10, padx=10)

            if photo.validated:
                tk.Button(second_frame, image=image_list[i + counter], bg='yellow',
                          command=lambda x=photos_names_dict[dict_key]: click_check_box(x)).grid(
                    row=y_position + 1, column=x_position, pady=1, padx=10)
            elif photo.worse:
                tk.Button(second_frame, image=image_list[i + counter], bg='red',
                          command=lambda x=photos_names_dict[dict_key]: click_check_box(x)).grid(
                    row=y_position + 1, column=x_position, pady=1, padx=10)
            else:
                tk.Button(second_frame, image=image_list[i + counter],
                          command=lambda x=photos_names_dict[dict_key]: click_check_box(x)).grid(
                    row=y_position + 1, column=x_position, pady=1, padx=10)
            x_position += 1
            if x_position >= MAX_IMAGES_IN_LINE:
                x_position = 0
                y_position += 5

        styl = ttk.Style()
        styl.configure('TSeparator', background='blue')

        # horizontal separator
        for col in range(MAX_IMAGES_IN_LINE):
            ttk.Separator(
                master=second_frame,
                orient=tk.HORIZONTAL,
                style='blue.TSeparator',
                takefocus=1
            ).grid(row=y_position + 5, column=col, ipadx=150)

        counter += len(product.all_photos)
        x_position, y_position = 0, y_position + 6

    def select_photos(products_list):

        for product in products_list:
            for photo in product.all_photos:
                checkbnt = photos_names_dict.get(f"{product.product_id};{photo.name}")
                if checkbnt.var.get():
                    photo.selected_photo = True
                    print('Item selected: {}'.format(checkbnt['text']))
                else:
                    photo.selected_photo = False

    # #####################Right site of frame#########################
    right_frame = tk.Frame(root)
    # Progress bar
    progress_frame = tk.Frame(right_frame)
    progress = ClsProgress(progress_frame)
    progress.add_counter()
    progress.progress(progress_counter.get("current") / progress_counter.get("all") * 100)
    if progress_counter.get("current") >= progress_counter.get("all"):
        progress.change_counter_label_text(f"{progress_counter.get('all')}/{progress_counter.get('all')}")
    else:
        progress.change_counter_label_text(f"{progress_counter.get('current')}/{progress_counter.get('all')}")
    # progress.root.place(x=LAST_COLUMN_POSITION, y=10)
    progress_frame.grid(row=0, column=MAX_IMAGES_IN_LINE)

    # Buttons and functions
    button_action = tk.IntVar()
    button_action.set(int(ButtonConst.NEXT))

    global next_product_id
    next_product_id = None

    def buttons_function(button_type):
        if button_type == ButtonConst.NEXT:
            select_photos(products_list)
        elif button_type == ButtonConst.CLOSE:
            select_photos(products_list)
            button_action.set(int(button_type))
        elif button_type == ButtonConst.BACK:
            select_photos(products_list)
            button_action.set(int(button_type))
        elif button_type == ButtonConst.GO_TO:
            global next_product_id
            select_photos(products_list)
            next_product_id = go_to_text_box.get("1.0", "end-1c")
            button_action.set(int(button_type))
        elif button_type == ButtonConst.DOWNLOAD:
            select_photos(products_list)
            button_action.set(int(button_type))
        root.quit()
        root.destroy()
        button_action.get()

    # Next button
    if progress_counter.get('current') >= progress_counter.get('all'):
        button_next = tk.Button(right_frame, text="Finish", command=lambda: buttons_function(ButtonConst.NEXT),
                                width=30,
                                height=5)
    else:
        button_next = tk.Button(right_frame, text="Next", command=lambda: buttons_function(ButtonConst.NEXT), width=30,
                                height=5)
    # button_next.place(x=LAST_COLUMN_POSITION, y=50)
    button_next.grid(row=1, column=MAX_IMAGES_IN_LINE)
    root.bind('<Right>', lambda event: buttons_function(1))

    # Back button
    back_button = tk.Button(right_frame, text="Back", command=lambda: buttons_function(ButtonConst.BACK), width=30,
                            height=5)
    back_button.grid(row=2, column=MAX_IMAGES_IN_LINE)
    # back_button.place(x=LAST_COLUMN_POSITION, y=150)
    if progress_counter.get("first") == 0:
        back_button['state'] = "disable"
    else:
        root.bind('<Left>', lambda event: buttons_function(ButtonConst.BACK))

    # Close button
    close_button = tk.Button(right_frame, text="Close", command=lambda: buttons_function(ButtonConst.CLOSE), width=30,
                             height=5)
    close_button.grid(row=3, column=MAX_IMAGES_IN_LINE)
    # close_button.place(x=LAST_COLUMN_POSITION, y=250)

    # GoTo button
    go_to_label = tk.Label(right_frame, text=f"Go to:")
    # go_to_label.place(x=LAST_COLUMN_POSITION, y=350)
    go_to_label.grid(row=4, column=MAX_IMAGES_IN_LINE)

    go_to_text_box = tk.Text(right_frame, height=1, width=25)
    # go_to_text_box.place(x=LAST_COLUMN_POSITION, y=370)
    go_to_text_box.grid(row=5, column=MAX_IMAGES_IN_LINE)

    go_to_button = tk.Button(right_frame, text="Go To", command=lambda: buttons_function(ButtonConst.GO_TO), width=30,
                             height=5)
    # go_to_button.place(x=LAST_COLUMN_POSITION, y=410)
    go_to_button.grid(row=6, column=MAX_IMAGES_IN_LINE)

    if entry_info.data_from_step:
        close_and_download_button = tk.Button(right_frame, text="Close and download selected",
                                              command=lambda: buttons_function(ButtonConst.DOWNLOAD), width=30,
                                              height=5)
        # close_and_download_button.place(x=LAST_COLUMN_POSITION, y=500)
        close_and_download_button.grid(row=7, column=MAX_IMAGES_IN_LINE)
    right_frame.pack(fill=tk.BOTH, expand=1)

    # Closing by 'X' warning
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            button_action.set(int(ButtonConst.CLOSE))
            button_action.get()
            root.quit()
            root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)

    # Root settings
    root.focus_force()
    root.mainloop()
    return button_action.get(), next_product_id


def add_scroll_bar(main_frame, my_canvas, second_frame):
    y_scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=my_canvas.yview)
    y_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Configure the canvas
    my_canvas.configure(yscrollcommand=y_scrollbar.set)
    my_canvas.bind("<Configure>", lambda e: my_canvas.config(scrollregion=my_canvas.bbox(tk.ALL)))

    # mouse ScrollBar
    def my_callback(event):
        if event.delta > 0:
            my_canvas.yview_scroll(-1, "units")
        else:
            my_canvas.yview_scroll(1, "units")

    second_frame.bind("<MouseWheel>", my_callback)


def get_image(photo):
    if photo.extension == PDF:
        image = convert_from_path(f"{TEMP_ASSETS_FROM_STEP_FOLDER}/{photo.name}.{photo.extension}",
                                  poppler_path=Path(POPPLER_PATH))[0]
    else:
        image = Image.open(
            f"{TEMP_ASSETS_FROM_STEP_FOLDER}/{photo.name}.{photo.extension}")  # Image.open(f"{photo_path}/{photo.name}")
    return image