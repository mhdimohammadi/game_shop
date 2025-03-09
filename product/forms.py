from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(
                attrs={'id': 'name', 'autocomplete': 'on', 'placeholder': 'Your Name...', 'required': 'required'}),
            'last_name': forms.TextInput(
                attrs={'id': 'surname', 'autocomplete': 'on', 'placeholder': 'Your Lastname...',
                       'required': 'required'}),
            'email': forms.EmailInput(
                attrs={'id': 'email', 'autocomplete': 'on', 'placeholder': 'Your E-mail...', 'required': 'required',
                       'pattern': "[^ @]*@[^ @]*"}),
            'subject': forms.Select(
                attrs={'id': 'subject', 'autocomplete': 'on', 'placeholder': 'Subject...', 'required': 'required',
                       'style': 'width: 100%;height: 53px;border-radius: 25px;background-color: #f7f7f7;border: 1px solid #e7e7e7;font-size: 14px;color: #4a4a4a;margin-bottom: 30px;'}),
            'message': forms.Textarea(
                attrs={'id': 'message', 'autocomplete': 'on', 'placeholder': 'Your Message', 'required': 'required'}),
        }
