from django.http import HttpRequest
from django.urls import reverse_lazy
from django.views import generic
from phy_django.views import RedirectView, ContextMixin

from .models import WordModel


class WordMixin(ContextMixin):
    site_name = 'Remember Me'
    request: HttpRequest


class IndexView(WordMixin, generic.ListView):
    page_title = '即将学习的词汇'
    page_description = 'Remember Me 的首页'
    template_name = 'word/index.html'

    def get_queryset(self):
        word_ids = self.request.session.get('word_list', [])
        if word_ids:
            word_list = WordModel.objects.filter(id__in=word_ids)
        else:
            word_list = WordModel.objects.order_by('stage')[:10]
        self.request.session['word_list'] = [w.id for w in word_list]
        self.request.session['word_index'] = 0
        return word_list


class ChangeCurrentLearningSet(RedirectView):
    """
    程序通过session来记录当前的学习列表，本视图用于重新进行一次随机，生成一批学习列表。
    """
    url = reverse_lazy('word:index')

    def get(self, request, *args, **kwargs):
        self.request.session.pop('word_list', None)
        return super().get(request, *args, **kwargs)
