from strenum import StrEnum
from enum import IntEnum


class ButtonConst(IntEnum):
    NEXT = 1
    CLOSE = 2
    BACK = 3
    GO_TO = 4


class ShowAllConst(StrEnum):
    PRODUCT_ID = 'Product <ID>'
    PHOTO_ID = 'Picture ID'
    PHOTO_REFERENCE = 'Reference'
    HEIGHT = 'Image HEIGHT'
    WIDTH = 'Image WIDTH'


class SummaryConst(StrEnum):
    PRODUCT_ID = '<ID>'
    FIRST_PHOTO_ID = 'Picture ID of 1st duplicate'
    FIRST_REFERENCE = 'Reference 1st duplicate'
    HEIGHT = 'Image HEIGHT'
    WIDTH = 'Image WIDTH'
    SECOND_HEIGHT = '2nd Image HEIGHT'
    SECOND_WIDTH = '2nd Image WIDTH'
    SECOND_PHOTO_ID = 'Picture ID of 2nd duplicate'
    SECOND_REFERENCE = 'Reference 2nd duplicate'
    WORSE = 'Worse Image'
