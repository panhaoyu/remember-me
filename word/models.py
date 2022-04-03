import os

import ebbinghaus
from django.db import models

EBBINGHAUS_DATABASE = os.path.join(os.path.expanduser('~'), '.remember-me', 'word', 'ebbinghaus.db')
ebbinghaus.set_database(EBBINGHAUS_DATABASE)


# Create your models here.

class WordModel(models.Model):
    word = models.CharField(max_length=128)
    translation = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    modified_datetime = models.DateTimeField(auto_now=True)

    @classmethod
    def create_ebbinghaus(cls, word, translation):
        obj = WordModel.objects.create(word=word, translation=translation)
        try:
            ebbinghaus.register(obj.id)
        except:
            pass

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not ebbinghaus.exists(self.id):
            ebbinghaus.register(self.id)

    @classmethod
    def get_random(cls, length):
        id_list = ebbinghaus.random(length)
        obj_list = [cls.objects.get(id=obj_id) for obj_id in id_list]
        return obj_list

    @property
    def stage(self):
        return ebbinghaus.get_stage(self.id)
