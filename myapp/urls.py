from django.urls import path
from myapp import views

app_name = 'myapp'
urlpatterns = [
    path(r'', views.index, name='index'),
	path('about',views.about,name='about'),
    path('<slug:top_no>/',views.detail),
]
