import pandas as pd

from enum import Enum, auto
from PIL import Image as PILImage
from utils import LOG
from io import StringIO

class ContentType(Enum):
    TEXT = auto()
    TABLE = auto()
    IMAGE = auto()

class Content:
    def __init__(self, content_type, original, translation=None):
        self.content_type = content_type
        self.original = original
        self.translation = translation
        self.status = False

    def set_translation(self, translation, status):
        if not self.check_translation_type(translation):
            raise ValueError(f"Invalid translation type. Expected {self.content_type}, but got {type(translation)}")
        self.translation = translation
        self.status = status

    def check_translation_type(self, translation):
        if self.content_type == ContentType.TEXT and isinstance(translation, str):
            return True
        elif self.content_type == ContentType.TABLE and isinstance(translation, pd.DataFrame):
            return True
        elif self.content_type == ContentType.IMAGE and isinstance(translation, PILImage.Image):
            return True
        return False

    def __str__(self):
        return str(self.original)

class TableContent(Content):
    def __init__(self, data, translation=None):
        df = pd.DataFrame(data)
        super().__init__(ContentType.TABLE, df)

    def set_translation(self, translation, status):
        if not isinstance(translation, pd.DataFrame):
            raise ValueError(f"Invalid translation type. Expected DataFrame, but got {type(translation)}")
        self.translation = translation
        self.status = status

    def __str__(self):
        return self.original.to_string(header=True, index=False)

    def iter_items(self, translated=False):
        target_df = self.translation if translated else self.original
        for row_idx, row in target_df.iterrows():
            for col_idx, item in enumerate(row):
                yield (row_idx, col_idx, item)

    def update_item(self, row_idx, col_idx, new_value, translated=False):
        target_df = self.translation if translated else self.original
        target_df.at[row_idx, col_idx] = new_value

    def get_original_as_str(self):
        return self.original.to_string(header=True, index=False)