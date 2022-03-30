from phy_django.views import TemplateView

from .models import WordModel


class BaseView(TemplateView):
    site_name = 'Remember Me'


class IndexView(BaseView):
    page_title = '首页'
    page_description = 'Remember Me 的首页'
    template_name = 'word/index.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)

        word_list = self.request.session.get('word_list', [])
        word_list = [WordModel.objects.get(id=word) for word in word_list]
        if not word_list:
            word_list = WordModel.get_random(10)
            self.request.session['word_list'] = [word.id for word in word_list]
        kwargs |= {'words': word_list}

        return kwargs
