from django.urls import path, re_path
from .views import*


urlpatterns = [
    path('role_list_create', RoleListCreate.as_view(), name='RoleListCreate'),
    path('role_retrive_update_delete/<int:pk>', RoleRetriveUpdateDestroy.as_view(),
         name='RoleRetriveUpdateDestroy'),
    path('user-type_list_create', UserTypeListCreate.as_view(),
         name='UserTypeListCreate'),
    path('user-type_retrive_update_delete/<int:pk>', UserTypeRetriveUpdateDestroy.as_view(),
         name='UserTypeRetriveUpdateDestroy'),
    path('reporting_to_list_create', ReportingToListCreate.as_view(),
         name='ReportingToListCreate'),
    path('reporting_to_retrive_update_delete/<int:pk>', ReportingToRetriveUpdateDestroy.as_view(),
         name='ReportingToRetriveUpdateDestroy'),
    path('user_register', UserRegister.as_view(), name='UserRegister'),
    re_path('email-confirm-verify/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)', EmailConfirmVerify.as_view(),
            name='EmailConfirmVerify'),
    path('login', UserLogin.as_view(), name='UserLogin'),
    path('forget_password', ForgetPassword.as_view(), name='ForgetPassword'),

    re_path('reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)', ResetPasswordConfirm.as_view(),
            name='ResetPasswordConfirm'),
]
