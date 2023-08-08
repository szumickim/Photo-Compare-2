from clsPhoto import PhotoStep
import clsProduct
import requests
from requests.auth import HTTPBasicAuth
import json
from PIL import Image
import io

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

if __name__ == "__main__":
    pim_id = 'PIM21310811'
    photo_reference = 'Product Image further'
    context = 'en-GL'
    assets_dict = get_asstets_id(pim_id, photo_reference, context)
    assets_dict = json.loads(assets_dict)

    for assets in assets_dict.get("references"):
        response = get_assets(assets.get("target"))
        asset_info = Image.open(io.BytesIO(response.content))
        photo_object = PhotoStep(asset_info, assets.get("target"))
        pass