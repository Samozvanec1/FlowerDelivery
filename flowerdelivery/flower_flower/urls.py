from django.urls import path
from . import views
from .models import Flower

urlpatterns = [
    path('', views.index, name='index'),
]
for flower in Flower.objects.all():
    urlpatterns.append(path(f'flowers/{flower.id}/', views.flower, name=f'flower_{flower.id}'))
    urlpatterns.append(path(f'buying/{flower.id}/', views.buying, name=f'buying_{flower.id}'))