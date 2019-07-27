from django.shortcuts import render
from .models import WordModel


# Create your views here.
def index(request):
    word_list = request.session.get('word_list', [])
    word_list = [WordModel.objects.get(id=word) for word in word_list]
    if not word_list:
        word_list = WordModel.get_random(10)
        request.session['word_list'] = [word.id for word in word_list]
    return render(request, 'word/index.html', context={
        'words': word_list,
    })
