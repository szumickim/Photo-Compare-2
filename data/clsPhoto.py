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

