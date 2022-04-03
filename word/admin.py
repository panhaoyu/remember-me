from django.contrib import admin

from .models import WordModel


# Register your models here.
@admin.register(WordModel)
class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'word', 'translation', 'stage')
    # readonly_fields = ('created_datetime', 'modified_datetime')
