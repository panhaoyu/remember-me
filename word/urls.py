from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'word'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('change-current-learning-set', views.ChangeCurrentLearningSet.as_view(), name='change-current-learning-set'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
