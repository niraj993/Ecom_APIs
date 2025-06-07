from rest_framework import serializers
from ..models import Otp
from typing import Dict,Any
from django.utils import timezone
from datetime import timedelta
from configs.creds import OTP_EXP_MIN
from configs.constaints import OTP
from configs.response_messages import OTP_INVALID_MESS,OTP_EXPIRED_MESS


class VerifySerializer(serializers.ModelSerializer):
    otp = serializers.CharField(required=True)


    class Meta:
        model = Otp
        fields = [OTP]

    
    def validate(self,request_payload:Dict[str,Any]):
        otp = request_payload[OTP]
        try:
            otp_obj = Otp.objects.get(otp=otp)
        except Otp.DoesNotExist:
            raise serializers.ValidationError(OTP_INVALID_MESS)
        
        if timezone.now() > otp_obj.created_at + timedelta(minutes=OTP_EXP_MIN):
            raise serializers.ValidationError(OTP_EXPIRED_MESS)
        return request_payload
        

        
    