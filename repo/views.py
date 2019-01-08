# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render

# Create your views here.
import requests
import zipfile
import io
import sys

from repo.models import usernames, RepoDetails

check_username_url = "https://api.github.com/users/"
repos_url = "https://api.github.com/users/"
repo_zip_url = "https://github.com/"

@api_view(['POST'])
def checkUsername(request):
    username=request.data['username']
    print("before'''''''''''''''''''")
    un=usernames.objects.filter(username=username).values()
    print(un)
    if not un:
        url = check_username_url + request.data['username']
        response = requests.get(url)
        user = response.json()
        print("uuuuuuuuuuuu----------------------------",user)
        # if user['message']!='Not Found':
        if 'message' in user.keys():
            return render(request, 'home.html', {'error': "Username does not exist in gitHub!"})
        else:
            user_name = usernames()
            user_name.username = username
            user_name.save()
            data = getRepos(username)
            for i in data:
                lan = requests.get(i['languages_url']).json()
                print("lan----------------------------------", lan)
                store_repo = RepoDetails()
                store_repo.usernames = user_name
                store_repo.name = username
                store_repo.repository_name = i['name']
                store_repo.repository_url = i['html_url']
                store_repo.languages = lan
                store_repo.save()
            data1 = RepoDetails.objects.filter(usernames=user_name).values()
            return render(request, 'home.html', {'results': data1})
    else:
        repos = getRepos(username)
        for i in repos:
            if RepoDetails.objects.filter(repository_name=i['name']):
                print("repo exist----------------------")
                pass
            else:
                store_repo = RepoDetails()
                store_repo.usernames = un
                store_repo.name = un.username
                store_repo.repository_name = i['name']
                store_repo.repository_url = i['html_url']
                lan = requests.get(i['languages_url']).json()
                store_repo.languages = lan
                store_repo.save()
                print("saved-------------------")
        data1 = RepoDetails.objects.filter(name=username).values()
        return render(request, 'home.html', {'results': data1})


def getRepos(username):
    print ("Getting your Repository List")
    if username:
        try:
            url = repos_url + username + "/repos"
            response = requests.get(url)
            repos = response.json()
            print (repos)
            return repos
        except Exception as e:
            print (e)
    else:
        return "Oops ! you don't have pass your username ."



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



# def saveRepos(username, repos=None):
#     if repos:
#         try:
#             repo_number = 1
#             for repo in repos:
#                 reponame = repo["name"]
#                 print (str(repo_number) + " " + reponame + " downloading....")
#                 repozipurl = repo_zip_url + username + "/" + reponame + "/archive/master.zip"
#                 get_repo_zip = requests.get(repozipurl)
#                 repozipfile = zipfile.ZipFile(io.BytesIO(get_repo_zip.content))
#                 print ("\tExtracting " + reponame + "....")
#                 repozipfile.extractall()
#                 print ("\t" + reponame + "downloading Complete :)")
#                 repo_number += 1
#             return True
#         except Exception as e:
#             print (e)
#             return False
#     else:
#         return "Oops! Your don't have any Repository"
#
#
# def main():
#     username = input("Enter your Github Profile username : ")
#     if checkUsername(username):
#         repos = getRepos(username)
#         status = saveRepos(username=username, repos=repos)
#         if status:
#             print ("Done")
#         else:
#             print ("Oops ! something went wrong :(")
#     else:
#         print ("Username does not exist !")