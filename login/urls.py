from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='home'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('edit',views.edit,name='edit'),
    path('dashboard',views.dash,name='dashboard'),
    path('order',views.hos_order,name='order'),
    path('avail_orders',views.avail_orders,name='avail_orders'),
    path('vaccept',views.vaccept,name='vaccept'),
    path('taccept',views.taccept,name='taccept'),
    path('pickup',views.pickup,name='pickup'),
    path('drop',views.drop,name='drop'),
    path('myorders',views.myorders,name='myorders'),
    path('sos',views.sos,name='sos'),
]