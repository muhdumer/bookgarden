from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView

app_name='customer_app'

urlpatterns = [
    path('register/',views.SignUpView.as_view(),name='register'),
    path('login/',views.SignInView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('send-activation-link/<uid64>',views.SendAccountActivationLinkView,name="send_activate_link"),
    path('activate/<uid64>/<token>/',views.ActivateUserAccountView,name='activate_user'),
    path('password_reset/',views.PasswordResetClassView.as_view(),name="password_reset"),
    path('password_reset_confirm/<uidb64>/<token>',views.PasswordConfirmClassView.as_view(),name='password_reset_confirm'),
    path('password_reset/done/',TemplateView.as_view(template_name='Password_reset/password_reset_done.html'),name='password_reset_done'),
    path('password_reset_confirm/done/',TemplateView.as_view(template_name='Password_reset/password_reset_confirm_done.html'),name='password_reset_confirm_done'),
    path('myaccount/update-personal-info/',views.UserUpdateView.as_view(),name='my_account_pinfo'),
    path('myaccount/update-password/',views.UserOldPasswordUpdateView.as_view(),name='my_account_password'),
    path('myaccount/new-address/',views.AddressBookCreateView.as_view(),name='my_account_new_address'),
    path('myaccount/addressbook-entries/',views.AddressBookListView.as_view(),name='address_book_list'),
    path('myaccount/<int:pk>/update/',views.AddressBookUpdateView.as_view(),name='address_book_update'),
    path('myaccount/<int:pk>/delete/',views.AddressBookDeleteView.as_view(),name='address_book_delete')
]
