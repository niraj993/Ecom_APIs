from rest_framework import serializers
from django.contrib.auth import get_user_model
from configs.constaints import EMAIL,USER
from configs.response_messages import EMAIL_DOES_NOT_EX
from typing import Dict,Any

User = get_user_model()


class ForgotPasswordSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)


    class Meta:
        model = User
        fields = [EMAIL]
    
 
    def validate(self,request_payload:Dict[str, Any])->Dict[str, Any]:
        email:str = request_payload[EMAIL]
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(EMAIL_DOES_NOT_EX)
        user = User.objects.get(email=email)
        request_payload[USER] = user
        return request_payload


