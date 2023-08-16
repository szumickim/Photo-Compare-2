import itertools
import cv2
from skimage.metrics import structural_similarity as ssim
import tkinter as tk
from PIL import Image
import pymsgbox
import shutil
from entryInfo import EntryInfo
from clsPhoto import Photo
from clsProduct import Product
from clsPhotosPair import PhotosPair
from showAllPhotos import show_all_photos
from showCompareImages import show_image
from excelWorkspace import *
from dataFromStep import create_product_collection_from_step
from dataFromStep import create_products_objects
import progressBar
from constants import *

def main(entry_info: EntryInfo):

    if entry_info.data_from_step:
        photo_reference_list = list(entry_info.references_dict.keys())
        context = 'en-GL'
        products_collection = create_products_objects(entry_info.pim_id_list)
        if entry_info.gather_data_before_start:
            products_collection = create_product_collection_from_step(products_collection, photo_reference_list, context)

        first_row = 0
    else:
        # Wczytywanie excela z informacjami o zdjęciach
        df_export, first_row = read_export(entry_info.excel_path, entry_info.continue_work)

        # tworzenie obiektów 'products'
        products_collection = create_products_collection(df_export, entry_info)


    # Inicjowanie progressBaru
    if entry_info.program_type == COMPARE:
        compare_photo_path = resize_photos(entry_info.photo_path) if entry_info.resize_photo else entry_info.photo_path
        progres_bar = progressBar.ClsProgress(tk.Toplevel())
        progres_bar.add_counter()
    else:
        progres_bar = None

    # Pozycja pierwszego produktu
    i = first_row

    # Ustalanie wartości początkowej parametru do wcześniejszego wyłączenia programu
    continue_program = True

    # Inicjowanie zmiennej używanej do przycisków
    button_action = int(ButtonConst.NEXT)

    # Licznik backupu
    backup_counter = 0

    while i < len(products_collection):
        backup_counter += 1

        if i < 0:
            i = 0

        if not continue_program:
            break

        if entry_info.program_type == COMPARE:
            product = products_collection[i]
            product.photos_connection_type = IS_DIFFERENT

            continue_program, button_action = compare_images_loop(product, entry_info, continue_program, button_action, compare_photo_path)

            progres_bar.progress(int(i - first_row) / (len(products_collection) - first_row) * 100)
            progres_bar.change_counter_label_text(f'{int(i - first_row)}/{len(products_collection) - first_row}')

        elif entry_info.program_type == ALL_IMAGES:
            continue_program, button_action, i = show_all_images_loop(products_collection, entry_info, continue_program, i)

            if backup_counter % 100 == 0:
                backup_excel(products_collection, entry_info.photo_path)

        if button_action == int(ButtonConst.BACK):
            i -= entry_info.elements_on_screen
        elif button_action == int(ButtonConst.NEXT):
            i += entry_info.elements_on_screen

    if entry_info.program_type == COMPARE:
        add_column_to_excel(entry_info.excel_path, products_collection, first_row)
        create_summary_excel(products_collection, entry_info.photo_path)
        # Wyłączanie progressbaru
        progres_bar.kill_bar()
        # Usuwanie tymczasowych, rozszerzonych zdjęć
        if entry_info.resize_photo:
            shutil.rmtree(compare_photo_path)

    elif entry_info.program_type == ALL_IMAGES:
        work_with_show_all_summ_excel(products_collection, entry_info.photo_path)

    if entry_info.data_from_step and button_action == ButtonConst.DOWNLOAD:
        download_selected(products_collection)




def download_selected(products_collection):
    for product in products_collection:
        product.download_selected()

def show_all_images_loop(products_collection: list, entry_info: EntryInfo, continue_program, i):
    progress_counter = {"first": i, "current": i + entry_info.elements_on_screen, "all": len(products_collection)}

    button_action, next_product_id = show_all_photos(products_collection[i:i + entry_info.elements_on_screen], entry_info.photo_path, progress_counter, entry_info)
    if button_action in [int(ButtonConst.CLOSE), int(ButtonConst.DOWNLOAD)]:
        continue_program = False
    elif button_action == int(ButtonConst.GO_TO):
        go_to_i = go_to_product(products_collection, next_product_id)
        if go_to_i >= 0:
            i = go_to_i
    return continue_program, button_action, i


def compare_images_loop(product: Product, entry_info: EntryInfo, continue_program, button_action, photo_path):
    # pętla po wszystkich możliwych kombinacjach zdjęć produktu
    for first_photo, second_photo in itertools.combinations(product.all_photos, 2):

        # Sczytywanie danych zdjęć
        first_photo.photo_array = cv2.imread(f"{photo_path}/{first_photo.name}")
        second_photo.photo_array = cv2.imread(f"{photo_path}/{second_photo.name}")

        # Porównywanie odbywa się jedynie w przypadku, gdy oba zdjęcia są tych samych rozmiarów
        if first_photo.photo_array.shape[0] == second_photo.photo_array.shape[0] and first_photo.photo_array.shape[1] == \
                second_photo.photo_array.shape[1]:

            # Zmiana kolorów na czarno-białe
            first_photo.photo_array = cv2.cvtColor(first_photo.photo_array, cv2.COLOR_BGR2GRAY)
            second_photo.photo_array = cv2.cvtColor(second_photo.photo_array, cv2.COLOR_BGR2GRAY)

            # Porównywanie
            continue_program, button_action = compare_images(first_photo, second_photo, product, photo_path,
                                                             entry_info.live_preview)

            if not continue_program:
                break
    return continue_program, button_action


def go_to_product(products_collection, next_product_id):
    for count, prod in enumerate(products_collection):
        if getattr(prod, '<ID>') == next_product_id.strip():
            return count
    return -1


def get_columns_length(df_export) -> int:
    if SIMILARITY_TYPE_COLUMN in df_export.columns:
        return len(df_export.columns) - 2
    else:
        return len(df_export.columns)


def create_products_collection(df_export, entry_info):
    df_new = pd.DataFrame(df_export["<ID>"])

    columns_length = get_columns_length(df_export)

    for j in range(1, columns_length, 3):
        temp_df = df_export.iloc[:, j:3+j]
        temp_df.columns = ["name", "photo_height", "photo_width"]
        photos_list = [create_obj_list(row.get("name"), row.get("photo_height"),
                                       row.get("photo_width"), df_export.columns[j]) if str(row.get("name")).lower() != "nan" else "" for row in temp_df.to_dict(orient='records')]
        df_new[df_export.columns[j]] = photos_list

    products_collection = [Product(**kwargs) for kwargs in df_new.to_dict(orient='records') if kwargs]

    if entry_info.program_type == ALL_IMAGES:
        add_validated_products_to_collection(products_collection, entry_info)

    return products_collection


def find_to_summary_excel(folder_path):
    pattern = "Summary"
    files = os.listdir(folder_path)
    paths = [os.path.join(folder_path, basename) for basename in files if basename.find(pattern) >= 0]
    if paths:
        return pd.read_excel(max(paths, key=os.path.getmtime), sheet_name=0, dtype=str)
    else:
        return None


def select_validated_products(products_collection, df_validated):
    for product in products_collection:
        if (df_validated[SummaryConst.PRODUCT_ID].eq(getattr(product, "<ID>"))).any():
            single_row = df_validated.loc[df_validated[SummaryConst.PRODUCT_ID] == getattr(product, "<ID>")]
            for photo in product.all_photos:
                if (single_row[SummaryConst.WORSE]).eq(photo.name).any():
                    photo.worse = True

                elif (single_row[SummaryConst.FIRST_PHOTO_ID]).eq(photo.name).any() \
                        or (single_row[SummaryConst.SECOND_PHOTO_ID]).eq(photo.name).any():
                    photo.validated = True


def add_validated_products_to_collection(products_collection, entry_info: EntryInfo):
    df_validated = find_to_summary_excel(entry_info.photo_path)
    if isinstance(df_validated, pd.DataFrame):
        select_validated_products(products_collection, df_validated)


def resize_photos(photo_path):

    resize_progress = progressBar.ClsProgress(tk.Toplevel())
    temp_folder_dir = f"{photo_path}/temp"
    os.mkdir(temp_folder_dir)
    counter = 1
    for filename in os.listdir(photo_path):
        if filename.endswith(".jpg"):
            image = Image.open(f"{photo_path}/{filename}")
            new_image = image.resize((200, 200))
            new_image.save(f"{temp_folder_dir}/{filename}")

        resize_progress.progress(counter/len(os.listdir(photo_path))*100)

        counter += 1

    photo_path = temp_folder_dir

    resize_progress.kill_bar()

    return photo_path


def read_export(excel_path, continue_work):
    df = pd.read_excel(excel_path, sheet_name=0, dtype=str)

    # Jeżeli jest wybrana opcja 'continue work' to dane są zaczytywane od ostatniego produktu,
    # którego zdjęcia były porównywane.
    if continue_work:
        blank_row_bool = df.iloc[:, -2].isna()

        if len([i for i, x in enumerate(blank_row_bool) if x]) == 0:
            pymsgbox.alert('Export file is already filled!', 'Photo Compare Error')
            exit()

        first_row_of_iteration = [i for i, x in enumerate(blank_row_bool) if x][0] - 2
        df = df.iloc[first_row_of_iteration:, :]
    else:
        first_row_of_iteration = 0
    return df, first_row_of_iteration


def create_obj_list(name: str, height: str, width: str, asset_type):

    zip_list = zip(str(name).split(";"), str(height).split(";"), str(width).split(";"))
    obj_list = []
    for single_name, single_height, single_width in zip_list:
        single_name = f'{single_name}.jpg' if single_name.find(".jpg") == -1 else single_name
        obj_list.append(Photo(single_name, single_height, single_width, asset_type))
    return obj_list


def compare_images(imageA: Photo, imageB: Photo, product: Product, photo_folder_path: str, live_preview):

    # ustawianie domyślnych wartości
    button_action = int(ButtonConst.NEXT)
    continue_program = True

    # Obliczanie wartości wskaźnika SSIM
    ssim_score = ssim(imageA.photo_array, imageB.photo_array)

    if float(1) <= ssim_score <= float(1):  # Jeżeli program uzna, że zdjęcia są identyczne
        product.photos_pairs_list.append(PhotosPair(imageA, imageB, "S"))
        product.photos_connection_type = IS_SIMILAR

        print(f"SSIM:{ssim_score}")
        print(imageA.name, imageB.name)

    elif float(0.95) <= ssim_score < float(1):  # Jeżeli program uzna, że zdjęcia powinny zostać poddane weryfikacji
        if live_preview:
            manual_pick, button_action, better_photo = show_image(photo_folder_path, imageA, imageB)

            if button_action != 2:
                if manual_pick == SAME:
                    photo_pair = PhotosPair(imageA, imageB, "S")
                    if better_photo == 1:
                        photo_pair.better_photo = imageA.name
                    elif better_photo == 2:
                        photo_pair.better_photo = imageB.name

                    product.photos_pairs_list.append(photo_pair)

                    product.photos_connection_type = MANUAL

                    print(f"SSIM:{ssim_score}")
                    print(imageA.name, imageB.name)
            else:
                continue_program = False
        else:

            product.photos_pairs_list.append(PhotosPair(imageA, imageB, "P"))

            if product.photos_connection_type not in [IS_SIMILAR, MANUAL]:
                product.photos_connection_type = POSSIBLE
            print(f"SSIM:{ssim_score}")
            print(imageA.name, imageB.name)

    return continue_program, button_action


if __name__ == "__main__":
    excel_test_path = r'excel.xlsx'
    photo_test_path = r'C:\Users\szumimic\Desktop\Python_scripts\Photo Compare\Zdjecia\Foty 7\2023-05-11_12.12.53_images (1)'
    excel_path = fr"{photo_test_path}\{excel_test_path}"
    continue_work = False
    if_resize_photos = False
    live_preview = False

    # entry_info = EntryInfo(excel_path=excel_path, photo_path=photo_test_path, live_preview=live_preview, continue_work=continue_work,
    #                      resize_photo=if_resize_photos, program_type=ALL_IMAGES, elements_in_show_all=3, data_from_step=True)

    entry_info = EntryInfo(program_type=ALL_IMAGES, elements_in_show_all=3, data_from_step=True)
    main(entry_info)
