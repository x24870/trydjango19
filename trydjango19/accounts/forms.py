from django import forms
from django.contrib.auth import authenticate, get_user_model, login, logout

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
    # Implement a clean() method on your Form 
    # when you must add custom validation for fields that are interdependent.
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('This user does not exist')
            if not user.check_password(password):
                #this condition will not triggered, because if the password is not correct, we can't get user
                raise forms.ValidationError('Incorrect password')
            if not user.is_active:
                raise forms.ValidationError('This user is no longer active')
        
        return super(UserLoginForm, self).clean(*args, *kwargs)