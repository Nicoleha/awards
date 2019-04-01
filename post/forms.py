from django import forms
from .models import Profile,Project,Comments,Votes

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user', 'pub_date']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ['user','profile','posted_on']

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        exclude = ['user','project','posted_on']

class VotesForm(forms.ModelForm):
    class Meta:
        model = Votes
        exclude = ['user','project','posted_on']
