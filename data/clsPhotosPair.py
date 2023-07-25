from clsPhoto import Photo

class PhotosPair:
    def __init__(self, photo1: Photo, photo2: Photo, similarity_type: str):
        self.photo1 = photo1
        self.photo2 = photo2
        self.similarity_type = similarity_type
        self.better_photo = None