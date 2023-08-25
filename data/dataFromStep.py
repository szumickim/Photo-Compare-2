from clsPhoto import PhotoStep
from clsProduct import ProductStep
import requests
from requests.auth import HTTPBasicAuth
import json
from PIL import Image
import io
import threading
import warnings
import progressBar
import tkinter as tk
from pdf2image import convert_from_path, convert_from_bytes
from pathlib import Path
from constants import *

warnings.filterwarnings('ignore')
LOGIN = 'SZUMIMIC'
PASSWORD = 'step23'
FIND_ID_ASSETS_URL = 'https://steppimprod001.ku.k-netti.com/restapiv2/products' # /PIM21310811/references/Product%20Image%20further?context=en-GL&workspace=Main
GET_ASSETS_URL = 'https://steppimprod001.ku.k-netti.com/restapiv2/assets' # /PIM21310811/references/Product%20Image%20further?context=en-GL&workspace=Main


def create_product_collection_from_step(products_list, photo_reference_list, entry_info):
    progres_bar = progressBar.ClsProgress(tk.Toplevel())
    progres_bar.add_counter()
    progres_bar.window_always_on_top()
    for index, photo_reference in enumerate(photo_reference_list):
        progres_bar.change_counter_label_text(f'{photo_reference} {index + 1}/{len(photo_reference_list)}')
        progres_bar.progress((int(index) + 1) / len(photo_reference_list) * 100)
        get_assets_id(products_list, photo_reference, entry_info)
    progres_bar.kill_bar()
    return products_list


def create_products_objects(pim_id_list):
    return [ProductStep(pim_id) for pim_id in pim_id_list]


def get_assets_id(products_list, photo_reference, entry_info):

    # Semaphore to limit the number of parallel downloads
    semaphore = threading.Semaphore(4)
    # create a list of threads
    threads = []
    for index, product in enumerate(products_list):
        t = threading.Thread(target=get_asset_id_mutli, args=(semaphore, product, photo_reference, entry_info))
        threads.append(t)
        t.start()

    # wait for all threads to finish
    for t in threads:
        t.join()


def get_asset_id_mutli(semaphore, product, photo_reference, entry_info):
    """Download a file from the given url"""
    try:
        with semaphore:
            url_asset = f'{FIND_ID_ASSETS_URL}/{product.product_id}/references/{photo_reference}?context=en-GL&workspace=Main'
            url_asset = url_asset.replace(" ", "%20")
            response = requests.get(url_asset,
                                    auth=HTTPBasicAuth(entry_info.step_login, entry_info.step_password), verify=False)
            asset_info = json.loads(response.content.decode("UTF-8"))
            gather_data(asset_info, product, photo_reference, entry_info)
            print(product.product_id, photo_reference)
    except Exception as e:
        print(f"Failed to download: {e}")


def gather_data(assets_dict, product, photo_reference, entry_info):
    if assets_dict.get("references"):  # jeżeli jest więcej niż 1 zdjęcie
        for assets in assets_dict.get("references"):
            try:
                response = get_assets(assets.get("target"), entry_info)

                asset_info = get_asset_info(response)

                photo_object = PhotoStep(asset_info, assets.get("target"), photo_reference)
                product.all_photos.append(photo_object)
            except Exception as e:
                print(f'Response error: {e}')
    elif assets_dict.get("reference"):  # jeżeli jest tylko 1 zdjęcie
        try:
            assets = assets_dict.get("reference")
            response = get_assets(assets.get("target"), entry_info)

            asset_info = get_asset_info(response)

            photo_object = PhotoStep(asset_info, assets.get("target"), photo_reference)
            product.all_photos.append(photo_object)
        except Exception as e:
            print(f'Response error: {e}')

def get_asset_info(response):
    if response.headers.get("Content-Type").find("image") >= 0:
        return Image.open(io.BytesIO(response.content))
    elif response.headers.get("Content-Type").find("pdf") >= 0:
        return convert_from_bytes(response.content, poppler_path=Path(POPPLER_PATH))[0]


def get_assets(asset_id, entry_info):
    url_asset = f'{GET_ASSETS_URL}/{asset_id}/content?context=en-GL&workspace=Main'
    try:
        response = requests.get(url_asset,
                                auth=HTTPBasicAuth(entry_info.step_login, entry_info.step_password), verify=False, stream=True)
    except:
        return None
    else:
        return response

