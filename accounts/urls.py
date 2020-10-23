from django.urls import path
from .views import login_view, logout_view, signup_view, select_signup

urlpatterns = [
    path('login/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout_view'),
    path('signup/<user_type>', signup_view, name='signup_view'),
    path('select_signup/', select_signup, name='select_signup'),
]
