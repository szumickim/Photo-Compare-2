class Photo:
    def __init__(self, name, photo_height, photo_width, asset_type):
        self.name = name
        self.height = photo_height
        self.width = photo_width
        self.asset_type = asset_type
        self.similar_photo = None
        self.photo_array = None
        self.delete_photo = False
        self.validated = False
        self.worse = False

class PhotoBasics:
    def __init__(self, name, photo_height, photo_width, asset_type):
        self.name = None
        self.height = None
        self.width = None
        self.asset_type = None
        self.similar_photo = None
        self.photo_array = None
        self.delete_photo = False
        self.validated = False
        self.worse = False

class PhotoStep(PhotoBasics):
    def __init__(self, asset_info, asset_name):
        self.name = asset_name
        self.height = None
        self.width = None
        self.asset_type = None
        self.asset_data = None
