from __future__ import absolute_import, unicode_literals
from celery import task

import requests

from repo.models import usernames, RepoDetails
from repo.views import getRepos


@task()
def updateRepos():
    print("initial*************************")
    users=usernames.objects.all()
    for j in users:
        print (j.username)
        repos=getRepos(j.username)
        for i in repos:
           if RepoDetails.objects.filter(repository_name=i['name']):
               print("repo exist----------------------")
               pass
           else:
               store_repo = RepoDetails()
               store_repo.usernames = j.id
               store_repo.name = j.username
               store_repo.repository_name = i['name']
               store_repo.repository_url = i['html_url']
               lan = requests.get(i['languages_url']).json()
               store_repo.languages = lan
               store_repo.save()
               print("saved-------------------")