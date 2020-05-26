from django.urls import path
from . import views

urlpatterns = [
    path('',views.InLog,name='inlog'),
    path('savelogin',views.DrInLog,name='savelogin'),
    path('usersign',views.user_sign,name='usersign'),
    path('userlogin',views.UserInLog,name='userlogin'),
    path('drforget',views.DrForget,name='drforget'),
    path('droutlog/', views.DrOutlog, name='droutlog'),
    path('visit/', views.Visit, name='visit'),
]