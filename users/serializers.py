from rest_framework import serializers
from .models import User
import re

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password',]
        extra_kwargs = {
            'first_name': {'required': True, 'allow_blank': False},
            'last_name': {'required': True, 'allow_blank': False},
            'gender': {'required': True},
            'email': {'required': True, 'allow_blank': False,},
            'username': {'required': True, 'allow_blank': False},
            'phone_number': {'required': True, 'allow_blank': False},
        }
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email already exists.')
        return value
    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError('Phone No already exists.')
        return value
        
        
class UpdatePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$')
        if not pattern.match(value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character."
            )
        
        return value

    def validate(self, data):
        user = self.context['request'].user
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')

        if not user.check_password(old_password):
            raise serializers.ValidationError({"old_password": "Current password is incorrect."})

        if new_password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "New password and confirm password do not match."})

        return data


class SendForgotPasswordOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(required=True)

    def validate_mobile_number(self,value):
        if not User.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError('Unable to process your request. Please check the number and try again.')
        return value



class ForgotPasswordSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    token_otp = serializers.CharField(required=True)   
    
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$')
        if not pattern.match(value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character."
            )
        
        return value

    def validate_confirm_password(self, value):
        new_password = self.initial_data.get('new_password')
        if new_password != value:
            raise serializers.ValidationError("New password and confirm password do not match.")
        return value