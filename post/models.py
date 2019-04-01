from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from django.core.validators import MinValueValidator,MaxValueValidator

# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    bio = HTMLField()
    profile_pic = models.ImageField(upload_to='images/')
    pub_date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.first_name

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

    @classmethod
    def get_profiles(cls):
        profiles = cls.objects.all()
        return profiles
    
    @classmethod
    def search_by_username(cls,search_term):
        profiles = cls.objects.filter(title__icontains=search_term)
        return profiles

class Project(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    project_name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='images/')
    description = HTMLField()
    project_url = models.CharField(max_length=100)
    technologies_used = HTMLField()
    posted_on = models.DateTimeField(auto_now_add=True,)


    def save_projects(self):
        self.save()
    
    @classmethod
    def get_projects(cls):
        projects = cls.objects.all()
        return projects

    @classmethod
    def search_project(cls,search_term):
        project = cls.objects.filter(project_name__icontains = search_term)
        return project

class Comments(models.Model):
    comment = models.CharField(max_length = 500)
    posted_on = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save_comment(self):
        self.save()

    def delete_comment(self):
        self.delete()

    @classmethod
    def get_comments_by_projects(cls, id):
        comments = Comments.objects.filter(project__pk = id)
        return comments

class Votes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    posted_on = models.DateTimeField(auto_now_add=True,)
    project =  models.ForeignKey(Project,on_delete=models.CASCADE)
    design = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)])
    usability = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)])
    content = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(10)])
