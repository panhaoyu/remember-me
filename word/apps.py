import csv
from functools import cached_property
from pathlib import Path
from typing import Type, TYPE_CHECKING

from django.apps import AppConfig
from django.contrib import auth

if TYPE_CHECKING:
    from word.models import WordModel
    from django.contrib.auth.models import User


class WordConfig(AppConfig):
    name = 'word'

    @cached_property
    def word_model(self) -> Type['WordModel']:
        from . import models
        return models.WordModel

    def ready(self):
        user_model: User = auth.get_user_model()
        if not user_model.objects.exclude(username='AnonymousUser').exists():
            user_model.objects.create_superuser('wolf', password='asdglkhwepqdsagphoiqpfasdkjgfaplksj')

        if not self.word_model.objects.exists():
            word_path = Path(r'C:\Users\wolf\OneDrive - 同济大学\3017-博士阶段全过程\220228-复试材料\专业英语\岩土工程专业英语词库.csv')
            with open(word_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            [self.word_model.create_ebbinghaus(k, v) for k, v in csv.reader(lines[1:])]
