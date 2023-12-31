
from rest_framework import viewsets
from .models import User
from profiles.models import Profile
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.views import APIView
from django.db.models import Q
from datetime import datetime


class UserRegistrationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        password = request.data.get('password',None)
        confirm_password = request.data.get('confirm_password',None)

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
        profile_id = Profile.objects.filter(user=user).first()
        if profile_id:
            profile_id = profile_id.pk
        response_data = {
                'StatusCode':6000,
                'access_token': str(refresh.access_token),
                'user_id':user.pk,
                'profile_id':profile_id,
                'message':'Login Successfull..'
        }
        return Response(response_data, status=status.HTTP_201_CREATED)  
        
       

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
