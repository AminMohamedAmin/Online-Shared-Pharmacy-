from django.urls import path
from . import views

urlpatterns = [
    path('',views.Home,name='userhome'),
    path('usersearch/',views.Search,name='usersearch'),
    path('ask/',views.Ask,name='ask'),
    path('checkask/',views.CheckAsk,name='checkask'),
    path('message/',views.Contact,name='message'),
]
