from django.urls import path
from django.contrib.auth import views as auth_views
from .views import login_view, RegisterView, logout_view, ProfileView,OTPVerificationView,delete_account,account_deleted,delete_account_confirm

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('verify-otp/', OTPVerificationView.as_view(), name='verify_otp'),

]

# password reset for forgetten password and delete account
urlpatterns+=[
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(template_name='views/resetpassword/password_reset_form.html'), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='views/resetpassword/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='views/resetpassword/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='views/resetpassword/password_reset_complete.html'), 
         name='password_reset_complete'),
    path('delete_account/', delete_account, name='delete_account'),
    path('account_deleted/', account_deleted, name='account_deleted'),
    path('delete-account/confirm/', delete_account_confirm, name='delete_account_confirm'),  # URL for confirmation page


]