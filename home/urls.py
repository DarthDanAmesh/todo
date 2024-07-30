from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import IndexView, register, mzalendo_list_view, mzalendo_create_view, mzalendo_detail_cpy,MzalendoDetail, quick_edit
from . import views
# this is a namespace which allows mzalendo:login and equivalent to {% url 'mzalendo:login' %} to work
app_name = 'mzalendo'

urlpatterns = [
    #path('', IndexView.as_view(template_name='mzalendo/mzalendo_list.html'), name='index'),
    path('', views.mzalendo_list_view, name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    #name corresponds to the url in the template tag
    path('mzalendo/', views.mzalendo_list_view, name='mzalendo_list'),
    path('mzalendo/create/', views.mzalendo_create_view, name='mzalendo_create'),
    path('mzalendo/<int:pk>/', MzalendoDetail.as_view(), name='mzalendo_detail'),
    path(
        "mzalendo/<int:pk>/quickedit",
        views.quick_edit,
        name="quick-edit",
    ),
    path(
        "mzalendo/<int:pk>/",
        views.delete_comment,
        name="delete-comment", #check models for the name
    ),
]
