from django.conf.urls import url

from . import views

app_name = 'fotoxop'

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^upload/$', views.upload, name='upload'),
	url(r'^rotate/', views.rotate, name='rotate'),
	url(r'^invert/', views.invert, name='invert'),
   url(r'^contrast/', views.contrast, name='contrast'),
	url(r'^bright/', views.bright, name='bright'),
	url(r'^color/', views.color, name='color'),
    url(r'^grey/', views.grey, name='grey'),
    url(r'^resize/', views.resize, name='resize'),
    url(r'^channel/', views.channel, name='channel'),
	url(r'^mirror/', views.mirror, name='mirror'),
    url(r'^reset/', views.reset, name='reset'),
]