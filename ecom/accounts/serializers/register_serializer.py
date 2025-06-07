from rest_framework import serializers
from configs.validators import name_validator,phone_validator
from django.contrib.auth import get_user_model
from typing import Dict,Any
from configs.constaints import EMAIL,PASSWORD,FIRST_NAME,LAST_NAME,PHONE
from configs.response_messages import PASSWORD_INVALID_MESS,EMAIL_ALREADY_EX,PHONE_NU_ALREADY_EX
User = get_user_model()



class RegisterSerializer(serializers.ModelSerializer):
  
    first_name = serializers.CharField(required=True,max_length=50,validators=[name_validator])
    last_name = serializers.CharField(required=True,max_length=50,validators=[name_validator])
    phone = serializers.CharField(required=True,validators=[phone_validator])
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True,write_only=True, min_length=6,max_length=20, help_text= PASSWORD_INVALID_MESS)

    class Meta:
        model = User
        fields = [FIRST_NAME,LAST_NAME, PHONE, EMAIL, PASSWORD]

    
    def validate_email(self, value:str)->str:
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(EMAIL_ALREADY_EX)
        return value
    

    def validate_phone(self, value:str)->str:
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError(PHONE_NU_ALREADY_EX)
        return value
    

    def create(self, validated_data:Dict[str, Any]):
        return User.objects.create_user(
            email=validated_data[EMAIL],
            password=validated_data[PASSWORD],
            first_name=validated_data[FIRST_NAME],
            last_name=validated_data[LAST_NAME],
            phone=validated_data[PHONE],
        )

