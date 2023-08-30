class PhotoBasics:
    def __init__(self):
        self.name = None
        self.height = None
        self.width = None
        self.asset_type = None
        self.similar_photo = None
        self.photo_array = None
        self.selected_photo = False
        self.validated = False
        self.worse = False
        self.extension: str

class Photo(PhotoBasics):
    def __init__(self, name, photo_height, photo_width, asset_type):
        super().__init__()
        self.name = name
        self.height = photo_height
        self.width = photo_width
        self.asset_type = asset_type


class PhotoStep(PhotoBasics):
    def __init__(self, asset_name, asset_type, asset_data=None):
        super().__init__()
        self.name = asset_name
        self.asset_type = asset_type

        if asset_data:
            self.height = asset_data.height
            self.width = asset_data.width
            self.asset_data = asset_data