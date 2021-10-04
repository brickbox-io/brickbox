''' bb_accounts forms.py '''

from django import forms

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


# ----------------------------- Registration Form ---------------------------- #
class RegistrationForm(UserCreationForm):
    '''
    Registration form.
    '''
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
                    'class' : 'mdc-text-field__input',
                    'id' : 'username',
                    'autocomplete' : 'username',
                    'tabindex' : '1'
                }))
    email = forms.EmailField(max_length=254, required=True, widget=forms.TextInput(attrs={
                'class' : 'mdc-text-field__input',
                'id' : 'email',
                'autocomplete' : 'email',
                'tabindex' : '5'
            }))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
                    'class' : 'mdc-text-field__input',
                    'id' : 'password1',
                    'autocomplete' : 'new-password',
                    'tabindex' : '2'
                }))

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'email', 'password1']:
            self.fields[fieldname].help_text = None

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
