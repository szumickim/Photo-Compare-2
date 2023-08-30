from clsPhoto import PhotoStep
from clsProduct import ProductStep
import requests
from requests.auth import HTTPBasicAuth
import json
from PIL import Image
import io
import os
import threading
import warnings
import progressBar
import tkinter as tk
from pdf2image import convert_from_bytes
from pathlib import Path
from constants import *

warnings.filterwarnings('ignore')
LOGIN = 'SZUMIMIC'
PASSWORD = 'step23'
FIND_ID_ASSETS_URL = 'https://steppimprod001.ku.k-netti.com/restapiv2/products'  # /PIM21310811/references/Product%20Image%20further?context=en-GL&workspace=Main
GET_ASSETS_URL = 'https://steppimprod001.ku.k-netti.com/restapiv2/assets'  # /PIM21310811/references/Product%20Image%20further?context=en-GL&workspace=Main


def create_product_collection_from_step(products_list, photo_reference_list, entry_info):
    progres_bar = progressBar.ClsProgress(tk.Toplevel())
    progres_bar.add_counter()
    progres_bar.window_always_on_top()
    for index, photo_reference in enumerate(photo_reference_list):
        progres_bar.change_counter_label_text(f'{photo_reference} {index + 1}/{len(photo_reference_list)}')
        progres_bar.progress((int(index) + 1) / len(photo_reference_list) * 100)
        swagger_module(products_list, photo_reference, entry_info)
    progres_bar.kill_bar()
    return products_list


def create_products_objects(pim_id_list):
    return [ProductStep(pim_id) for pim_id in pim_id_list]


def swagger_module(products_list, photo_reference, entry_info):
    # Semaphore to limit the number of parallel downloads
    semaphore = threading.Semaphore(4)
    # create a list of threads
    threads = []
    for index, product in enumerate(products_list):
        t = threading.Thread(target=gather_data, args=(semaphore, product, photo_reference, entry_info))
        threads.append(t)
        t.start()

    # wait for all threads to finish
    for t in threads:
        t.join()


def gather_data(semaphore, product, photo_reference, entry_info):
    """Download a file from the given url"""
    try:
        with semaphore:
            url_asset = f'{FIND_ID_ASSETS_URL}/{product.product_id}/references/{photo_reference}?context={entry_info.assets_context}&workspace=Main'
            url_asset = url_asset.replace(" ", "%20")
            response = requests.get(url_asset,
                                    auth=HTTPBasicAuth(entry_info.step_login, entry_info.step_password), verify=False)
            asset_info = json.loads(response.content.decode("UTF-8"))

            get_asset_data(asset_info, product, photo_reference, entry_info)

            print(product.product_id, photo_reference)
    except Exception as e:
        print(f"Failed to download: {e}")


def create_object_from_swagger(asset, product, photo_reference, entry_info):
    try:
        response = get_assets(asset.get("target"), entry_info)

        if entry_info.download_data_before_start:
            photo_object = PhotoStep(asset.get("target"), photo_reference)
            photo_object.extension = PDF if response.headers.get("Content-Type").find("pdf") >= 0 else 'jpg'
            save_asset(photo_object, response)
        else:
            asset_data = get_asset_info(response)
            photo_object = PhotoStep(asset.get("target"), photo_reference, asset_data)
            photo_object.extension = PDF if response.headers.get("Content-Type").find("pdf") >= 0 else 'jpg'

        product.all_photos.append(photo_object)
    except Exception as e:
        print(f'Response error: {e}')


def get_asset_data(assets_dict, product, photo_reference, entry_info):
    if assets_dict.get("references"):  # jeżeli jest więcej niż 1 zdjęcie
        for asset in assets_dict.get("references"):
            create_object_from_swagger(asset, product, photo_reference, entry_info)

    elif assets_dict.get("reference"):  # jeżeli jest tylko 1 zdjęcie
        asset = assets_dict.get("reference")
        create_object_from_swagger(asset, product, photo_reference, entry_info)


def get_asset_info(response):
    if response.headers.get("Content-Type").find("image") >= 0:
        return Image.open(io.BytesIO(response.content))
    elif response.headers.get("Content-Type").find("pdf") >= 0:
        return convert_from_bytes(response.content, poppler_path=Path(POPPLER_PATH))[0]


def get_assets(asset_id, entry_info):
    url_asset = f'{GET_ASSETS_URL}/{asset_id}/content?context={entry_info.assets_context}&workspace=Main'
    try:
        response = requests.get(url_asset,
                                auth=HTTPBasicAuth(entry_info.step_login, entry_info.step_password), verify=False,
                                stream=True)
    except:
        return None
    else:
        return response


def download_selected(product, entry_info):
    create_selected_photos_folder()
    for photo in product.all_photos:
        if photo.selected_photo:

            if photo.extension == PDF:
                url_asset = f'{GET_ASSETS_URL}/{photo.name}/content?context={entry_info.assets_context}&workspace=Main'
                url_asset = url_asset.replace(" ", "%20")
                response = requests.get(url_asset,
                                        auth=HTTPBasicAuth(entry_info.step_login, entry_info.step_password),
                                        verify=False)
                save_asset(photo, response)
            else:
                photo.asset_data.save(f"SelectedPhotos/{photo.name}.{photo.asset_data.format}")


def create_selected_photos_folder():
    if not os.path.exists(SELECTED_PHOTOS):
        os.makedirs(SELECTED_PHOTOS)


def save_asset(photo, response):
    with open(fr"{SELECTED_PHOTOS}/{photo.name}.{photo.extension}", "wb") as plik:
        plik.write(response.content)
