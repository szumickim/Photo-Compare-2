import tkinter as tk
from PIL import ImageTk
from consts import *
from tkinter import messagebox
from clsPhoto import Photo


# ################# PORÓWNYWANIE ZDJĘĆ LIVE ###########################
def show_image(photo_path, img1: Photo, img2: Photo):
    # root window
    image_root = tk.Toplevel()
    image_root.title('Photo Compare')

    image_root.geometry("800x400+300+400")

    first_img = ImageTk.PhotoImage(file=f"{photo_path}/{img1.name}", master=image_root)
    label = tk.Label(image_root, image=first_img)
    label.pack()
    label.place(relx=0.5, rely=0.5, x=-300, y=-150)

    first_img_label = tk.Label(image_root, text=f"Image name: {img1.name}")
    first_img_label.pack()
    first_img_label.place(x=100, y=255)

    first_img_height = tk.Label(image_root, text=f"Height: {img1.height}")
    first_img_height.pack()
    first_img_height.place(x=100, y=275)

    first_img_width = tk.Label(image_root, text=f"Width: {img1.width}")
    first_img_width.pack()
    first_img_width.place(x=100, y=295)

    second_img = ImageTk.PhotoImage(file=f"{photo_path}/{img2.name}", master=image_root)
    label = tk.Label(image_root, image=second_img)
    label.pack()
    label.place(relx=0.5, rely=0.5, x=100, y=-150)

    second_img_label = tk.Label(image_root, text=f"Image name: {img2.name}")
    second_img_label.pack()
    second_img_label.place(x=500, y=255)

    second_img_height = tk.Label(image_root, text=f"Height: {img2.height}")
    second_img_height.pack()
    second_img_height.place(x=500, y=275)

    second_img_width = tk.Label(image_root, text=f"Width: {img2.width}")
    second_img_width.pack()
    second_img_width.place(x=500, y=295)

    # ###################### PRZYCISKI ######################

    manual_pick = tk.IntVar()
    manual_pick.set(1)

    button_action = tk.IntVar()
    button_action.set(int(ButtonConst.NEXT))

    better_image_pick = tk.IntVar()
    better_image_pick.set(0)

    def first_img_better_function():
        manual_pick.set(1)
        manual_pick.get()
        better_image_pick.set(1)
        better_image_pick.get()
        button_action.get()
        image_root.quit()
        image_root.destroy()

    first_img_better_button = tk.Button(image_root, text="Worse ->", command=first_img_better_function, width=6, height=1)
    first_img_better_button.pack()
    first_img_better_button.place(relx=0.5, rely=0.5, x=-350, y=30)

    def second_img_better_function():
        manual_pick.set(1)
        manual_pick.get()
        better_image_pick.set(2)
        better_image_pick.get()
        button_action.get()
        image_root.quit()
        image_root.destroy()

    second_img_better_button = tk.Button(image_root, text="Worse ->", command=second_img_better_function, width=6, height=1)
    second_img_better_button.pack()
    second_img_better_button.place(relx=0.5, rely=0.5, x=50, y=30)

    def same_function():
        manual_pick.set(1)
        manual_pick.get()
        button_action.get()
        image_root.quit()
        image_root.destroy()

    image_root.bind('s', lambda event: same_function())

    same_button = tk.Button(image_root, text="Same", command=same_function, width=20, height=2)
    same_button.pack()
    same_button.place(relx=0.5, rely=0.5, x=-100, y=150)

    def different_function():
        manual_pick.set(2)
        manual_pick.get()
        button_action.get()
        image_root.quit()
        image_root.destroy()

    image_root.bind('d', lambda event: different_function())
    different_button = tk.Button(image_root, text="Different", command=different_function, width=20, height=2)
    different_button.pack()
    different_button.place(relx=0.5, rely=0.5, x=50, y=150)

    # Close button
    def end_program():
        button_action.set(int(ButtonConst.CLOSE))
        button_action.get()
        image_root.quit()
        image_root.destroy()

    end_button = tk.Button(image_root, text="Close", command=end_program, width=20, height=2)
    end_button.pack()
    end_button.place(relx=0.5, rely=0.5, x=200, y=150)

    # Ostrzeżenie przed zamknięciem programu za pomocą 'X'
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            button_action.set(int(ButtonConst.CLOSE))
            button_action.get()
            image_root.quit()
            image_root.destroy()

    image_root.protocol("WM_DELETE_WINDOW", on_closing)
    image_root.focus_force()
    # Loop
    image_root.mainloop()
    return manual_pick.get(), button_action.get(), better_image_pick.get()
