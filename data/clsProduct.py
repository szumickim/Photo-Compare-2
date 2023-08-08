import itertools


class ProductBasics:
    def __init__(self):
        self.product_id = None
        self.all_photos = []
        self.similar_photos_list = []
        self.photos_connection_type = ""
        self.photos_pairs_list = []


class Product(ProductBasics):
    def __init__(self, **kwargs):
        super().__init__()
        kwargs = {k: v for k, v in kwargs.items() if v != ""}
        self.__dict__.update(kwargs)
        self.create_all_photos_list()
        self.add_product_id()

    def add_product_id(self):
        self.product_id = getattr(self, "<ID>")

    def create_all_photos_list(self):
        self.all_photos = [getattr(self, a) for a in dir(self) if not a.startswith('__') and a != "<ID>"]
        self.all_photos = list(itertools.chain.from_iterable(self.all_photos[0:-1]))

        for photo in self.all_photos:
            if photo.asset_type.find('Primary') != -1:
                self.all_photos.remove(photo)
                self.all_photos.insert(0, photo)


class ProductStep(ProductBasics):
    def __init__(self, pim_id):
        super().__init__()
        self.product_id = pim_id
