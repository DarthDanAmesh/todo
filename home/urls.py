from django.urls import include, path
from django.contrib.auth.views import LoginView, LogoutView

from .views import IndexView, RegisterUser, mzalendo_list_view, ActivateView, MzalendoEdit, mzalendo_create_view, mzalendo_detail_cpy,MzalendoDetail, quick_edit
from . import views
# this is a namespace which allows mzalendo:login and equivalent to {% url 'mzalendo:login' %} to work
app_name = 'mzalendo'

urlpatterns = [
    #path('', IndexView.as_view(template_name='mzalendo/mzalendo_list.html'), name='index'),
    path('', views.mzalendo_list_view, name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
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
        "mzalendo/<int:pk>/edit",
        MzalendoEdit.as_view(),
        name="mzalendo_edit",
    ),
    path(
        "mzalendo/<int:pk>/",
        views.delete_comment,
        name="delete-comment", #check models for the name
    ),
]
