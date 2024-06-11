
from django.urls import path
from .views import *

urlpatterns = [
    path('', test_view, name='home'),
    path('login/',login_view, name='login'),
    path('logout/', logout_view, name='logout'),


    path('add-user/', add_user, name='add_user'),
    path('list-users/', list_users, name='list_users'),
    path('user/edit/<int:user_id>/', add_user, name='edit_user'),

    path('add-proveedor/', add_proveedor, name='add_proveedor'),
    path('list-proveedor/', list_proveedor, name='list_proveedor'),
    path('proveedor/edit/<int:prov_id>/', add_proveedor, name='edit_proveedor'),

    path('list-fincas/', list_fincas, name='list_fincas'),
    path('add-fincas/', add_fincas, name='add_fincas'),
    path('add-fincas/edit/<str:fincas_id>/', add_fincas, name='edit_fincas'),

    path('list-bodegas/', list_lotes, name='list_bodegas'),
    path('add-bodegas/', add_lotes, name='add_bodegas'),
    path('add-bodegas/edit/<int:lotes_id>/', add_lotes, name='edit_bodegas'),

    path('list-lotes/', list_bodegas, name='list_lotes'),
    path('add-lotes/', add_bodegas, name='add_lotes'),
    path('add-lotes/edit/<int:bodegas_id>/', add_bodegas, name='edit_lotes'),


    
]