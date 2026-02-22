from os import name
from django.urls import path
from . import views

app_name ='user' #to reverse search in tests

urlpatterns = [
    path('create/',views.CreateUserView.as_view(),name='create'),
    path('token/',views.CreateTokenView.as_view(),name="token"),
    path('me/',views.ManageUserView.as_view(),name='me')
]