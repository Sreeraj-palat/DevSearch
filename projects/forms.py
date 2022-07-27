from cProfile import label
from dataclasses import field
import imp
from pyexpat import model
from django import forms
from django.forms import ModelForm, widgets
from . models import Project,Review

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title','description','featured_image','source_link','demo_link']

        widgets = {
            'tags' : forms.CheckboxSelectMultiple(),
        }

    def __init__(self,*args, **kwargs):
        super(ProjectForm,self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})    


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value','body']

        labels = {
            'value':'Place your Vote',
            'body':'Add a comment'
        }
           
    def __init__(self,*args, **kwargs):
        super(ReviewForm,self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})      