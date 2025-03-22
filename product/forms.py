from cProfile import label

from django import forms
from .models import Ticket, CustomUser


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(
                attrs={'id': 'name', 'placeholder': 'Your Name...', 'required': 'required'}),
            'last_name': forms.TextInput(
                attrs={'id': 'surname', 'placeholder': 'Your Lastname...',
                       'required': 'required'}),
            'email': forms.EmailInput(
                attrs={'id': 'email', 'placeholder': 'Your E-mail...', 'required': 'required',
                       'pattern': "[^ @]*@[^ @]*"}),
            'subject': forms.Select(
                attrs={'id': 'subject', 'placeholder': 'Subject...', 'required': 'required',
                       'style': 'width: 100%;height: 53px;border-radius: 25px;background-color: #f7f7f7;border: 1px solid #e7e7e7;font-size: 14px;color: #4a4a4a;margin-bottom: 30px;'}),
            'message': forms.Textarea(
                attrs={'id': 'message', 'placeholder': 'Your Message', 'required': 'required'}),
        }


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Your username...', 'id': 'name'}))
    password = forms.CharField(max_length=100, required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Your password...', 'id': 'surname'}))


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=100, required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(max_length=100, required=True,
                                widget=forms.PasswordInput(attrs={'placeholder': 'Repeat Password'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'phone', 'email', 'first_name', 'last_name']

        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'username'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'email': forms.TextInput(attrs={'placeholder': 'email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'phone'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Passwords don't match")
        return cd['password2']

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if CustomUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError("phone already exist!")
        return phone





class UserEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone', 'email', 'first_name', 'last_name', 'address']

        widgets = {
            'username': forms.TextInput(
                attrs={'placeholder': 'Your Username...'}),
            'first_name': forms.TextInput(
                attrs={'placeholder': 'Your First Name...'}),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Your Lastname...'}),
            'email': forms.EmailInput(
                attrs={'placeholder': 'Your E-mail...'}),
            'phone': forms.TextInput(
                attrs={'placeholder': 'Your phone...'}),
            'address': forms.Textarea(
                attrs={'placeholder': 'Your Address'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if CustomUser.objects.exclude(id=self.instance.id).filter(phone=phone).exists():
            raise forms.ValidationError("phone already exist!")
        return phone

    def clean_username(self):
        username = self.cleaned_data['username']
        if CustomUser.objects.exclude(id=self.instance.id).filter(username=username).exists():
            raise forms.ValidationError("username already eexist!")
        return username
