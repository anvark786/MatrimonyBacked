from django.urls import include, path
from rest_framework import routers
from profiles.views import ProfileViewSet,ReligionViewSet,CommunityViewSet,EducationViewSet,OccupationViewSet,FamilyDetailsViewSet,AddressViewSet,PreferenceViewSet,PhotoViewSet,ProfileInterestViewSet
from users.views import UserViewSet,UserRegistrationAPIView,UserLoginAPIView,SendMobileOtpAPIView,VerifyMobileOtpAPIView,UpdateLoginPasswordAPIView,SendForgotPasswordOTPAPIView,VerifyForgotPasswordOTPAPIView,ForgotPasswordAPIView
from social_meadia.views import SocialMediaViewSet,SocialLinkAccessRequestViewSet

router = routers.DefaultRouter()

router.register(r'users', UserViewSet,basename='users')
router.register(r'profiles', ProfileViewSet,basename='profiles')
router.register(r'religions', ReligionViewSet,basename='religions')
router.register(r'communities', CommunityViewSet,basename='communities')
router.register(r'educations', EducationViewSet,basename='educations')
router.register(r'occupations', OccupationViewSet,basename='occupations')
router.register(r'family-details', FamilyDetailsViewSet,basename='family_details')
router.register(r'address', AddressViewSet,basename='address')
router.register(r'preferences', PreferenceViewSet,basename='preferences')
router.register(r'photos', PhotoViewSet,basename='photos')
router.register(r'social-media', SocialMediaViewSet,basename='social_media')
router.register(r'social-access-request', SocialLinkAccessRequestViewSet,basename='social_access_request')
router.register(r'profile-interests', ProfileInterestViewSet,basename='profile_intrests')



urlpatterns = [
    path('', include(router.urls)),    
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
    path('send-mobile-otp/', SendMobileOtpAPIView.as_view(), name='send-mobile-otp'),
    path('verify-mobile-otp/', VerifyMobileOtpAPIView.as_view(), name='verify-mobile-otp'),
    path('update-login-password/', UpdateLoginPasswordAPIView.as_view(), name='update-login-password'),
    path('send-forgot-password-otp/', SendForgotPasswordOTPAPIView.as_view(), name='send-forgot-password'),
    path('verify-forgot-password-otp/', VerifyForgotPasswordOTPAPIView.as_view(), name='verify-forgot-password'),
    path('forgot-password/', ForgotPasswordAPIView.as_view(), name='forgot-password'),

]