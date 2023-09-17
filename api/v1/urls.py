from django.urls import include, path
from rest_framework import routers
from profiles.views import ProfileViewSet,ReligionViewSet,CommunityViewSet,EducationViewSet,OccupationViewSet,FamilyDetailsViewSet,AddressViewSet,PreferenceViewSet,PhotoiewSet
from users.views import UserViewSet,UserRegistrationAPIView,UserLoginAPIView
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
router.register(r'photos', PhotoiewSet,basename='photos')
router.register(r'social-media', SocialMediaViewSet,basename='social_media')
router.register(r'social-access-request', SocialLinkAccessRequestViewSet,basename='social_access_request')







urlpatterns = [
    path('', include(router.urls)),    
    path('register/', UserRegistrationAPIView.as_view(), name='user-registration'),
    path('login/', UserLoginAPIView.as_view(), name='user-login'),
]