from django import forms
from .models import Person
from django.contrib.auth.forms import ReadOnlyPasswordHashField
class register_public_user(forms.ModelForm):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    username = forms.CharField(label = 'username',max_length=50)
    email= forms.EmailField(max_length=254)
    phone_no = forms.CharField(max_length=13)
    birth_date = forms.DateField()
    password1 = forms.CharField(
        label='password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='password confirmation',
        widget=forms.PasswordInput
    )


    def clean_password2(self):
        #Check that the two password entries match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 != password2:
            raise forms.ValidationError('Password do not match')
        return password2

    def save(self, commit=True):
        user = super(register_public_user, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    class Meta:
        model = Person
        fields = ['first_name','last_name','username','email','phone_no','birth_date','password1','password2']



class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Person
        fields = ('username', 'password', 'active','staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
