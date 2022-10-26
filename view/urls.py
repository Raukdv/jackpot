from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView, TokenVerifyView
)

from . import views

app_name = 'view'

urlpatterns = [
    path('',
        views.HomeView.as_view(), #Home
        name='home'
    ),
    #User block
    path(
        'user/',
        include([
            path(
            'login/',
            views.LoginView.as_view(), #Login
            name='login'
            ),
            path(
                'create/',
                views.UserCreateView.as_view(), 
                name='create_user'
            ),
            path(
                'list/',
                views.UserListView.as_view(), 
                name='list_user'
            ),
            path(
                '<int:pk>/',
                include([
                    path(
                        'detail/',
                        views.UserDetailView.as_view(),
                        name='user_detail'
                    ),
                    path(
                        'delete/',
                        views.UserDeleteView.as_view(),
                        name='user_delete'
                    ),
                    path(
                        'update/',
                        views.UserUpdateView.as_view(),
                        name='user_update'
                    ),
                ]) #End second include for user detail, delete, update
            ),
        ]) #End frist include list and create
    ),   
]