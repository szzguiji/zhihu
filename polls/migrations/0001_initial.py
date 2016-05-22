# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Agree',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('datetime', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.CharField(max_length=100)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('answer', models.ForeignKey(related_name='comment_answer', to='polls.Answer')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
        ),
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.CharField(unique=True, max_length=100)),
                ('description', models.CharField(default=b'', max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('asker', models.ForeignKey(related_name='asker', to='polls.NewUser')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(unique=True, max_length=20)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(to='polls.Tag'),
        ),
        migrations.AddField(
            model_name='follow',
            name='followed',
            field=models.ForeignKey(related_name='followed', to='polls.NewUser'),
        ),
        migrations.AddField(
            model_name='follow',
            name='follower',
            field=models.ForeignKey(related_name='follower', to='polls.NewUser'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user_from',
            field=models.ForeignKey(related_name='user_from', to='polls.NewUser'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user_to',
            field=models.ForeignKey(related_name='user_to', blank=True, to='polls.NewUser', null=True),
        ),
        migrations.AddField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(related_name='author', to='polls.NewUser'),
        ),
        migrations.AddField(
            model_name='answer',
            name='comments',
            field=models.ManyToManyField(to='polls.NewUser', through='polls.Comment'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(related_name='answer_question', to='polls.Question'),
        ),
        migrations.AddField(
            model_name='agree',
            name='answer',
            field=models.ForeignKey(related_name='agree_answer', to='polls.Answer'),
        ),
        migrations.AddField(
            model_name='agree',
            name='user',
            field=models.ForeignKey(related_name='agree_user', to='polls.NewUser'),
        ),
    ]
