from authapp.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect,HttpResponse
from django.template import RequestContext
from django.shortcuts import render,redirect,render_to_response,get_object_or_404
from models import Person, Dog,Review
from django.views.generic.edit import FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from models import UploadDog,UploadProfile,ReviewForm
from django.contrib import messages
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse_lazy
import json
from django.http import JsonResponse
from .models import Car1, Car2,Booking
from django.core import serializers
import re
    

#views.py

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1']
            )
            person = Person.objects.create(
            email=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            mobilephone=form.cleaned_data['phonenumber'],
            )
            return HttpResponseRedirect('/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
    return render(request, 'registration/register.html', {'form': form})
   

def register_success(request):
    user = Person.objects.get(email=request.user.username)
    print "user: ",user
    if request.method == 'POST':
        upform = UploadProfile(request.POST, request.FILES)

    else:
        upform = UploadProfile()
    return render_to_response(
    'registration/register_success.html',
    )

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')    

@login_required
def add_review(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        user_name = request.user.username
        review = Review()
        review.wine = wine
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        update_clusters()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:wine_detail', args=(wine.id,)))
    
    return render(request, 'reviews/wine_detail.html', {'wine': wine, 'form': form})

@login_required
def home(request):
    review_list = Review.objects.all()     

    email = ''
    provider = None
    user_name = request.user.username
    provider_string = ''
    if user_name != '':
         email = request.user.email
         provider = request.user.social_auth.values_list('provider', flat=True)
         for name in provider:
             provider_string += name.lower().replace('-', '_')

    info = {
         'user_name' : user_name,
         'email' : email,
         'provider' : provider_string
    }
    social = 'facebook'
    print"passord: ", request.user.password
    print "Info: ",info
    if provider_string.encode('utf8') == social:
        # social = user.social_auth.get(provider='facebook')  # or twitter or linkedin
        # print "email: ",social.extra_data['email']
        print "facebookkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk"
      
        if not Person.objects.get(password=request.user.password):
            person = Person.objects.create(
            username=request.user.username,    
            email='',
            password=request.user.password,
            mobilephone='',
            )
            redirect_url = reverse('profile', args=[person.id])
            return HttpResponseRedirect(redirect_url)
        else:
            pnow = Person.objects.get(password=request.user.password)
            print"email: ",pnow.email
            return render(request, 'service.html',{'current_user':pnow,'review_list':review_list})   
    else:
        pnow = Person.objects.get(email=request.user.username)
        # check if user not haveusername or address
        if Person.objects.filter(email=request.user.username,username=''):
            pnow = Person.objects.get(email=request.user.username)
            print "username now is noneeeeeeeeeeeeeeeeeeeeeeeeeee"
            return HttpResponseRedirect('/addInfo') 
       
        return render(request, 'service.html',{'current_user':pnow,'review_list':review_list})
@login_required
def dogprofile(request):
    return render(request, 'dogprofile.html')

@login_required
def contact(request):
    email = ''
    provider = None
    user_name = request.user.username
    provider_string = ''
    if user_name != '':
         email = request.user.email
         provider = request.user.social_auth.values_list('provider', flat=True)
         for name in provider:
             provider_string += name.lower().replace('-', '_')
    social = 'facebook'        
    if provider_string.encode('utf8') == social:
        pnow = Person.objects.get(password=request.user.password)
    else:
        pnow = Person.objects.get(email=request.user.username)


    return render(request, 'contact.html',{'current_user':pnow})

@login_required
def comment_list(request):
    email = ''
    provider = None
    user_name = request.user.username
    provider_string = ''
    if user_name != '':
         email = request.user.email
         provider = request.user.social_auth.values_list('provider', flat=True)
         for name in provider:
             provider_string += name.lower().replace('-', '_')
    social = 'facebook'        
    if provider_string.encode('utf8') == social:
        pnow = Person.objects.get(password=request.user.password)
    else:
        pnow = Person.objects.get(email=request.user.username)

    review_list = Review.objects.all()   

    return render(request, 'service.html',{'current_user':pnow,'review_list':review_list})    

@login_required
def add_comment(request):
   
    email = ''
    provider = None
    user_name = request.user.username
    provider_string = ''
    if user_name != '':
         email = request.user.email
         provider = request.user.social_auth.values_list('provider', flat=True)
         for name in provider:
             provider_string += name.lower().replace('-', '_')
    social = 'facebook'        
    if provider_string.encode('utf8') == social:
        pnow = Person.objects.get(password=request.user.password)
    else:
        pnow = Person.objects.get(email=request.user.username)
    if request.method == 'POST':
        print"add comment"
        user_name = Person.objects.get(email=pnow.email)

        reviewForm = ReviewForm(request.POST,request.FILES)
        if request.POST['star'] is  None:
            star = 0;
        else:
            star = request.POST['star']
        print"star: ",star
        # star_id = request.POST.get('star-5')
        
      
        
        if reviewForm.is_valid():
            # print "reviewForm.cleaned_data['picture']:  ",reviewForm.cleaned_data['picDR']
            # to_update = Review.objects.filter(person=pnow).update(picture=reviewForm.cleaned_data['picture'])
            review = Review.objects.create(
                person = pnow,
                user_name=pnow.username,
                comment = reviewForm.cleaned_data['comment'],
                rating = star,
                picDR=reviewForm.cleaned_data['picDR'],
                )
            print "update review"
            return HttpResponseRedirect('/comment_list')
    else:
        reviewForm = ReviewForm()
    return render(request,'addReviews.html',{'current_user':pnow,'reviewForm':reviewForm}) 

@login_required
def summit_comment(request):
   
    print "submit_comment"
    email = ''
    provider = None
    user_name = request.user.username
    provider_string = ''
    if user_name != '':
         email = request.user.email
         provider = request.user.social_auth.values_list('provider', flat=True)
         for name in provider:
             provider_string += name.lower().replace('-', '_')
    social = 'facebook'        
    if provider_string.encode('utf8') == social:
        pnow = Person.objects.get(password=request.user.password)
    else:
        pnow = Person.objects.get(email=request.user.username)
    
    if request.is_ajax() and request.GET:
        data = request.GET.get('json',False)
        # file1 = request.FILES.get('json')[1]
        # print "file1: ",file1
        
        x = data 
        data =json.loads(data)
        # print "comment: ",data.get('comment')
        print "rate: ",data.get('rate')
        # print "picture: ",data.get('picture')

        # to_update = Review.objects.filter(person=pnow).update(rating=data.get('rate'),comment=data.get('comment'))
        # print "pic: ",request.FILES['imgInp']

        review = Review.objects.create(
                person = pnow,
                user_name=pnow.username,
                comment = '',
                rating = data.get('rate'),
                )

        if to_update:
            print "save create"
    return JsonResponse({'data': x})
  
   

@login_required
def addDogs(request):
    email = ''
    provider = None
    user_name = request.user.username
    provider_string = ''
    if user_name != '':
         email = request.user.email
         provider = request.user.social_auth.values_list('provider', flat=True)
         for name in provider:
             provider_string += name.lower().replace('-', '_')
    social = 'facebook'        
    if provider_string.encode('utf8') == social:
        pnow = Person.objects.get(password=request.user.password)
    else:
        pnow = Person.objects.get(email=request.user.username)
    
    if request.method == 'POST':
        dogOwner = Person.objects.get(email=pnow.email)
        print "dogOwner: ",dogOwner
        dogform = UploadDog(request.POST, request.FILES)
        if dogform.is_valid():
           
            # name = form.cleaned_data['name']
            # weight = form.cleaned_data['weight']
            # allergic = form.cleaned_data['allergic']
            # picDog = form.cleaned_data['picDog']

            dog = Dog.objects.create(
            name=dogform.cleaned_data['name'],
            weight = dogform.cleaned_data['weight'],
            allergic = dogform.cleaned_data['allergic'],
            picDog = dogform.cleaned_data['picDog'],
            dogOwner = dogOwner
            )
            print "dog: ",dog
            # dogform.save()
            return HttpResponseRedirect('/profile')
    else:
        dogform = UploadDog()
    return render(request,'addDogs.html',{'dog':dogform,'current_user':pnow,}) 

def dog_delete(request, pk, template_name='profile.html'):

    item = Dog.objects.get(id=pk)       
    item.delete()
    
    return HttpResponseRedirect('/profile')

def booking_delete(request, pk, template_name='profile.html'):

    item = Booking.objects.get(id=pk)
    split = map(int, re.findall(r'\d+', item.time))
    print "split: ",len(split)
    print "type split ",type(split)
    if item.carNumber =="car1":
        
        for i in range(len(split)):
            carItem = Car1.objects.get(day=item.day,time=split[i])
            carItem.delete()
        # carItem = Car1.objects.get(day=item.day,time=item.time) 

    elif item.carNumber =="car2":
        print"item.time: ",item.time
        for i in range(len(split)):
            carItem = Car2.objects.get(day=item.day,time=split[i])
            carItem.delete()
        # print"item.day: ",item.day
        
    else:
        print"item.carNumber: ",item.carNumber
        print "cannot del"
    item.delete()

    
    return HttpResponseRedirect('/profile')

@login_required
def user_profile(request):
    
    success = False
    email = ''
    provider = None
    user_name = request.user.username
    provider_string = ''
    if user_name != '':
         email = request.user.email
         provider = request.user.social_auth.values_list('provider', flat=True)
         for name in provider:
             provider_string += name.lower().replace('-', '_')
    social = 'facebook'
    if provider_string.encode('utf8') == social:
        user = Person.objects.get(password=request.user.password)
    else:
        user = Person.objects.get(email=request.user.username)
    booking = Booking.objects.filter(user_id=user.id)
    # book= Booking.objects.get(user_id=user.id)
    count = booking.count()
    print"count: ",booking.values('dog').count()
    # jsonDec = json.decoder.JSONDecoder()
    # myPythonList = jsonDec.decode(booking.values_list('dog')[0])
    listofobjs = []
    nameDog = []
   
    for i in range(booking.count()):

        print"booking[j].id: ",booking[i].id
        print"booking[j].day: ",booking[i].day
        day = booking[i].day
        # for x in range(booking.values('dog').count()):
        book_list1 =booking.values_list('dog')[i]
        print "book_list1: ",book_list1
        # print "x: ",x
        ec = book_list1[0].encode('utf8')
        print "ec: ",ec
        dID = map(int, re.findall(r'\d+', ec))
        print"dID: ",len(dID)
        if len(dID)==2:
            dog = Dog.objects.get(id=dID[0])
            dog2 = Dog.objects.get(id=dID[1])
            split = map(int, re.findall(r'\d+', booking[i].time))
            print "split: ",split
            if split[0] == 1:
                t1 = "9:00-11:00 "
            elif split[0] == 2:
                t1= "11:00-13:00 "
            elif split[0] == 3:
                t1= "11:00-13:00 "    
            elif split[0] == 4:
                t1= "11:00-13:00 "
            elif split[0] == 5:
                t1= "11:00-13:00 "
            elif split[0] == 6:
                t1= "19:00-21:00 "

            if split[1] == 1:
                time2 = "9:00-11:00"
            elif split[1] == 2:
                time2= "11:00-13:00 "
            elif split[1] == 3:
                time2= "11:00-13:00 "    
            elif split[1] == 4:
                time2= "11:00-13:00 "
            elif split[1] == 5:
                time2= "11:00-13:00 "
            elif split[1] == 6:
                time2= "19:00-21:00 "    
            temp = t1+time2
            d = {'id':booking[i].id,'day':day+"",'dogName':""+dog.name+" and "+dog2.name,'total':booking[i].total,'time':temp}
        elif len(dID)==1:
            dog = Dog.objects.get(id=dID[0])
            print "booking[i].time: ",booking[i].time
            time = booking[i].time
            if time == '1':
                time1 = "9:00-11:00 "
            elif time == '2':
                time1= "11:00-13:00 "
            elif time == '3':
                time1= "11:00-13:00 "    
            elif time == '4':
                time1= "11:00-13:00 "
            elif time == '5':
                time1= "11:00-13:00 "
            elif time == '6':
                time1= "19:00-21:00 "    
            else:
                print"NOTOIMEEEEEEEEEEEEEEEEEEEEEEEE"

            d = {'id':booking[i].id,'day':day+"",'dogName':""+dog.name,'total':booking[i].total,'time':time1}
         
        listofobjs.append(d)
    print "listofobjs: ",listofobjs
    print "user: ",user
    dog_list = Dog.objects.filter(dogOwner=user)
    if request.method == 'POST':
 

        dogOwner = Person.objects.get(email=user.email)
        print "dogOwner: ",dogOwner
        dogform = UploadDog(request.POST, request.FILES)
        
        if dogform.is_valid():

            dog = Dog.objects.create(
            name=dogform.cleaned_data['name'],
            weight = dogform.cleaned_data['weight'],
            allergic = dogform.cleaned_data['allergic'],
            picDog = dogform.cleaned_data['picDog'],
            dogOwner = dogOwner
            )
            print "dog: ",dog
            # dogform.save()
            return render(request, 'home.html')   
    else:
        # upform = UploadProfile(instance=user.get_profile())  
        upform = UploadProfile()       
        dogform = UploadDog()
    return render(request,'profile.html',{'person':upform,'dog':dogform,'username': request.user.username,'user':user,
        'dog_list':dog_list,'booking':booking,'count':count,'book_list':listofobjs})

def addInfo(request):
    user = Person.objects.get(email=request.user.username)
    print "user: ",user
    if request.method == 'POST':
        upform = UploadProfile(request.POST, request.FILES)

        form = UploadProfile(request.POST, request.FILES)
        print "form username: ",form['username'].value()
        to_update = Person.objects.filter(email=request.user.username).update(username=form['username'].value(),
        address = form['address'].value(),
        )
        print "Add Success"
        return HttpResponseRedirect('/')  

            # up = upform.save(commit=False)
            # up.user = request.user
            # up.save()
            # success = True
    else:
        upform = UploadProfile()
        print "cannot ADD"
    return render(request,'addInfo.html',{'person':upform,}) 

@login_required
def dogList(request):
    dog_list = Dog.object.all()
    return render(request,'addDogs.html') 

class UpdateProfileView(UpdateView):
    queryset = Person.objects.all()
    template_name='update_profile.html'
    fields = ['username','email', 'address','mobilephone', ]
    # picPerson = forms.FileInput(attrs={'id': 'imgInp'}),
    # form_class = UploadProfile
    success_url = '/profile'    

class UpdateDogView(UpdateView):
    queryset = Dog.objects.all()
    template_name='update_dogProfile.html'
    form_class = UploadDog
    success_url = '/profile'



# Create your views here.
def IndexView(request):
    email = ''
    provider = None
    user_name = request.user.username
    provider_string = ''
    if user_name != '':
         email = request.user.email
         provider = request.user.social_auth.values_list('provider', flat=True)
         for name in provider:
             provider_string += name.lower().replace('-', '_')
    social = 'facebook'        
    if provider_string.encode('utf8') == social:
        pnow = Person.objects.get(password=request.user.password)
    
    else:
        pnow = Person.objects.get(email=request.user.username)

    dog = Dog.objects.filter(dogOwner=pnow)
    return render(request, 'booking.html', {'current_user':pnow,'dog' : dog})    

def getTime(request):

    if request.is_ajax() :
        data = request.GET.get('use', False)
        data = json.loads(data)
        daySel = str(data['day'])+"/"+str(data['month'])+"/"+str(data['year'])
        print ("++++++ : "+daySel)
        car1 = Car1.objects.filter(day = daySel)
        car2 = Car2.objects.filter(day = daySel)
        response1 = serializers.serialize("json", car1)
        response2 = serializers.serialize("json", car2)
        count1 = Car1.objects.filter(day=daySel).count()
        count2 = Car2.objects.filter(day=daySel).count()
        print("++++++++++1")
        print(count1)
        print("++++++++++2")
        print(count2)
    
        if(data['la'] >= 14.06810492):
            
            if(count1 <= 0) :
                return HttpResponse(json.dumps({"count": count1,"car":"car1"}), content_type='application/json')
            if(count1 >= 6 and count2 < 6):
                print("+++++++1")
                return HttpResponse(json.dumps({"response": response2,"count": count2,"car":"car2"}), content_type='application/json')
            if(count1 >= 6 and count2 >= 6):
                print("+++++++1.2")
                return HttpResponse(json.dumps({"count": "full","car":"full"}), content_type='application/json')
            print("+++++++1.3")
            return HttpResponse(json.dumps({"response": response1,"count": count1,"car":"car1"}), content_type='application/json')
        else :

            if(count2 <= 0):
                return HttpResponse(json.dumps({"count": count2,"car":"car2"}), content_type='application/json')
            if(count2 >= 6 and count1 < 6 ):
                print("++++++++2")
                return HttpResponse(json.dumps({"response": response1,"count": count1,"car":"car1"}), content_type='application/json')
            if(count2 >= 6 and count1 >= 6):
                print("+++++++2.1")
                return HttpResponse(json.dumps({"count": "full"}), content_type='application/json')
            
            return HttpResponse(json.dumps({"response": response2,"count": count2,"car":"car2"}), content_type='application/json')

   
        
    return JsonResponse({'foo':'bar'})


def submit(request):
 
    if request.is_ajax() and request.GET:
        data = request.GET.get('json', False)
        x = data
        data = json.loads(data)
        user_id = Person.objects.get(id=data.get('user_id'))
        print "data.get('user_id'): ",data.get('user_id')
        print "user_id: ",user_id
        if(data.get('count') == 1):
            day = data.get('day',None)
            time = data.get('time',None)
            if(data.get('car') == 'car1'):
                carNum = Car1.objects.create(day=day, time=time)
                carNum = "car1"
                
            else :
                Car2.objects.create(day=day, time=time)
                carNum ="car2"
                
            Booking.objects.create(user_id=user_id,dog=data.get('dog'),total=data.get('total'),
                               service=json.dumps(data.get('service')),location=data.get('location'),day=day,time=time,carNumber=carNum) 
        else :
            day = data.get('day',None)
            time1 = data.get('time1',None)
            time2 = data.get('time2',None)
            totaltime = "["+time1+","+time2+"]"
            if(data.get('car') == 'car1'):
                Car1.objects.create(day=day, time=time1)
                Car1.objects.create(day=day, time=time2)
                carNum = "car1"
                
            else :
                Car2.objects.create(day=day, time=time1)
                Car2.objects.create(day=day, time=time2)
                carNum = "car2"
            Booking.objects.create(user_id=user_id,dog=json.dumps(data.get('dog')),total=data.get('total'),
                               service=json.dumps(data.get('service')),location=data.get('location'),day=day,time=totaltime,carNumber=carNum
                            )

    return JsonResponse({'data': x})

def service(request):
    review_list = Review.objects.all()  
    email = ''
    provider = None
    user_name = request.user.username
    provider_string = ''
    if user_name != '':
         email = request.user.email
         provider = request.user.social_auth.values_list('provider', flat=True)
         for name in provider:
             provider_string += name.lower().replace('-', '_')
    social = 'facebook'        
    if provider_string.encode('utf8') == social:
        pnow = Person.objects.get(password=request.user.password)
    
    else:
        pnow = Person.objects.get(email=request.user.username)

    dog = Dog.objects.filter(dogOwner=pnow)
       
    return render(request, 'service.html', {'current_user':pnow,'dog' : dog,'review_list':review_list})
    
def receipt(request,data):
    email = ''
    provider = None
    user_name = request.user.username
    provider_string = ''
    if user_name != '':
         email = request.user.email
         provider = request.user.social_auth.values_list('provider', flat=True)
         for name in provider:
             provider_string += name.lower().replace('-', '_')
    social = 'facebook'        
    if provider_string.encode('utf8') == social:
        pnow = Person.objects.get(password=request.user.password)
    
    else:
        pnow = Person.objects.get(email=request.user.username)

    dog = Dog.objects.filter(dogOwner=pnow)
  
    return render(request, 'receipt.html',{'data':data,'current_user':pnow})