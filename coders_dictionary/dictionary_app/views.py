from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User 
from models import Language, Definition, Word, UserProfile
from forms import DefinitionForm, WordForm, UserForm, UserProfileForm, ContactForm, PasswordRecoveryForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import FormView
from django.core.urlresolvers import reverse_lazy 
from django.contrib.auth import update_session_auth_hash 
# from braces.views import LoginRequiredMixin



# Create your views here.
def index(request):
	context_dict = {}
	#request.session.set_test_cookie()
	#if request.session.test_cookie_worked():
	#	print ">>>TEST COOKIE WORKED"
	#	request.session.delete_test_cookie()


	language_list = Language.objects.order_by('-views')[:5]
	
	context_dict['languages'] = language_list
	word_list = Word.objects.order_by('-likes')[:5]
	context_dict['words'] = word_list

	#visits = int(request.COOKIES.get('visits', '1'))
	visits =  request.session.get('visits')

	if not visits:
		visits = 1

	reset_last_visit_time = False

	#if 'last_visit' in request.COOKIES:
	#	last_visit = request.COOKIES['last_visit']
	last_visit = request.session.get('last_visit')
	if last_visit:
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

		if (datetime.now() - last_visit_time).days > 0:
			visits =  visits + 1 
			reset_last_visit_time = True

	else:
		reset_last_visit_time = True

	if reset_last_visit_time:
		#response.set_cookie('last_visit', datetime.now())
		#response.set_cookie('visits', visits)
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = visits

	context_dict['visits'] = visits 	
	response = render(request, 'index.html', context_dict)
	
	return response



def about(request):

	context_dict = {}

	if request.session.get('visits'):
		count = request.session.get('visits')
	else: count = 0

	count = count + 1
	context_dict['visits'] = count 

	return render(request, 'about.html', context_dict)




def language(request, language_name_slug):
	context_dict = {}
	context_dict['result_list'] = None
	context_dict['query'] = None

	if request.method == 'POST':
		query = request.POST['query'].strip()

	try:
		language = Language.objects.get(slug=language_name_slug)
		words = Word.objects.filter(language=language)

		context_dict['language'] = language
		context_dict['words'] = words

	except Language.DoesNotExist:
		pass

	return render(request, 'language.html', context_dict)

def Word(request, word_name_slug):
	context_dict = {}
	context_dict['result_list'] = None
	context_dict['query'] = None

	language_list = Language.objects.order_by('-views')[:5]
	context_dict['languages'] = language_list

	if request.method == 'POST':
		query = request.POST['query'].strip()

	try:
		word = Language.objects.get(slug=word_name_slug)
		definitions = Definition.objects.filter(word=word)

		
		context_dict['word'] = word
		def_list = Definition.objects.order_by('-likes')[:5]
		context_dict['definitions'] = definitions

	except Language.DoesNotExist:
		pass

	visits =  request.session.get('visits')

	if not visits:
		visits = 1

	reset_last_visit_time = False

	#if 'last_visit' in request.COOKIES:
	#	last_visit = request.COOKIES['last_visit']
	last_visit = request.session.get('last_visit')
	if last_visit:
		last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

		if (datetime.now() - last_visit_time).days > 0:
			visits =  visits + 1 
			reset_last_visit_time = True

	else:
		reset_last_visit_time = True

	if reset_last_visit_time:
		#response.set_cookie('last_visit', datetime.now())
		#response.set_cookie('visits', visits)
		request.session['last_visit'] = str(datetime.now())
		request.session['visits'] = visits

	context_dict['visits'] = visits	
	return render(request, 'word.html', context_dict)

def add_language(request):
	if request.method == 'POST':
		form = LanguageForm(request.POST)
		if form.is_valid():
			lang = form.save(commit=False)
			lang.save()

			return index(request)
		else:
			print form.errors
	else:
		form = LanguageForm()

	return render(request, 'add_Language.html', {'form':form})

@login_required
def add_word(request, language_name_slug):
	try:
		lang =  Language.objects.get(slug=category_name_slug)
	except Language.DoesNotExist:
		lang = None 

	if request.method == 'POST':
		form =  WordForm(request.POST)

		if form.is_valid():
			if lang:
				word = form.save(commit=False)
				word.Language = lang
				word.views = 0 
				word.save()
				return language(request, language_name_slug)
			else:
				print form.errors
		else:
			print form.errors
	else:
		form = WordForm()

	context_dict = {'form':form, 'language':lang, 'slug':language_name_slug }
	return render(request, 'add_word.html', context_dict)

def add_defiition(request, language_name_slug):
	try:
		word =  Word.objects.get(slug=word_name_slug)
	except word.DoesNotExist:
		word = None 

	if request.method == 'POST':
		form =  DefinitionForm(request.POST)

		if form.is_valid():
			if defin:
				defin = form.save(commit=False)
				defin.word = word
				defin.views = 0 
				defin.save()
				return word(request, word_name_slug)
			else:
				print form.errors
		else:
			print form.errors
	else:
		form = DefinitionForm()

	context_dict = {'form':form, 'language':lang, 'slug':language_name_slug }
	return render(request, 'add_def.html', context_dict)


def register(request):
	registered = False

	if request.method == 'POST':
		user_form = UserForm(data=request.POST)

		profile_form = UserProfileForm(data=request.POST)

		if user_form.is_valid() and profile_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			profile = profile_form.save(commit=False)

			profile.user = user 

			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

			profile.save()

			registered = True 

		else:
			print user_form.errors, profile_form.errors
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

	return render(request, 'register.html', { 'user_form': user_form,
											'profile_form':profile_form,
											'registered':registered }
											)



def user_login(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(username=username, password=password)

		if user:
			if user.is_active:
				login(request, user)
				return HttpResponseRedirect('/')
			else:
				return HttpResponse('Your account is inactive')
		else:
			print "Invalid login details : {0}, {1}".format(username, password)
			return HttpResponse('Your login credentials were wrong')

	else:
		return render(request, 'login.html', {})

def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

# def track_url(request):
# 	page_id = None

# 	url = '/'

# 	if request.method == 'GET':
# 		if 'page_id' in request.GET:
# 			page_id = request.GET['page_id']
# 			try:
# 				page = Page.objects.get(id=page_id)
# 				page.views = page.views + 1 
# 				page.save()
# 				url = page.url
# 			except: 
# 				pass
# 	return redirect(url)


def user_profile(request, user_username):
	context_dict = {}
	user = User.objects.get(username=user_username)
	profile = UserProfile.objects.get(user=user)
	context_dict['profile'] = profile

	return	render(request, 'profile.html', context_dict)

@login_required
def edit_profile(request, user_username):
	profile = get_object_or_404(UserProfile, user__username=user_username)
	pic = profile.picture
	if request.user != profile.user:
		return HttpResponse('Access Denied')

	if request.method == 'POST':
		form = UserProfileForm(data=request.POST)
		if form.is_valid():
			if 'picture' in request.FILES:
				print 'pic found'
				profile.picture = request.FILES['picture']
			else:
				print 'not found'
				profile.picture = pic 

			profile.save()

			return user_profile(request, profile.user.username)
		else:
			print form.errors
	else:
		form = UserProfileForm()
	return render(request, 'edit_profile.html', {'form':form, 'profile':profile})




def contact(request):
	if request.method == 'POST':
		form = ContactForm(request.POST)

		if form.is_valid():
			form.send_message()
			return HttpResponseRedirect('/')
		else:
			print form.errors
	else:
		form = ContactForm()

	return render(request, 'contact.html', {'form':form})



def like_definition(request):
	def_id = None
	if request.method == "GET":
		def_id = request.GET['definition_id']

	likes = 0

	if def_id:
		defin = Definition.objects.get(id=int(def_id))
		if defin:
			likes = defin.likes + 1
			defin.likes = likes 
			defin.save()
	return HttpResponse(likes)

def dislike_definition(request):
	def_id = None
	if request.method == "GET":
		def_id = request.GET['definition_id']

	dislikes = 0

	if def_id:
		defin = Definition.objects.get(id=int(def_id))
		if defin:
			dislikes = defin.dislikes + 1
			defin.dislikes = dislikes 
			defin.save()
	return HttpResponse(dislikes)



class SettingsView(LoginRequiredMixin, FormView):
	template_name = 'settings.html'
	form_class =  PasswordChangeForm
	success_url = reverse_lazy('index')

	def get_form(self, form_class):
		return form_class(user=self.request.user, **self.get_form_kwargs())

	def form_valid(self, form):
		form.save()
		update_session_auth_hash(self.request, form.user)
		return super(SettingsView, self).form_valid(form)


class PasswordRecoveryView(FormView):
	template_name = "password-recovery.html"
	form_class =  PasswordRecoveryForm
	success_url = reverse_lazy('login')

	def form_valid(self, form):
		form.reset_email()
		return super(PasswordRecoveryView, self).form_valid(form)






