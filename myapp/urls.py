from django.urls import path
from myapp import views
from django.conf.urls import url
app_name = 'myapp'
urlpatterns = [
    path(r'', views.index, name='index'),
    path('about',views.about,name='about'),
    path('<int:top_no>/',views.detail),
]
