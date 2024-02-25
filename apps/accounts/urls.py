from django.urls import path
from .views import SignupView,AccountLoginView,LogoutUserView

app_name = 'accounts'

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('', AccountLoginView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
]