
from rest_framework import viewsets
from safedelete import HARD_DELETE
from .models import User,TempUser
from profiles.models import Profile,Education,Occupation
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Q
from datetime import datetime
from matrimony.utils import generate_otp_with_otpms,verify_otp_with_otpms,send_nms_sms
import random
import re


class UserRegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        password = request.data.get('password',None)
        confirm_password = request.data.get('confirm_password',None)
        phone_number = request.data.get('phone_number',None)


        if password is None or confirm_password is None:
            response_data = {
            'StatusCode':6001,
            'message':"Password and Confirm Password is requird"
            }
            return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE) 

        if password != confirm_password:
            response_data = {
            'StatusCode':6001,
            'message':"Password not match"
            }
            return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE) 
        
        temp_user = TempUser.objects.filter(phone_number=phone_number,is_verified_phone_number=True)

        if not temp_user:
            response_data = {
                'StatusCode':6001,
                'message':"Mobile Number is not verified"
            }
            return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE) 

        if serializer.is_valid():
            user = serializer.save()
            user.set_password(password)
            user.is_active = True
            user.save()
            refresh = RefreshToken.for_user(user)
            response_data = {
                'message':"Registration Successfull",
                'refresh_token': str(refresh),
                'access_token': str(refresh.access_token),
                'user_data':serializer.data
            }
            temp_user.delete(HARD_DELETE)
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginAPIView(APIView):
    def post(self, request, *args, **kwargs):        
        username_or_email = request.data.get('username_or_email',None)
        password = request.data.get('password',None)
        if not username_or_email or not password:
            response_data = {
            'StatusCode':6001,
            'message':"Username/Email and Password is requird"
            }
            return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE) 
        user = User.objects.filter(Q(username=username_or_email)|Q(email=username_or_email)).first()
        response_data = {
            'StatusCode':6001,
            'message':"Username/Email or Password is wrong"
        }
        if not user:
            return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE) 
        
        if not user.check_password(password):
            return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE) 
        refresh = RefreshToken.for_user(user)
        user.last_login = datetime.now()
        user.save()
        profile = Profile.objects.filter(user=user).first()
        profile_id = None
        if profile:
            profile_id = profile.pk
        login_redirection = check_signup_process(profile)
        response_data = {
                'StatusCode':6000,
                'access_token': str(refresh.access_token),
                'user_id':user.pk,
                'profile_id':profile_id,
                'profile_uuid':profile.uuid,
                "redirection_page":login_redirection,
                "has_completed_signup":user.has_completed_signup,
                'message':'Login Successfull..'
        }
        return Response(response_data, status=status.HTTP_201_CREATED)  
    
    

class SendMobileOtpAPIView(APIView):
    def post(self, request, *args, **kwargs):  
        otp_type = "signup_otp"
        mobile_number = request.data.get('phone_number',None)
        pattern = r'^(?:\+91|91)?[6789]\d{9}$'
        if not re.match(pattern, mobile_number):
            response_data = {
                'StatusCode': 6001,
                'message': "Please enter a valid Indian mobile number"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(phone_number=mobile_number).exists():
            response_data = {
                'StatusCode':6001,
                'message':"Mobile number already exists!."
            }
            return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE)
        
        temp_id = random.randint(10000, 99999)
        temp_user = TempUser.objects.filter(phone_number=mobile_number)
        if not temp_user.exists():
            temp_user = TempUser.objects.create(temp_id=temp_id,phone_number=mobile_number)
        else:
            temp_user = temp_user.first()    
        response_data = generate_otp_with_otpms(otp_type,temp_user.temp_id)
        status_code = response_data.get("statusCode")
        if status_code !=200:
            response_data = {
                'StatusCode':response_data.get("statusCode"),
                'message':response_data.get("message")
            }
            return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE) 
        mobile_otp = response_data.get("otp")
        message = "Your OTP for Signup is "+ mobile_otp
        nms_response = send_nms_sms(mobile_number,message)
        nms_response_status = nms_response.get("status")
        if nms_response_status == "error":
            return Response(nms_response, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(nms_response, status=status.HTTP_201_CREATED)  
        


class VerifyMobileOtpAPIView(APIView):
    def post(self, request, *args, **kwargs):  
        mobile_number = request.data.get('phone_number',None)
        mobile_otp = request.data.get('otp',None)
        if not mobile_otp:
            response_data = {
                'StatusCode':6001,
                'message':"Mobile Otp is Required"
            }
            return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE) 
        temp_user = TempUser.objects.filter(phone_number=mobile_number).first()
        if not temp_user:
            response_data = {
                'StatusCode':6001,
                'message':"Otp not created,please tray again"
            }
            return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE)
        temp_id = temp_user.temp_id
        key = "signup_otp_user_"+str(temp_id)
        response_data = verify_otp_with_otpms(key,mobile_otp)
        status_code = response_data.get("statusCode")
        if status_code !=200:            
            return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE)
        temp_user.is_verified_phone_number = True
        temp_user.save()       
        return Response(response_data, status=status.HTTP_201_CREATED) 




class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]






def check_signup_process(profile):
    if not profile:
        return 1
    elif not Education.objects.filter(profile=profile).exists():
        return 2
    elif not  Occupation.objects.filter(profile=profile).exists():        
        return 3   
    elif not hasattr(profile,'family'):
        return 4
    elif not hasattr(profile,'address'):
        return 5
    elif not hasattr(profile,'preference'):
        return 6
    else:
        user = profile.user
        if not user.has_completed_signup:
            user.has_completed_signup = True
            user.save()
        return 7