from django import forms
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.db.models import fields
from django.forms.widgets import Widget
from .models import Seller
from django.contrib.auth.hashers import check_password

class SelSignup(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput)
    retype_password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=Seller
        fields=['name','company','phone','email','address']

    def clean(self):
        super().clean()
        p=self.cleaned_data.get('password')
        p1=self.cleaned_data.get('retype_password')
        if p!=p1 or len(p)<6:
            raise forms.ValidationError("Error password : Both Password did not match...")


class Sellerlogin(forms.Form):
    company=forms.CharField()
    password=forms.CharField(widget=forms.PasswordInput)
    def clean(self):
        c=self.cleaned_data.get("company")
        p=self.cleaned_data.get("password")
        try:
            sel=Seller.objects.get(company=c)
        except:
            raise forms.ValidationError("User Does Not Exits")
        else:
            if not check_password(p,sel.password):
                raise forms.ValidationError("Password does not match")