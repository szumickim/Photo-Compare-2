import itertools
import os


class ProductBasics:
    def __init__(self):
        self.product_id = None
        self.similar_photos_list = []
        self.photos_connection_type = ""
        self.photos_pairs_list = []


class Product(ProductBasics):
    def __init__(self, **kwargs):
        kwargs = {k: v for k, v in kwargs.items() if v != ""}
        self.__dict__.update(kwargs)
        self.create_all_photos_list()
        super().__init__()
        self.add_product_id()


    def add_product_id(self):
        self.product_id = getattr(self, "<ID>")

    def create_all_photos_list(self):
        wrong_names = ['<ID>', 'add_product_id', 'create_all_photos_list']
        self.all_photos = [getattr(self, a) for a in dir(self) if not a.startswith('__') and a not in wrong_names]
        self.all_photos = list(itertools.chain.from_iterable(self.all_photos))

        for photo in self.all_photos:
            if photo.asset_type.lower().find('primary') != -1:
                self.all_photos.remove(photo)
                self.all_photos.insert(0, photo)


class ProductStep(ProductBasics):
    def __init__(self, pim_id):
        super().__init__()
        self.all_photos: list = []
        self.product_id = pim_id

    def download_selected(self):
        if not os.path.exists('SelectedPhotos'):
            os.makedirs('SelectedPhotos')
        for photo in self.all_photos:
            if photo.selected_photo:
                photo.asset_data.save(f"SelectedPhotos/{photo.name}.{photo.asset_data.format}")
