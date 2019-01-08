# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class usernames(models.Model):
    username=models.TextField()


class RepoDetails(models.Model):
    usernames=models.ForeignKey('usernames', on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    repository_name=models.CharField(max_length=200)
    languages=models.TextField(null=True, blank=True)
    repository_url=models.TextField()
