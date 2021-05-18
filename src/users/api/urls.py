from django.urls import path, re_path
from .views import*


urlpatterns = [
    path('role_list_create', RoleListCreate.as_view(), name='RoleListCreate'),
    path('role_retrive_update_delete/<int:pk>', RoleRetriveUpdateDestroy.as_view(),
         name='RoleRetriveUpdateDestroy'),
    path('user-type_retrive_update_delete/<int:pk>',
         UserTypeRetriveUpdateDelete.as_view(), name='user-type-retrive-update-delete'),

    path('user-type_list_create', UserTypeListCreate.as_view(),
         name='UserTypeListCreate'),

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
    path('change_password', ChangePassword.as_view(), name='ChangePassword'),
    path('logged-in-user-detail', LoggedIn.as_view(), name='LoggedIn'),
    path('add-user', AddUser.as_view(), name='AddUser'),
    path('generate_otp', GenerateOTP.as_view(), name='GenerateOTP'),
    path('otp_verification', OTPVerification.as_view(), name='OTPVerification'),

    path('bulk-upload/add-account', AddAccount.as_view(), name='Add Account'),
    path('bulk-upload/add-school', AddSchool.as_view(), name='Add School'),
    path('bulk-upload/add-school-grade-subject',
         AddSchoolGradeSubject.as_view(), name='Add School Grade Subject'),
    path('bulk-upload/add-user', AddUserData.as_view(), name='AddUserData'),


]
