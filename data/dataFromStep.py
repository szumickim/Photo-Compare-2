from clsPhoto import PhotoStep
from clsProduct import ProductStep
import requests
from requests.auth import HTTPBasicAuth
import json
from PIL import Image
import io
import progressBar
import tkinter as tk

FIND_ID_ASSETS_URL = 'https://steppimprod001.ku.k-netti.com/restapiv2/products' # /PIM21310811/references/Product%20Image%20further?context=en-GL&workspace=Main
GET_ASSETS_URL = 'https://steppimprod001.ku.k-netti.com/restapiv2/assets' # /PIM21310811/references/Product%20Image%20further?context=en-GL&workspace=Main


def get_asstets_id(pim_id, photo_reference, context):
    url_asset = f'{FIND_ID_ASSETS_URL}/{pim_id}/references/{photo_reference}?context={context}&workspace=Main'
    url_asset = url_asset.replace(" ", "%20")
    try:
        response = requests.get(url_asset,
                                auth=HTTPBasicAuth('SZUMIMIC', 'step23'), verify=False)
    except:
        return None
    else:
        return response.content.decode("UTF-8")


def get_assets(asset_id):
    url_asset = f'{GET_ASSETS_URL}/{asset_id}/content?context=en-GL&workspace=Main'
    try:
        response = requests.get(url_asset,
                                auth=HTTPBasicAuth('SZUMIMIC', 'step23'), verify=False, stream=True)
        pass
    except:
        return None
    else:
        return response


def gather_data(assets_dict, photos_list, photo_reference):
    if assets_dict.get("references"):  # jeżeli jest więcej niż 1 zdjęcie
        for assets in assets_dict.get("references"):
            response = get_assets(assets.get("target"))
            asset_info = Image.open(io.BytesIO(response.content))
            photo_object = PhotoStep(asset_info, assets.get("target"), photo_reference)
            photos_list.append(photo_object)
    elif assets_dict.get("reference"):  # jeżeli jest tylko 1 zdjęcie
        assets = assets_dict.get("reference")
        response = get_assets(assets.get("target"))
        asset_info = Image.open(io.BytesIO(response.content))
        photo_object = PhotoStep(asset_info, assets.get("target"), photo_reference)
        photos_list.append(photo_object)
    return photos_list


def get_data_from_Step(pim_id, photo_reference_list, context):
    photos_list = []
    for photo_reference in photo_reference_list:
        assets_dict = get_asstets_id(pim_id, photo_reference, context)
        assets_dict = json.loads(assets_dict)
        gather_data(assets_dict, photos_list, photo_reference)
    return photos_list


def create_product_collection_from_step(pim_id_list, photo_reference_list, context):
    progres_bar = progressBar.ClsProgress(tk.Toplevel())
    progres_bar.add_counter()
    products_list = []
    counter = 0
    for pim_id in pim_id_list:
        progres_bar.progress(counter / len(pim_id_list) * 100)
        photos_list = get_data_from_Step(pim_id, photo_reference_list, context)
        product = ProductStep(pim_id)

        for photo in photos_list:
            product.all_photos.append(photo)

        products_list.append(product)
        counter += 1

    progres_bar.kill_bar()
    return products_list
