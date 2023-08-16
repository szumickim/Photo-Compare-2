from clsPhoto import PhotoStep
from clsProduct import ProductStep
import requests
from requests.auth import HTTPBasicAuth
import json
from PIL import Image
import io
import threading
import os
import urllib.request

LOGIN = 'SZUMIMIC'
PASSWORD = 'step23'
FIND_ID_ASSETS_URL = 'https://steppimprod001.ku.k-netti.com/restapiv2/products' # /PIM21310811/references/Product%20Image%20further?context=en-GL&workspace=Main
GET_ASSETS_URL = 'https://steppimprod001.ku.k-netti.com/restapiv2/assets' # /PIM21310811/references/Product%20Image%20further?context=en-GL&workspace=Main


def create_product_collection_from_step(pim_id_list, photo_reference_list, context):
    products_list = create_products_objects(pim_id_list)
    for photo_reference in photo_reference_list:
        get_assets_id(products_list, photo_reference, context)
    return products_list


def create_products_objects(pim_id_list):
    return [ProductStep(pim_id) for pim_id in pim_id_list]


def get_assets_id(products_list, photo_reference, context):

    # Semaphore to limit the number of parallel downloads
    semaphore = threading.Semaphore(4)
    # create a list of threads
    threads = []
    for index, product in enumerate(products_list):
        t = threading.Thread(target=get_asset_id_mutli, args=(semaphore, product, photo_reference, context))
        threads.append(t)
        t.start()



    # wait for all threads to finish
    for t in threads:
        t.join()


def get_asset_id_mutli(semaphore, product, photo_reference, context):
    """Download a file from the given url"""
    try:
        with semaphore:
            url_asset = f'{FIND_ID_ASSETS_URL}/{product.product_id}/references/{photo_reference}?context={context}&workspace=Main'
            url_asset = url_asset.replace(" ", "%20")
            response = requests.get(url_asset,
                                    auth=HTTPBasicAuth(LOGIN, PASSWORD), verify=False)
            asset_info = json.loads(response.content.decode("UTF-8"))
            gather_data(asset_info, product, photo_reference)
    except Exception as e:
        print(f"Failed to download: {e}")


def gather_data(assets_dict, product, photo_reference):
    if assets_dict.get("references"):  # jeżeli jest więcej niż 1 zdjęcie
        for assets in assets_dict.get("references"):
            try:
                response = get_assets(assets.get("target"))
                asset_info = Image.open(io.BytesIO(response.content))
                photo_object = PhotoStep(asset_info, assets.get("target"), photo_reference)
                product.all_photos.append(photo_object)
            except:
                pass
    elif assets_dict.get("reference"):  # jeżeli jest tylko 1 zdjęcie
        try:
            assets = assets_dict.get("reference")
            response = get_assets(assets.get("target"))
            asset_info = Image.open(io.BytesIO(response.content))
            photo_object = PhotoStep(asset_info, assets.get("target"), photo_reference)
            product.all_photos.append(photo_object)
        except:
            pass


def get_assets(asset_id):
    url_asset = f'{GET_ASSETS_URL}/{asset_id}/content?context=en-GL&workspace=Main'
    try:
        response = requests.get(url_asset,
                                auth=HTTPBasicAuth(LOGIN, PASSWORD), verify=False, stream=True)
    except:
        return None
    else:
        return response






