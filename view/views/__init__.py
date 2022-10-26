from .home.viewhome import (
    HomeView,
)

from .user.viewuser import (
    UserCreateView, UserListView, UserDetailView, UserDeleteView, UserUpdateView
)

from .login.viewlogin import (
    LoginView
)

from .register.viewregister import(
    UserRegisterView
)

__all__ = [
    'HomeView', #Home Views
    'UserCreateView', #User Views
    'UserListView',
    'UserDetailView',
    'UserDeleteView',
    'UserUpdateView',
    'LoginView', #Login View
    'UserRegisterView', #Register View
]
