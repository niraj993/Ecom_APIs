from django.core.validators import RegexValidator


name_validator = RegexValidator(regex=r'^[A-Za-z\s]+$',message="Name must contain only alphabets and spaces. No numbers or special characters allowed.")
phone_validator = RegexValidator(regex=r'^[6-9]\d{9}$',message="Enter a valid 10-digit Indian phone number.")