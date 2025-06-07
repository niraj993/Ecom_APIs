from .serializers.register_serializer import RegisterSerializer
from .serializers.login_serializer import LoginSerializer
from .serializers.forgot_password import ForgotPasswordSerializer
from .serializers.verify_otp_serializer import VerifySerializer
from rest_framework.views import APIView
from django.http import HttpRequest
from rest_framework.response import Response
from configs.constaints import ERROR,MESSAGE,STATUS_CODE,USER_ID,REFRESH_TOKEN,ACCESS_TOKEN,DATA,USER
from configs.response_messages import REGISTER_MESS,REGISTER_FAIL_MESS,LOGIN_MESS,LOGIN_FAILED_MESS,OTP_MESS,FAILED_TO_OTP_MESS,OTP_VERIFIED_MESS,OTP_VERIFIED_FAILED_MESS
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.timezone import now
from services.email_service import send_otp_email,generate_otp
from .models import Otp




class RegisterAPIView(APIView):
    def post(self,request:HttpRequest)->Response:
        try:
            register_serializer  = RegisterSerializer(data=request.data)
            if register_serializer.is_valid():
                register_serializer.save()
                return Response({STATUS_CODE:201,MESSAGE:REGISTER_MESS,DATA:register_serializer.data})
            return Response({STATUS_CODE:500,MESSAGE:REGISTER_FAIL_MESS,ERROR:register_serializer.errors})
        
        except Exception as e:
            return Response({ERROR:str(e),STATUS_CODE:500})



class LoginAPIView(APIView):
    def post(self,request:HttpRequest)->Response:
        try:
            login_serializer = LoginSerializer(data=request.data)
            if login_serializer.is_valid():
                user = login_serializer.validated_data[USER]
                user.last_login = now()
                user.save(update_fields=["last_login"])
                refresh_token = RefreshToken.for_user(user=user)
                return Response({MESSAGE:LOGIN_MESS,STATUS_CODE:200,REFRESH_TOKEN:str(refresh_token),ACCESS_TOKEN:str(refresh_token.access_token),USER_ID:user.id})
            return Response({MESSAGE:LOGIN_FAILED_MESS,STATUS_CODE:500,ERROR:login_serializer.errors})
        
        except Exception as e:
            return Response({ERROR:str(e),STATUS_CODE:500})
        


class ForgotPasswordAPIView(APIView):

    def post(self,request:HttpRequest)->Response:
        try:
            forgot_serializer = ForgotPasswordSerializer(data=request.data)
            if forgot_serializer.is_valid():
                user = forgot_serializer.validated_data[USER]
                otp = generate_otp()
                otp_obj = Otp.objects.filter(user_id=user.id).order_by('-created_at').first()
                if otp_obj:
                    otp_obj.otp = otp
                    otp_obj.updated_at = now()
                    otp_obj.save()
                else:
                    Otp.objects.create(user=user, otp=otp)

                send_otp_email(to_email=user.email,name=user.first_name,otp=otp)
                return Response({MESSAGE:OTP_MESS,STATUS_CODE:200,USER_ID:user.id})
            
            return Response({MESSAGE:FAILED_TO_OTP_MESS,ERROR:forgot_serializer.errors,STATUS_CODE:500})
        except Exception as e:
            return Response({ERROR:str(e),STATUS_CODE:500})


    

class VerifyOtpAPIView(APIView):
    def post(self, request:HttpRequest)->Response:
        try:
            verify_serializer = VerifySerializer(data=request.data)
            if verify_serializer.is_valid():
                return Response({MESSAGE:OTP_VERIFIED_MESS,STATUS_CODE:200})
            return Response({MESSAGE:OTP_VERIFIED_FAILED_MESS,ERROR:verify_serializer.errors,STATUS_CODE:500})
        except Exception as e:
            return Response({ERROR:str(e),STATUS_CODE:500})

                    