from functools import cached_property

from django.apps import AppConfig


class WordConfig(AppConfig):
    name = 'word'

    @cached_property
    def models_module(self):
        from . import models
        return models

    def ready(self):
        if not self.models_module.WordModel.objects.exists():

            print(123)
