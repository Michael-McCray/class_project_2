from django import forms
from models import Language, Definition, Word, UserProfile
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.crypto import get_random_string

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('username', 'password', 'email')


class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('picture',)


class LanguageForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text='Please enter a cateogry name!')
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Language
		fields = ('name',)

class WordForm(forms.ModelForm):
	name = forms.CharField(max_length=128, help_text='Please enter a Word!')
	language = forms.CharField(max_length=128, help_text='Please enter a language!',required=False)
	views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	slug = forms.CharField(widget=forms.HiddenInput(), required=False)

	class Meta:
		model = Word
		fields = ('name', 'language')
		exclude = ('user', )

class DefinitionForm(forms.ModelForm):
	Definition = forms.CharField(widget=forms.Textarea(), required=True)
	likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
	dislikes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

	class Meta:
		model = Definition
		fields = ('definition', )
		exclude = ('user', )

class ContactForm(forms.Form):
	name = forms.CharField(required=True)
	email = forms.CharField(widget=forms.EmailInput(), required=True)
	subject = forms.CharField(required=True)
	body = forms.CharField(widget=forms.Textarea(), required=True)


	def send_message(self):
		name = self.cleaned_data['name']
		email = self.cleaned_data['email']
		subject = self.cleaned_data['subject']
		body = self.cleaned_data['body']

		message = '''
				New Message from {name} @ {email}
				Subject: {subject}
				Message:
				{body}
				'''.format(name=name,
					email=email,
					subject=subject,
					body=body)

		email_msg = EmailMessage('New Contact Form Submission',
					message,
					email,
					['joeknows718@gmail.com'])

		email_msg.send()

		

class PasswordRecoveryForm(forms.Form):
	email = forms.EmailField(required=False)

	def clean_email(self):
		try:
			return User.objects.get(email=self.cleaned_data['email'])
		except User.DoesNotExist:
			raise forms.ValidationError("Can't find a user based on this email")
		return self.cleaned_data['email']

	def reset_password(self):
		user = self.clean_email()

		password = get_random_string(length=8)

		user.set_password(password)

		user.save() 

		body = """
				Sorry you are having issues with your account! Below is your user name and new password

				Username: {username}
				Password: {password}

				You can log in here: http://localhost:8000/login/
				You can change your password here: http://localhost:8000/settings/

				""".format(username=user.username, password=password)

		pw_msg = EmailMessage('Your new password', body, 'joeknows718@gmail.com', [user.email])

		pw_msg.send()






