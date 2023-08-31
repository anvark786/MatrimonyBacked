from django.db.models import Q
from .models import Profile, Preference

def get_matching_profiles(profile_pk):
    # Get the user's preference
    try:
        preference = Preference.objects.get(profile__pk=profile_pk)
    except Preference.DoesNotExist:
        # Handle case where preference does not exist for the user
        return []

    # Retrieve profiles that match the user's preferences
    matching_profiles = Profile.objects.filter(
        ~Q(pk=profile_pk),
        Q(age__gte=preference.age_min) &  # Minimum age
        Q(age__lte=preference.age_max) & # Maximum age
        Q(user__gender=preference.preferred_gender) | # Preferred gender
        Q(address__district=preference.preferred_district) | Q(address__district='')| # Preferred district or any district
        Q(address__street=preference.street) | Q(address__street='')| # Preferred street or any street
        Q(address__location=preference.location) | Q(address__location='') # Preferred location or any location
    )

    return matching_profiles
