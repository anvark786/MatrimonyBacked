from django.db import models
from users.models import User
from matrimony.models import BaseModel
from datetime import date

DISTRICT_CHOICES = (
        ('thiruvananthapuram', 'Thiruvananthapuram'),
        ('kollam', 'Kollam'),
        ('pathanamthitta', 'Pathanamthitta'),
        ('alappuzha', 'Alappuzha'),
        ('idukki', 'Idukki'),
        ('ernakulam', 'Ernakulam'),
        ('thrissur', 'Thrissur'),
        ('palakkad', 'Palakkad'),
        ('malappuram', 'Malappuram'),
        ('kozhikode', 'Kozhikode'),
        ('wayanad', 'Wayanad'),
        ('kannur', 'Kannur'),
        ('kasaragod', 'Kasaragod'),
    )

COMMUNITY = (

    ('','Any'),
    ('A Muslim','A Muslim'),
    ('Ahle Hadees','Ahle Hadees'),
    ('Bohra ','Bohra '),
    ('Deobandi','Deobandi'),
    ('Hanafi','Hanafi'),
    ('Ithna Ashari','Ithna Ashari'),
    ('Jafferi','Jafferi'),
    ('Maliki','Maliki'),
    ('Salafi','Salafi'),    
     ('Shafi','Shafi'),
    ('Sunni','Sunni'),
    ('Wahabi','Wahabi'),    
     ('Jafferi','Jafferi'),
    ('Maliki','Maliki'),
    ('Salafi','Salafi'),
    
)


class Religion(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=35, blank=True,null=True)
    def __str__(self):
        return self.name

class Community(BaseModel):
    name = models.CharField(max_length=100,blank=True,null=True)
    religion = models.ForeignKey(Religion, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Profile(BaseModel):
   
    COMPLEXION_CHOICES = (
        ('very_fair', 'Very Fair'),
        ('fair', 'Fair'),
        ('wheatish', 'Wheatish'),
        ('dark', 'Dark'),
    )  
    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-')
    )
    MARITAL_STATUS_CHOICES = (
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Widowed', 'Widowed'),
    )  
    PHYSICAL_STATUS_CHOICES = (
        ('normal_person', 'Normal Person'),
        ('deaf_or_dumb', 'Deaf/Dumb'),
        ('blind', 'Blind'),
        ('physically_challenged', 'Physically Challenged'),
        ('mentally_challenged', 'Mentally Challenged'),
        ('other_disablity', 'Other Disablity'),


    )    
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_id = models.CharField(max_length=10, unique=True, blank=True,null=True)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.CharField(max_length=15, blank=True,null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    complexion = models.CharField(max_length=30, choices=COMPLEXION_CHOICES,blank=True,null=True)
    blood_group = models.CharField(max_length=30, choices=BLOOD_GROUP_CHOICES,blank=True,null=True)
    community = models.ForeignKey(Community, on_delete=models.CASCADE,blank=True,null=True)   
    marital_status = models.CharField(max_length=30, choices=MARITAL_STATUS_CHOICES,blank=True,null=True)
    physical_status = models.CharField(max_length=30, choices=PHYSICAL_STATUS_CHOICES,blank=True,null=True)
    is_locked_photos = models.BooleanField(default=False)
    is_locked_social_accounts = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        # Update age field based on date_of_birth before saving
        today = date.today()
        age = today.year - self.date_of_birth.year
        if today < date(today.year, self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        self.age = age

        if not self.profile_id:
            last_profile = Profile.objects.order_by('-id').first()
            print("last_profile",last_profile)
            if last_profile:
                last_id = int(last_profile.profile_id[3:])
                new_id = f"SHK{str(last_id + 1).zfill(5)}"
            else:
                new_id = "SHK00001"
            self.profile_id = new_id
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        ordering = ['-created_at']


class Education(BaseModel):
    EDUCATION_CHOICES = (
        ('sslc', 'SSLC'),
        ('pls_two', 'Plus Two'),
        ('degree', 'Bachelor Degree'),
        ('pg', 'Master Degree'),
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='educations')
    name = models.CharField(max_length=15,choices=EDUCATION_CHOICES)  
    institution = models.CharField(max_length=50,blank=True,null=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Occupation(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='occupation')
    profession = models.CharField(max_length=100)  
    company_name = models.CharField(max_length=50,blank=True,null=True)
    job_details = models.TextField(blank=True)
    profession_type = models.CharField(max_length=100)  
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)    

    def __str__(self):
        return self.profile.user.email

class Address(BaseModel):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='address')
    address = models.TextField(blank=True)
    city = models.CharField(max_length=128,blank=True,null=True)
    district =models.CharField(max_length=128,blank=True,null=True)
    street = models.CharField(max_length=128, blank=True,null=True)     
    location = models.CharField(max_length=128, blank=True,null=True)
    post_code = models.CharField(max_length=50, blank=True,null=True)

    def __str__(self):
        return self.profile.user.username

class FamilyDetails(BaseModel):
    FINANCIAL_STATUS_CHOICES = (
        ('ritch', 'Ritch'),
        ('upper', 'Upper Middle Class'),
        ('middle', 'Middle Class'),
        ('lower', 'Lower Middle Class'),
        ('poor', 'Poor'),

    )
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='family')
    financial_status = models.CharField(max_length=50, choices=FINANCIAL_STATUS_CHOICES,blank=True,null=True)
    father_alive =  models.BooleanField(default=True)
    mother_alive =  models.BooleanField(default=True)
    father_occupation = models.CharField(max_length=128,blank=True,null=True)
    mother_occupation = models.CharField(max_length=128,blank=True,null=True)

    no_of_elder_bro = models.IntegerField()
    no_of_younger_bro = models.IntegerField()
    no_of_married_bro = models.IntegerField()

    no_of_elder_sis = models.IntegerField()
    no_of_younger_sis = models.IntegerField()
    no_of_married_sis = models.IntegerField()
    more_details = models.TextField(blank=True,null=True)

    def __str__(self):
        return self.profile.user.email

class Photo(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='photos/')    

    def __str__(self):
        return f"Photo for {self.profile.user.username}"

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'
        ordering = ['-created_at']


class Preference(BaseModel):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ] 
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='preference')
    age_min = models.IntegerField()
    age_max = models.IntegerField()    
    preferred_gender =models.CharField(max_length=1, choices=GENDER_CHOICES,blank=True,null=True)
    preferred_district =models.CharField(max_length=128,blank=True,null=True)
    street = models.CharField(max_length=128, blank=True,null=True)     
    location = models.CharField(max_length=128, blank=True,null=True)
    interests = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Update preferred_gender field based on selected_gender before saving
        selected_gender = self.profile.user.gender       
        if selected_gender:
            if selected_gender == 'M':
                self.preferred_gender = 'F'
            elif selected_gender == 'F':
                self.preferred_gender = 'M'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Preference for {self.profile.user.username}"

    class Meta:
        verbose_name = 'Preference'
        verbose_name_plural = 'Preferences'
        ordering = ['-created_at']


class Interest(BaseModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='interests')
    interested_in = models.OneToOneField(User, on_delete=models.CASCADE, related_name='interested_by')   

    def __str__(self):
        return f"Interest: {self.user.username} is interested in {self.interested_in.username}"

    class Meta:
        verbose_name = 'Interest'
        verbose_name_plural = 'Interests'
        ordering = ['-created_at']



