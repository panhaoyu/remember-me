from django.contrib import admin

from .models import WordModel


# Register your models here.
@admin.register(WordModel)
class WordAdmin(admin.ModelAdmin):
    list_display = ('id', 'word', 'translation', 'stage', 'is_active')
    search_fields = ('word', 'translation')
    list_filter = ('stage', 'is_active')
    # readonly_fields = ('created_datetime', 'modified_datetime')
