from django.conf.urls import url

from .views import checkUsername, updateRepos

urlpatterns=[
    url(r'getRepos',checkUsername),
    url(r'updateRepos',updateRepos)
]