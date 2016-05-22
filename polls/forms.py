from django import forms

class RegisterForm(forms.Form):
	username = forms.CharField(max_length=100)
	email = forms.EmailField()
	password = forms.CharField(max_length=100)


class LoginForm(forms.Form):
	email = forms.EmailField()
	password = forms.CharField(max_length=100)


class QuestionForm(forms.Form):
	name = forms.CharField(max_length=100)
	tag = forms.CharField(max_length=20)
	description = forms.CharField(required=False)


class ProfileForm(forms.Form):
	description = forms.CharField(max_length=100)
	city = forms.CharField(max_length=20)
	job = forms.CharField(max_length=20)
	img = forms.ImageField()