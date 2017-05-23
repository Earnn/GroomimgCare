from __future__ import unicode_literals
from django.db import models
from django.forms import ModelForm, Textarea,TextInput,FileInput,ChoiceField
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.
class Image(models.Model):
	"""docstring for Image"""
	image=models.ImageField(upload_to='images')
	description=models.CharField(max_length=100,blank=True,null=True)

		
class Person(models.Model):	
	"""docstring for Event"""

	username=models.CharField(max_length=200,blank=True,null=True,default="")
	email= models.EmailField(max_length=200,blank=False,null=True)
	address = models.CharField(max_length=1000,blank=False,null=False)
	password=models.CharField(max_length=200,blank=False,null=False)
	mobilephone = models.CharField(max_length=200,blank=False,null=False)
	def __unicode__(self):# __unicode__ on Python 2
		return "%s" % (self.id)


class Dog(models.Model):
	"""docstring for Dog"""
	CHOICES = (
        ('Small', 'Less than 15'),
        ('Big', 'More than 15'),
    )
	name=models.CharField(max_length=200,blank=True,null=True,default="")
	weight= models.CharField(max_length=100,blank=False,null=False,choices=CHOICES)
	allergic=models.CharField(max_length=200,blank=True,null=True,default="")
	picDog=models.FileField(upload_to="documents/",default="")
	dogOwner= models.ForeignKey(Person,on_delete=models.CASCADE,null=True)


class Review(models.Model):
    RATING_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    person = models.ForeignKey(Person,on_delete=models.CASCADE,null=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    user_name = models.CharField(max_length=200,null=True,default="")
    comment = models.CharField(max_length=200)
    rating = models.IntegerField()
    picDR = models.ImageField(upload_to="documents/",default="")

class UploadProfile(ModelForm):
    class Meta:
        model = Person
        fields = [
			"username",
			"email",
			"address",
			"password",
			"mobilephone",
		
			
        ]
       	widgets = {
            'address': TextInput(attrs={'id':'a'}),
            'username': TextInput(attrs={'id':'u'}),
            

        }
class UploadDog(ModelForm):
    class Meta:
        model = Dog
        fields = [
			"name",
			"weight",
			"allergic",
			"picDog"
			
        ]
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Name'}),
            'allergic': TextInput(attrs={'placeholder': 'Allergic'}),
            'picDog': FileInput(attrs={'id': 'imgInp'}),
            
        }

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = [ 'picDR','comment']
        widgets = {
            
            'comment': Textarea(attrs={'cols': 5, 'rows': 5,'placeholder': "Comment and Share your happy dog's photo."}),
            'picDR': FileInput(attrs={'id': 'imgInp'}),
        }
        
class Car1(models.Model):   
    """docstring for Event"""
    # booking_id=models.ForeignKey(Booking,on_delete=models.CASCADE,null=True)
    day=models.CharField(max_length=10,blank=False,null=False,default="")
    time=models.CharField(max_length=10,blank=False,null=False,default="")


class Car2(models.Model):   
    """docstring for Event"""
    # booking_id=models.ForeignKey(Booking,on_delete=models.CASCADE,null=True)
    day=models.CharField(max_length=10,blank=False,null=False,default="")
    time=models.CharField(max_length=10,blank=False,null=False,default="")

class Booking(models.Model):
    # user=models.CharField(max_length=10,blank=False,null=False,default="")
    user_id=models.ForeignKey(Person,on_delete=models.CASCADE,null=True)
    dog=models.TextField(max_length=10,blank=False,null=False,default="")
    total=models.FloatField(max_length=10,blank=False,null=False,default="")
    service=models.TextField(max_length=100,blank=False,null=False,default="")
    location=models.CharField(max_length=1000,blank=False,null=False,default="")
    day=models.CharField(max_length=10,blank=False,null=False,default="")
    time=models.CharField(max_length=10,blank=False,null=False,default="")
    carNumber = models.CharField(max_length=10,blank=False,null=False,default="")
