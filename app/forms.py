from django import forms
from django.contrib.auth.models import User
from app.models import UserProfile, City, Event, EventWebsite , EventDetails, EventComment
from datetimewidget.widgets import DateTimeWidget

class UserProfileForm(forms.ModelForm):
   
    
    class Meta:
        living_in_turkey_choices=(
        ('YES', 'Yes'),
        ('NO', 'no'), 
        )

        country_of_origin_choices=(
            ('KENYA', 'Kenya'),
            ('UGANDA', 'Uganda'),
            ('SOUTH SUDAN', 'South Sudan'),
            ('CAMEROON', 'Cameroon'),
            ('MADAGASCAR','Madagascar'),
            )

        city_living_choices=()

        for city in City.objects.all():
            item=((city.name.upper(),)+(city.name,),)
            city_living_choices+=item
            item=()

        status_choices=(
            ('SINGLE', 'Single'),
            ('IN_A_RELATIONSHIP', 'In a Relationship'),
            ('MARRIED_WITH_KIDS', 'Married With Kids'),
            ('SINGLE_WITH_KIDS', 'Single With Kids'),
            )
        gender_choices=(
            ('MALE', 'Male'),
            ('FEMALE', 'Female'),
            )

        occupation_choices=(
            ('STUDENT', 'Student'),
            ('EMPLOYED', 'Employed'),
            ('JOB_SEEKERS', 'Job Seekers'),
            ('SELF_EMPLOYED', 'Self Employed'),
            ('ENTREPRENUER', 'Entreprener'),
            ('RETIRED', 'Retired'),
            ('TRAINEE', 'Trainee'),
            )

        model=UserProfile
        fields=['living_in_turkey', 'country_of_origin', 'city_living', 'profile_picture',
                'gender', 'status', 'about_yourself','interests', 'languages', 'occupation',
                ]
        widgets={
            'living_in_turkey': forms.RadioSelect(choices=living_in_turkey_choices),
            'country_of_origin': forms.Select(choices=country_of_origin_choices),
            'city_living': forms.Select(choices=city_living_choices),
            'profile_picture': forms.FileInput(attrs={'class': 'file_input'}),
            'gender': forms.RadioSelect(choices=gender_choices),
            'status':forms.Select(choices=status_choices),
            'about_yourself': forms.Textarea(),
            'interests': forms.Textarea(),
            'languages': forms.Textarea(),
            'occupation': forms.Select(choices=occupation_choices)
            }
 
class EventForm(forms.ModelForm):
   
    class Meta:
        category_choices=(
            ('BUSINESS', 'Business'),
            ('CULTURE_ART', 'Culture and Art'),
            ('EDUCATION', 'Education')
        )

        city_choices=()

        for city in City.objects.all():
            item=((city.name.upper(),)+(city.name,),)
            city_choices+=item
            item=()
        
        event_privacy_choices=(
            ('PUBLIC_EVENT', 'Public Event'),
            ('PRIVATE_EVENT', 'Private Event'),
            ('INVITED_ONLY', 'Invited Only'),
        )
        model=Event
        fields=['category', 'title', 'description', 'event_privacy', 'city', 'event_venue', 'start_time', 'end_time']

        widgets={
            'category': forms.Select(choices=category_choices),
            'description': forms.Textarea(attrs={'rows': 5}),
            'event_privacy': forms.Select(choices=event_privacy_choices),
            'city':forms.Select(choices=city_choices),
            'start_time': DateTimeWidget(usel10n=True, bootstrap_version=3),
            'end_time': DateTimeWidget(usel10n=True, bootstrap_version=3)
        }

class EventWebsiteForm(forms.ModelForm):
    
    class Meta:
        model=EventWebsite
        fields=['event_website']


class EventDetailsForm(forms.ModelForm):
    
    class Meta:
        model=EventDetails
        fields=['contact_name', 'company_name', 'address', 'phone_number', 'email', 'organisers_website']
        widgets={
            'address': forms.Textarea(attrs={'rows': 5})
        }

class EventCommentForm(forms.ModelForm):
     
     class Meta:
         model=EventComment
         fields=['comment_text',]
         
         widgets={
             'comment_text': forms.Textarea(attrs={'rows': 5}),
         }