from django.contrib import admin
from .models import SocialLinkAccessRequest,SocialMedia


admin.site.register(SocialMedia)
admin.site.register(SocialLinkAccessRequest)
