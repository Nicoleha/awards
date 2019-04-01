from django.shortcuts import render,redirect
from django.http  import HttpResponse
from .forms import ProfileForm,ProjectForm,CommentsForm,VotesForm
from .models import Project,Profile,Comments,Votes
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import ProjectSerializer,ProfileSerializer
from rest_framework import status


# Create your views here.


# Create your views here.
def index(request):
    project = Project.objects.all()

    profile = Profile.objects.all()
    return render(request,'index.html',{"project":project,"profile":profile})

@login_required(login_url='/accounts/login/')
def images(request,project_id):
    project = Project.objects.get(id = project_id)
    comments = Comments.objects.filter(project = project.id).all() 
    votes = Votes.objects.filter(project = project.id).all() 
    return render(request,"Pro.html", {"project":project,"comments":comments,"votes":votes})

@login_required(login_url='/accounts/login/')
def myProfile(request,id):
    user = User.objects.get(id = id)
    profiles = Profile.objects.get(user = user)
   
    return render(request,'profile.html',{"profiles":profiles,"user":user})

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()

            return redirect('index')

    else:
        form = ProfileForm()
    return render(request, 'pro_form.html', {"form": form})

def project(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.user = current_user
            project.save()

            return redirect('index')

    else:
        form = ProjectForm()
    return render(request, 'project.html', {"form": form})

def comments(request,id):
    current_user = request.user
    post = Project.objects.get(id=id)
    comments = Comments.objects.filter(project=post)
  
    if request.method == 'POST':
        form = CommentsForm(request.POST,request.FILES)
        if form.is_valid():
            comment = form.cleaned_data['comment']
            new_comment = Comments(comment = comment,user =current_user,project=post)
            new_comment.save()

            return redirect('project')        
                
    else:
        form = CommentsForm()
        return render(request, 'new-comment.html', {"form":form,'post':post,'user':current_user,'comments':comments})

def votes(request,id):
    current_user = request.user
    post = Project.objects.get(id=id)
    votes = Votes.objects.filter(project=post)
  
    if request.method == 'POST':
            vote = VotesForm(request.POST)
            if vote.is_valid():
                design = vote.cleaned_data['design']
                usability = vote.cleaned_data['usability']
                content = vote.cleaned_data['content']
                rating = Votes(design=design,usability=usability,content=content,user=request.user,project=post)
                rating.save()
                return redirect('project')      
    else:
        form = VotesForm()
        return render(request, 'new-vote.html', {"form":form,'post':post,'user':current_user,'votes':votes})

def search_results(request):

    if 'project' in request.GET and request.GET["project"]:
        search_term = request.GET.get("project")
        searched = Project.search_project(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"searched": searched})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})        

class ProfileList(APIView):
    def get(self, request, format=None):
        serializers = ProfileSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)