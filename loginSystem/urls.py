from django.urls import path
from .views import UserRegister,UserEditView,PasswordChange,password_success
from . import views

urlpatterns = [
  path('register/',UserRegister.as_view(),name='register'),
  path('edit_profile/',UserEditView.as_view(),name='edit_profile'),
  path('password/',PasswordChange.as_view(template_name='registration/change_password.html') ),
  path('password_success/',views.password_success,name='password_success'),
]