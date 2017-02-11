from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
	user = models.OneToOneField(User)
	picture = models.ImageField(upload_to='profile_images', blank=True)

	def __unicode__(self):
		return self.user.username

class Language(models.Model):
	name = models.CharField(max_length=128, unique=True)
	views = models.IntegerField(default=0)
	slug = models.SlugField()

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)

		super(Language, self).save(*args, **kwargs)


	def __unicode__(self):  #For Python 2, use __str__ on Python 3
		return self.name


class Word(models.Model):
	user = models.ManyToManyField(User)
	name = models.CharField(max_length=128, unique=True)
	language = models.ForeignKey(Language)
	views = models.IntegerField(default=0)
	slug = models.SlugField()

	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)

		super(Language, self).save(*args, **kwargs)

	def __unicode__(self):      #For Python 2, use __str__ on Python 3
		return self.name

class Definition(models.Model):
	user = models.ForeignKey(User)
	word = models.ForeignKey(Word)
	definition = models.TextField(blank=True)
	likes = models.IntegerField(default=0)  
	dislikes = models.IntegerField(default=0)
	
	def __unicode__(self):      #For Python 2, use __str__ on Python 3
		return self.definition


