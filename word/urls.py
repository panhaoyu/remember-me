from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

app_name = 'word'
urlpatterns = [
    path('', views.ChangeCurrentLearningSet.as_view(), name='change-current-learning-set'),
    path('detail/<int:pk>', views.DetailView.as_view(), name='detail'),
    path('action/<int:pk>/<slug:action>', views.ActionView.as_view(), name='action'),
    path('list', views.IndexView.as_view(), name='index'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
