from django.urls import path
from configs.endpoints import REGISTER_ENDPOINT,LOGIN_ENDPOINT,FORGOT_PASSWORD,VERIFY_OTP_ENDPOINT
from .views import RegisterAPIView,LoginAPIView,ForgotPasswordAPIView,VerifyOtpAPIView

urlpatterns = [
    path(REGISTER_ENDPOINT,RegisterAPIView.as_view(),name="Register"),
    path(LOGIN_ENDPOINT,LoginAPIView.as_view(),name="Login"),
    path(FORGOT_PASSWORD,ForgotPasswordAPIView.as_view(),name="forgot-password"),
    path(VERIFY_OTP_ENDPOINT,VerifyOtpAPIView.as_view(),name="Verify_otp"),
]