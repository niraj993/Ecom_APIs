from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from typing import Dict,Any
from configs.constaints import USER,EMAIL,PASSWORD
from configs.response_messages import EMAIL_DOES_NOT_EX,INVALID_CREDS_MESS,PASSWORD_INVALID_MESS

User = get_user_model()


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True,write_only=True, min_length=6,max_length=20, help_text=PASSWORD_INVALID_MESS)

    
    class Meta:
        model = User
        fields = [EMAIL,PASSWORD]


    def validate(self,request_payload:Dict[str, Any])->Dict[str, Any]:
        email:str = request_payload[EMAIL]
        password:str = request_payload[PASSWORD]
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError(EMAIL_DOES_NOT_EX)
        user = authenticate(email=email,password=password)
        if not user:
            raise serializers.ValidationError(INVALID_CREDS_MESS)
        request_payload[USER] = user
        return request_payload
        

        

        

        




    


