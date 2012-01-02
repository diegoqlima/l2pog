# -*- coding: UTF-8 -*-
from django import forms
from l2pog.recaptchawidget.fields import ReCaptchaField
from l2pog.models import Contact, Characters

class FormRegister(forms.Form):
    nome = forms.CharField(max_length=45, required=True, label='Username')
    email = forms.EmailField(required=True, label='Email')
    login = forms.CharField(max_length=45, required=True, label='Login')
    senha = forms.CharField(max_length=45, required=True, label='Password', widget=forms.PasswordInput)
    recaptcha = ReCaptchaField(label='')

class FormContato(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ('idcontact','date')

    recaptcha = ReCaptchaField(label='')

class FormChars(forms.Form):
    character = forms.ModelChoiceField(queryset=Characters.objects.all())