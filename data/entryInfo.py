ALL_IMAGES: str = "Show all images"


class EntryInfo:
    def __init__(self, excel_path, photo_path, live_preview, continue_work, resize_photo, program_type, elements_in_show_all=20):
        self.excel_path = excel_path
        self.photo_path = photo_path
        self.live_preview = live_preview
        self.continue_work = continue_work
        self.resize_photo = resize_photo
        self.program_type = program_type
        self.elements_on_screen = int(elements_in_show_all)

        if self.program_type == ALL_IMAGES:
            self.resize_photo = None
            self.continue_work = None
        else:
            self.elements_on_screen = 1
