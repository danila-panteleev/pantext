from django.urls import include, path
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    path('', views.index, name='main'),
    path('contacts', views.contacts, name='contacts'),
    path('yandex_2076966e8ed47beb.html', TemplateView.as_view(template_name='main/yandex_2076966e8ed47beb.html')),
    path('sitemap.xml', TemplateView.as_view(template_name='main/sitemap.xml')),
    path('robots.txt', TemplateView.as_view(template_name='main/robots.txt')),


]
