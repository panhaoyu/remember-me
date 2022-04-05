from functools import cached_property
from typing import Optional

from django.http import HttpRequest
from django.urls import reverse_lazy
from django.views import generic
from phy_django.views import RedirectView, ContextMixin

from .models import WordModel


class WordMixin(ContextMixin):
    site_name = 'Remember Me'
    request: HttpRequest

    @cached_property
    def word_list(self):
        word_ids = self.request.session.get('word_list', [])
        if word_ids:
            word_list = WordModel.objects.filter(id__in=word_ids, is_active=True)
        else:
            word_list = WordModel.objects.order_by('stage')[:10]
        self.request.session['word_list'] = [w.id for w in word_list]
        return word_list

    @cached_property
    def current_word(self) -> Optional[WordModel]:
        """当前正在学习的词汇，对于列表页是第0个词，对于第1页是第0个词，对于第2页是第1个词"""
        current_word = self.request.session.get('word_index', 0)
        if current_word < 10:
            current_word = self.word_list[current_word]
        else:
            current_word = None
        return current_word

    @cached_property
    def next_word(self) -> Optional[WordModel]:
        word = self.request.session.get('word_index', 0) + 1
        if word < 10:
            word = self.word_list[word]
        else:
            word = None
        return word

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {
            **context,
            'current_word': self.current_word,
            'next_word': self.next_word,
            'word_list': self.word_list,
        }


class IndexView(WordMixin, generic.ListView):
    page_title = '即将学习的词汇'
    page_description = 'Remember Me 的首页'
    template_name = 'word/index.html'

    def get_queryset(self):
        self.request.session['word_index'] = 0
        return self.word_list


class DetailView(WordMixin, generic.DetailView):
    template_name = 'word/detail.html'
    model = WordModel


class ChangeCurrentLearningSet(WordMixin, RedirectView):
    """
    程序通过session来记录当前的学习列表，本视图用于重新进行一次随机，生成一批学习列表。
    """

    def get_redirect_url(self, *args, **kwargs):
        self.request.session.pop('word_list', None)
        return reverse_lazy('word:detail', args=(self.current_word.id,))


class ActionView(
    generic.detail.SingleObjectMixin,
    WordMixin, RedirectView,
):
    model = WordModel

    def get_redirect_url(self, *args, **kwargs):
        action: str = kwargs.get('action')
        obj: ActionView.model = self.get_object()
        match action:
            case 'remember':
                score = 1
            case 'forget':
                score = -2
            case 'not-seen':
                score = -1
            case 'inactive':
                score = 0
                obj.is_active = False
            case _:
                raise ValueError('No such action')
        stage = obj.stage + score
        stage = 0 if stage < 0 else stage
        obj.stage = stage
        obj.save()
        if self.next_word:
            self.request.session['word_index'] += 1
            return reverse_lazy('word:detail', args=(self.next_word.id,))
        else:
            # 处理这一整批的数据
            return reverse_lazy('word:index')
