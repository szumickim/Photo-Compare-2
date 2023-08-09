import tkinter as tk
from tkinter import filedialog
import tkinter.font as font

import photoCompareObj
from entryInfo import EntryInfo

window = tk.Tk()
window.title("Scorecard")

font_style = font.Font(weight="bold", size=12)
PHOTO_FOLDER_ROW: int = 0
EXCEL_ROW: int = 1
RUN_BUTTON_ROW: int = 2

window_width: int = 400
window_height: int = 200

space_span: int = 5
label_height: int = 20
label_width: int = 50
list_width: int = label_width
super_position_label: float = label_width * 0.5

# #################   Ustawianie pozycji userForma    #######################

# Gets the requested values of the height and width.
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()

# Gets both half the screen width/height and window width/height
positionRight = int(window.winfo_screenwidth() / 2 - windowWidth)
positionDown = int(window.winfo_screenheight() / 2 - windowHeight)

# Positions the window in the center of the page.
window.geometry("+{}+{}".format(positionRight, positionDown))
window.minsize(window_width, window_height)

# ################   Wgrywanie folderu ze zdjęciami i excela ###############

# folder path
photo_folder_label = tk.Label(window, text="Photo folder path:")
photo_folder_label.grid(row=PHOTO_FOLDER_ROW, column=0)

photo_folder_path = tk.Label(window, text="", background='yellow', width=30, anchor="w")
photo_folder_path.grid(row=PHOTO_FOLDER_ROW, column=2)

def select_new_data_folder_path():
    folder_name = filedialog.askdirectory()
    if folder_name:
        photo_folder_path['text'] = folder_name

# browse load button new data folder
load_button = tk.Button(window, text="Browse", command=select_new_data_folder_path, width=10)
load_button.grid(row=PHOTO_FOLDER_ROW, column=4)


# excel path
excel_label = tk.Label(window, text="Excel path:")
excel_label.grid(row=EXCEL_ROW, column=0)

excel_file_path = tk.Label(window, text="", background='yellow', width=30, anchor="w")
excel_file_path.grid(row=EXCEL_ROW, column=2)

def select_excel_folder_path():
    file_name = filedialog.askopenfilename(title="Select A File")
    if file_name:
        excel_file_path['text'] = file_name

load_button = tk.Button(window, text="Browse", command=select_excel_folder_path, width=10)
load_button.grid(row=EXCEL_ROW, column=4)
# ##################   Number of elements in show all   ##########

tk.Label(window, text="Number of elements in show all: ").grid(row=3, column=0)
elements_in_show_all = tk.Entry(window, width=2, justify='center')
elements_in_show_all.insert(0, "3")
elements_in_show_all.grid(row=3, column=1)

# ##################### CheckButtons ##############################

live_preview_var = tk.BooleanVar()
live_preview_check_box = tk.Checkbutton(window, text="Live preview", variable=live_preview_var, onvalue=True,
                                        offvalue=False)
live_preview_check_box.grid(sticky="W", row=5, column=0)

resize_photo_var = tk.BooleanVar()
resize_photo_check_box = tk.Checkbutton(window, text="Resize photos to 200x200", variable=resize_photo_var,
                                        onvalue=True, offvalue=False)
resize_photo_check_box.grid(sticky="W", row=6, column=0)

continue_work_var = tk.BooleanVar()
resize_photo_check_box = tk.Checkbutton(window, text="Continue work", variable=continue_work_var, onvalue=True,
                                        offvalue=False)
resize_photo_check_box.grid(sticky="W", row=7, column=0, padx=1, pady=1)

# ######################   SSIM values   #############################
#
# tk.Label(window, text="Similar - SSIM value ").grid(row=2, column=0)
# tk.Label(window, text="Possibly similar - SSIM value").grid(row=3, column=0)
#
# tk.Label(window, text="From:").grid(row=2, column=1)
# similar_from = tk.Entry(window)
# similar_from.insert(0, "1.0")
# similar_from.grid(row=2, column=2)
# tk.Label(window, text="To:").grid(row=2, column=3)
# similar_to = tk.Entry(window)
# similar_to.insert(0, "1.0")
# similar_to.grid(row=2, column=4)
#
# tk.Label(window, text="From:").grid(row=3, column=1)
# possibly_similar_from = tk.Entry(window)
# possibly_similar_from.insert(0, "0.95")
# possibly_similar_from.grid(row=3, column=2)
# tk.Label(window, text="To:").grid(row=3, column=3)
# possibly_similar_to = tk.Entry(window)
# possibly_similar_to.insert(0, "1.0")
# possibly_similar_to.grid(row=3, column=4)

# ######################   Radio Button   #############################

MODES = [
    ("Compare", "Compare"),
    ("Show all images", "Show all images")
]

program_type = tk.StringVar()
vertical_offset = 20
counter = 0
for text, mode in MODES:
    vertical_offset += 20
    radio_button = tk.Radiobutton(window, text=text, variable=program_type, value=mode)

    radio_button.grid(row=5 + counter, column=4)
    counter += 1
program_type.set('Compare')

# ######################   Run Button   #############################


def my_click():
    print(program_type.get())
    photo_path = photo_folder_path.cget('text')
    excel_path = excel_file_path.cget('text')

    entry_info = EntryInfo(excel_path=excel_path, photo_path=photo_path, live_preview=live_preview_var.get(), continue_work=continue_work_var.get(),
                         resize_photo=resize_photo_var.get(), program_type=program_type.get(), elements_in_show_all=elements_in_show_all.get(), data_from_step=True)

    photoCompareObj.main(entry_info)

    end_program_label = tk.Label(window, text="Finished!", background='green', width=30)
    end_program_label.grid(row=5, column=2)

run_button = tk.Button(window, text="Run", command=my_click, width=20, height=2)
run_button['font'] = font_style
run_button.grid(row=RUN_BUTTON_ROW, column=2)

window.mainloop()
