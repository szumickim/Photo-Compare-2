ALL_IMAGES: str = "Show all images"

class EntryInfo:
    def __init__(self, program_type=None, elements_in_show_all=20, excel_path='', photo_path='', live_preview=False, continue_work=False, resize_photo=False, data_from_step=False):
        self.excel_path = excel_path
        self.photo_path = photo_path
        self.live_preview = live_preview
        self.continue_work = continue_work
        self.resize_photo = resize_photo
        self.program_type = program_type
        self.elements_on_screen = int(elements_in_show_all)
        self.data_from_step = data_from_step
        self.references_dict = dict()

        if self.program_type == ALL_IMAGES:
            self.resize_photo = None
            self.continue_work = None
        else:
            self.elements_on_screen = 1

    def change_button_variable_to_boolean(self):
        self.live_preview = self.live_preview.get()
        self.resize_photo = self.resize_photo.get()
        self.continue_work = self.continue_work.get()

    def convert_elements_in_show_all(self):
        self.elements_on_screen = int(self.elements_on_screen.get())

    def remove_unused_references_from_dict(self):
        self.references_dict = {k: v for k, v in self.references_dict.items() if v == True}