from django import forms

class LoginForm(forms.Form):
   idul = forms.CharField()
   pasw = forms.CharField()
