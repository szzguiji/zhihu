# encoding=utf-8

import json
from itertools import chain
from operator import attrgetter

from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import RequestContext

from forms import RegisterForm, LoginForm, QuestionForm, ProfileForm
from models import NewUser, Question, Tag, Answer, Comment, Agree, Follow

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

def index(request):
	if request.user.is_authenticated() or 'user_id' in request.session:
		if 'user_id' in request.session:
			user_id = request.session['user_id']
			user = NewUser.objects.get(pk=user_id)
		else:
			user = request.user
		answers = Answer.objects.filter(author__followed__follower=user)
		questions = Question.objects.filter(asker__followed__follower=user)
		datas_list = sorted(chain(answers, questions), key=attrgetter('datetime'),
               reverse=True)

		paginator = Paginator(datas_list, 30)
		page = request.GET.get('page')
		try:
			datas = paginator.page(page)
		except PageNotAnInteger:
			datas = paginator.page(1)
		except EmptyPage:
			datas = paginator.page(paginator.num_pages)
		return render_to_response('home.html', {'datas':datas, 'user':user, 'paginator':paginator})
	else:
		return render_to_response('home.html', context=RequestContext(request))


@login_required(login_url='/polls/index')
def people(request, user_id):
	user = request.user
	people = get_object_or_404(NewUser, pk=user_id)
	follow = Follow.objects.filter(follower=user, followed=people)
	questions = Question.objects.filter(asker=people).order_by("-datetime")
	answers = Answer.objects.filter(author=people).order_by("-datetime")
	return render_to_response('people.html', {'user':user, 'people':people, 
		'questions':questions, 'answers':answers, 'follow':follow})


@login_required(login_url='/polls/index')
def my_asks(request, user_id):
	user = request.user
	page = request.GET.get('page')
	people = NewUser.objects.get(pk=user_id)
	follow = Follow.objects.filter(follower=user, followed=people)
	questions_list = Question.objects.filter(asker=people).order_by("-datetime")

	paginator = Paginator(questions_list, 30)
	try:
		questions = paginator.page(page)
	except PageNotAnInteger:
		questions = paginator.page(1)
	except EmptyPage:
		questions = paginator.page(paginator.num_pages)
	return render(request, 'my_asks.html', {'user':user, 'people':people, 
		'questions':questions, 'follow':follow, 'paginator':paginator})


@login_required(login_url='/polls/index')
def my_answers(request, user_id):
	user = request.user
	page = request.GET.get('page')
	people = NewUser.objects.get(pk=user_id)
	follow = Follow.objects.filter(follower=user, followed=people)
	answers_list = Answer.objects.filter(author=people).order_by("-datetime")

	paginator = Paginator(answers_list, 30)
	try:
		answers = paginator.page(page)
	except PageNotAnInteger:
		answers = paginator.page(1)
	except EmptyPage:
		answers = paginator.page(paginator.num_pages)
	return render_to_response('my_answers.html', {'user':user, 'people':people, 
		'answers':answers, 'follow':follow, 'paginator':paginator})


@csrf_exempt
@login_required(login_url='/polls/index')
def profile(request, user_id):
	user = request.user
	if request.method == 'POST':
		form = ProfileForm(request.POST, request.FILES)
		if form.is_valid():
			user.description = form.cleaned_data['description']
		 	user.city = form.cleaned_data['city']
		 	user.job = form.cleaned_data['job']
		 	user.img = form.cleaned_data['img']
		 	user.save()
		 	return redirect('polls:people', user_id=user_id)
	return render_to_response('profile.html', {'user':user})

@csrf_exempt
def follow(request):
	people_id = request.POST['people_id']
	follow_type = request.POST['follow']
	followed = NewUser.objects.get(pk=people_id)
	user = request.user
	if follow_type == "1":
		follow = Follow.objects.create(follower=user, followed=followed)
	else:
		follow = Follow.objects.filter(follower=user, followed=followed)
		follow.delete()
	return HttpResponse("")

@csrf_exempt
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = NewUser(name=name, email=email)
            user.set_password(password)
            user.save()
            request.session['user_id'] = user.id
    return HttpResponseRedirect(reverse('polls:index'))

@csrf_exempt
def userLogin(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user= authenticate(email=email, password=password)
			if user:
				login(request, user)
			return redirect("/polls/index")

@login_required(login_url='/polls/index')
def user_logout(request):
	logout(request)
	return redirect("/polls/index")

@csrf_exempt
def check_login(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		user= authenticate(email=email, password=password)
		if user:
			result = json.dumps({"success":"1"})
		else:
			result = json.dumps({"success":"0"})
		return HttpResponse(result)

@csrf_exempt
def check_register(request):
	if request.method == 'POST':
		email = request.POST['email']
		password = request.POST['password']
		username = request.POST['username']
		user = NewUser.objects.filter(email=email)
		if len(user)==1:
			result = json.dumps({"success":"0"})
		else:
			result = json.dumps({"success":"1"})
	return HttpResponse(result)

@csrf_exempt
@login_required(login_url='/polls/index')
def ask(request):
	if request.method == "POST":
		user = request.user
		form = QuestionForm(request.POST)
		if form.is_valid():
			title = form.cleaned_data['name']
			tag_name = form.cleaned_data['tag']
			description = form.cleaned_data['description']
			tag = Tag.objects.create(tag=tag_name)
			question = Question.objects.create(title=title, description=description, asker=user)
			question.tags.add(tag)
			return redirect('polls:question', question_id=question.id)
	return render_to_response('ask.html', context=RequestContext(request))

@csrf_exempt
@login_required(login_url='/polls/index')
def question(request, question_id):
	page = request.GET.get('page')
	question = Question.objects.get(pk=question_id)
	tags = question.tags.all()
	answer_list = Answer.objects.filter(question=question)

	paginator = Paginator(answer_list, 30)
	try:
		answers = paginator.page(page)
	except PageNotAnInteger:
		answers = paginator.page(1)
	except EmptyPage:
		answers = paginator.page(paginator.num_pages)
	data = [(answer, Comment.objects.filter(answer=answer)) for answer in answers]
	return render(request, 'question.html', 
		{'question':question, 'tags':tags, 'data':data, 'paginator':paginator, 'answers':answers})

@csrf_exempt
def answer(request):
	if request.method == "POST":
		user = request.user
		question_id = request.POST['question_id']
		question = Question.objects.get(pk=question_id)
		answers = Answer.objects.filter(author=user, question=question)

		if len(answers)>0:
			result = json.dumps({'has_commented':"1"})
		else:
			content = request.POST['answer']
			answer = Answer(content=content, question=question, author=user)
			answer.save()
			answer_time = answer.datetime.strftime("%Y-%m-%d")
			result = {
			'has_commented':"0",
			'user_name': user.name,
			'user_description': user.description,
			'answer': content,
			'answer_time':answer_time,
			}
		result = json.dumps(result)
		return HttpResponse(result)

@csrf_exempt
def comment(request):
    if request.method == "POST":
		user = request.user
		answer_id = request.POST['answer_id']
		answer = Answer.objects.get(pk=answer_id)
		content = request.POST['content']
		userto_id = request.POST['user_to']
		if userto_id == "":
			comment = Comment(content=content, answer=answer, user_from=user)
			userto_name = ""
		else:
			user_to = NewUser.objects.get(pk=userto_id)
			userto_name = user_to.name
			comment = Comment(content=content, answer=answer, user_from=user, user_to=user_to)
		comment.save()
		comment_time = comment.datetime.strftime("%Y-%m-%d %H:%M")

		result = {
		'content':content,
		'userto_name':userto_name,
		'userfrom_name':user.name,
		'comment_time':comment_time,
		}
		result = json.dumps(result)
		return HttpResponse(result)