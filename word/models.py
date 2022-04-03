import os

import ebbinghaus
from phy_django import models

EBBINGHAUS_DATABASE = os.path.join(os.path.expanduser('~'), '.remember-me', 'word', 'ebbinghaus.db')
ebbinghaus.set_database(EBBINGHAUS_DATABASE)


# Create your models here.

class WordModel(models.Model):
    class Meta(models.Model.BaseMeta):
        verbose_name = '单词'

    is_active = models.BooleanField(default=True)
    word = models.CharField(max_length=128)
    translation = models.TextField()
    stage = models.SmallIntegerField(verbose_name='学习阶段')

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
    def get_random(cls, length: int) -> list['WordModel']:
        """获取随机的一批词汇。

        Args:
            length: 本批次的词汇量。

        Returns:
           这些词汇对象。
        """
        id_list = ebbinghaus.random(length)
        obj_list = [cls.objects.get(id=obj_id) for obj_id in id_list]
        return obj_list
