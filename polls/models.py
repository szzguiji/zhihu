from django.db import models
from django.contrib.auth.models import AbstractBaseUser
# Create your models here.

class NewUser(AbstractBaseUser):
	name = models.CharField(max_length=100)
	email = models.CharField(max_length=100,unique=True)
	description = models.CharField(max_length=100, default="")
	city = models.CharField(max_length=20, default="")
	job = models.CharField(max_length=20, default="")
	img = models.ImageField(upload_to='upload', null=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name',]

	def __unicode__(self):
		return self.name


class Follow(models.Model):
	follower = models.ForeignKey(NewUser, related_name="follower")
	followed = models.ForeignKey(NewUser, related_name="followed")


class Tag(models.Model):
	tag = models.CharField(max_length=20, unique=True)

	def __unicode__(self):
		return self.tag


class Question(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	tags = models.ManyToManyField(Tag)
	datetime = models.DateTimeField(auto_now=True, auto_now_add=False)
	asker = models.ForeignKey(NewUser, related_name="asker")

	def data_name(self):
		return "question"

	def __unicode__(self):
		return self.title


class Answer(models.Model):
	content = models.TextField()
	datetime = models.DateTimeField(auto_now=True, auto_now_add=False)
	question = models.ForeignKey(Question, related_name="answer_question")
	comments = models.ManyToManyField(NewUser, through="Comment", through_fields=('answer', 'user_from'))
	author = models.ForeignKey(NewUser, related_name="author")

	def data_name(self):
		return "answer"

	def __unicode__(self):
		return self.content

class Comment(models.Model):
	content = models.CharField(max_length=100)
	datetime = models.DateTimeField(auto_now=True, auto_now_add=False)
	answer = models.ForeignKey(Answer, related_name="comment_answer")
	user_from = models.ForeignKey(NewUser, related_name="user_from")
	user_to = models.ForeignKey(NewUser, blank=True, null=True, related_name="user_to")

	def __unicode__(self):
		return self.content


class Agree(models.Model):
	datetime = models.DateTimeField(auto_now=False, auto_now_add=True)
	user = models.ForeignKey(NewUser, related_name="agree_user")
	answer = models.ForeignKey(Answer, related_name="agree_answer")
