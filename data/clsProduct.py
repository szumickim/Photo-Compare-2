import itertools

class Product:
    def __init__(self, **kwargs):
        kwargs = {k: v for k, v in kwargs.items() if v != ""}
        self.__dict__.update(kwargs)
        self.create_all_photos_list()

        self.similar_photos_list = []
        self.photos_connection_type = ""
        self.photos_pairs_list = []

    def create_all_photos_list(self):
        self.all_photos = [getattr(self, a) for a in dir(self) if not a.startswith('__') and a != "<ID>"]
        self.all_photos = list(itertools.chain.from_iterable(self.all_photos[0:-1]))

        for photo in self.all_photos:
            if photo.asset_type.find('Primary') != -1:
                self.all_photos.remove(photo)
                self.all_photos.insert(0, photo)