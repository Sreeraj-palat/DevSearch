from dataclasses import fields
from pyexpat import model
from django import forms
from django.forms import ModelForm, widgets
from . models import Job


class jobForm(ModelForm):
    class Meta:
        model = Job
        fields = ['title','description','featured_image']

    def __init__(self,*args, **kwargs):
        super(jobForm,self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})     