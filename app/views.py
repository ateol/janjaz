"""
Definition of views.
"""
from django.utils import timezone
import datetime
from django.shortcuts import render
from django.http import HttpRequest, request, HttpResponse , HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from app.forms import UserProfileForm, EventForm, EventWebsiteForm, EventDetailsForm, EventCommentForm
from app.models import UserProfile, Event, City, EventWebsite, EventDetails, EventComment, University
from django.contrib.auth.decorators import login_required

def home(request):
    context={}
    user=request.user
    context['user']=user
    return render(request, 'app/index.html', context)


def login(request):
    return HttpResponseRedirect('accounts/login')

def SignUp(request):
    return HttpResponseRedirect('accounts/signup')

@login_required
def SignOut(request):
    return HttpResponseRedirect('accounts/logout')

@login_required()
def Profile(request):
    current_user=request.user
    all_users=[]
    for object in UserProfile.objects.all():
        all_users.append(object.user)
    
    if(current_user in all_users):
        return HttpResponseRedirect('/user_profile')
        
    
    context={}
    if request.method=='POST':
        user_profile_form=UserProfileForm(request.POST, request.FILES)

        if user_profile_form.is_valid():
            user_profile=user_profile_form.save()
            if not current_user:
                HttpResponserRedirect('/login')
            else:
                if current_user in all_users:
                    current_profile=UserProfile.objects.get(user=current_user)
                    current_profile=user_profile_form.save()
                    current_profile.user=current_user
                    
                    if 'profile_picture' in request.FILES:
                        current_profile.profile_picture=request.FILES['profile_picture']
                    current_profile.save()
                else:
                    user_profile.user=current_user           
                    if 'profile_picture' in request.FILES:
                        user_profile.profile_picture=request.FILES['profile_picture']
                    
                    user_profile.save()
            return HttpResponseRedirect('/user_profile')
        else:
            print(user_profile_form.is_valid())
            print(user_profile_form.errors)
    else:
        user_profile_form=UserProfileForm()
    context['user_profile_form']=user_profile_form
    return render(request, 'app/profile.html', context)

def CreateEvent(request):
    context={}

    if request.method=='POST':
        event_form=EventForm(request.POST)
        event_website_form=EventWebsiteForm(request.POST)
        event_details_form=EventDetailsForm(request.POST)
        
        if event_form.is_valid():
            event=event_form.save()

            if event_website_form.is_valid():
                event_website=event_website_form.save()
                event.event_website=event_website
        
                if event_details_form.is_valid():
                    event_details=event_details_form.save()
                    event.event_organizer=event_details
                    event.save()
                    return HttpResponseRedirect("/event_thanks")
                else:
                    print (event_details_form.is_valid())
                    print (event_details_form.errors)
            else:
                print (event_website_form.is_valid())
                print (event_website_form.errors)
        else:
            print (event_form.is_valid())
            print (event_form.errors)
    else:
        event_form=EventForm()
        event_website_form=EventWebsiteForm()
        event_details_form=EventDetailsForm()
    context['event_form']=event_form
    context['event_website_form']=event_website_form
    context['event_details_form']=event_details_form

    return render(request, 'app/create_event.html', context)

def UpcomingEvents(request):
    context={}

    upcoming_events=Event.objects.filter(start_time__gte=timezone.now())
    today=datetime.datetime.today()
    one_day=datetime.timedelta(days=1)
    one_week=datetime.timedelta(days=7)
    tommorow=today+one_day
    one_week_later=today+one_week
    one_month_later=today+datetime.timedelta(days=28)

    if len(upcoming_events)> 4:
        upcoming_events=upcoming_events[:4]
    context['upcoming_events']=upcoming_events

    if request.method=='GET':
        city_choices={}
        for city in City.objects.all():
            city_choices[city.name.upper()]=city.name


        values=request.GET
        context['values']=values.items()

        city_to_search=values.getlist('city')
        category_to_search=values.getlist('category')
        date_to_search=values.getlist('date')


        final_list=[]
        for item1, item2, item3 in zip(city_to_search, category_to_search, date_to_search):
            if item1!='' and  item2=='' and item3=='':
                final_list.append(Event.objects.filter(city=item1))
            elif item3=='' and item2!='' and item1!='':
                final_list.append(Event.objects.filter(city=item1, category=item2))
            
            elif item1!='' and item2=='' and item3!='':
                if item3=='in-a-day':
                    final_list.append(Event.objects.filter(city=item1, start_time__lte=tommorow))
                elif item3=='in-a-week':
                    final_list.append(Event.objects.filter(city=item1,start_time__lte=one_week_later))
                elif item3=='in-a-month':
                    print(one_month_later)
                    final_list.append(Event.objects.filter(city=item1, start_time__lte=one_month_later))
            else:
                if item3=='in-a-day':
                    final_list.append(Event.objects.filter(city=item1, category=item2, start_time__lte=tommorow))
                elif item3=='in-a-week':
                    final_list.append(Event.objects.filter(city=item1, category=item2, start_time__lte=one_week_later))
                elif item3=='in-a-month':
                    print(one_month_later)
                    final_list.append(Event.objects.filter(city=item1, category=item2, start_time__lte=one_month_later))

        context['final_list']=final_list
        context['city_choices']=city_choices.items()

    return render(request, 'app/upcoming_events.html', context)

@login_required()
def EventDetails(request,event_id):
    context={}
    current_event=Event.objects.get(pk=event_id)
    current_user=request.user
    current_profile=UserProfile.objects.get(user=current_user)
    context['event']=current_event

    if request.method=="POST":
        event_comment_form=EventCommentForm(request.POST)
        
        if event_comment_form.is_valid():
            event_comment=event_comment_form.save()
            event_comment.author=current_user
            event_comment.author_profile=current_profile
            print (event_comment.author_profile.profile_picture)
            event_comment.save()
            current_event.comments.add(event_comment)
            event_comment.event_set.add(current_event)
            event_comment_form=EventCommentForm()
        else:
            print (event_comment_form.is_valid())
            print (event_comment_form.errors)
    else:
         event_comment_form=EventCommentForm()
    all_comments=None
    comment_count=0
    if current_event.comments.all().exists():
        all_comments=current_event.comments.order_by("-id")
        comment_count=all_comments.count()
    
    context['comment_count']=comment_count
    context['all_comments']=all_comments
    context['event_comment_form']=event_comment_form

    return render(request, 'app/event_details.html', context)

def UnderConstruction(request):
    context={}
    return render(request, 'app/under_construction.html',context)

@login_required
def UserFullProfile(request):
    context={}
    current_user=request.user
    current_user_profile=UserProfile.objects.get(user=current_user)
    current_city=current_user_profile.city_living
    current_upcoming_events=Event.objects.filter(city=current_city)[:3]

    context['user']=current_user
    context['upcoming_events']=current_upcoming_events

    return render(request, 'app/user_profile.html', context)

def EventThanks(request):
    context={}
    return render(request,'app/event_thanks.html', context)


def AllUniversities(request):
    context={}
    all_universities=University.objects.all()
    context['all_universities']=all_universities

    city_choices={}

    for city in City.objects.all():
        city_choices[city.name.upper()]=city.name

    context['city_choices']=city_choices.items()
    
    return render(request, 'app/all_universities.html', context)