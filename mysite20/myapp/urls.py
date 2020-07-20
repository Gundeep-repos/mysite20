from django.urls import path
from myapp import views
from django.conf.urls import url
app_name = 'myapp'
urlpatterns = [
    path(r'', views.index, name='index'),
    path('about',views.about,name='about'),
    path('<int:top_no>/',views.detail),
    path('courses',views.courses, name='courses'),
    path('placeorder',views.placeOrder,name='placeOrder'),
    path('courses/<int:cour_id>/',views.courseDetail),
    path('myaccount',views.myaccount,name="myaccount"),
    path('login',views.user_login,name="user_login"),
    path('logout',views.user_logout,name="user_logout"),
]
