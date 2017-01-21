from django.conf.urls import url

from . import views

app_name ='generator'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /generate/
    url(r'^generate/$', views.generate, name='generate'),
]