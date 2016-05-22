from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^index', views.index, name='index'),
	url(r'^register', views.register, name='register'),
	url(r'^login', views.userLogin, name="userLogin"),
	url(r'^logout', views.user_logout, name="user_logout"),
	url(r'^checklogin', views.check_login, name="check_login"),
	url(r'^checkregister', views.check_register, name="check_register"),
	url(r'^ask', views.ask, name='ask'),
	url(r'^question/(?P<question_id>[0-9]+)', views.question, name='question'),
	url(r'^answer', views.answer, name='answer'),
	url(r'^comment', views.comment, name='comment'),
	url(r'^people/(?P<user_id>[0-9]+)/profile', views.profile, name='profile'),
	url(r'^people/(?P<user_id>[0-9]+)/answers', views.my_answers, name='my_answers'),
	url(r'^people/(?P<user_id>[0-9]+)/asks', views.my_asks, name='my_asks'),
	url(r'^people/(?P<user_id>[0-9]+)', views.people, name='people'),
	url(r'^follow', views.follow, name='follow'),
]
