from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import PasswordResetForm,SetPasswordForm
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from .models import AddressBook


class Register_User_Form(UserCreationForm):

    class Meta:
        model=get_user_model()
        fields=('username','email','password1','password2')

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label='Username'
        self.fields['username'].widget.attrs={'data-toggle':'popover','data-trigger':'focus','class':'input100','placeholder':'Type your username','data-content':self.fields['username'].help_text,'data-placement':'top','data-container':'body'}
        self.fields['email'].label="Email"
        self.fields['email'].widget.attrs={'class':'input100','placeholder':'Type your email','required':True}
        self.fields['password1'].label='Password'
        self.fields['password1'].widget.attrs={'data-toggle':'popover','data-trigger':'focus','class':'input100','placeholder':'Type your password','data-placement':'top','data-container':'body'}
        self.fields['password2'].label='Confirm Password'
        self.fields['password2'].widget.attrs={'class':'input100','placeholder':'Type your password'}
        
    def clean_email(self):
        email=self.cleaned_data['email']
        if get_user_model().objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(_('User with this email address already exists.'))
        return email.lower()

    def clean_username(self):
        username=self.cleaned_data['username']
        if get_user_model().objects.filter(username__iexact=username).exists():
            raise forms.ValidationError(_('User with this username already exists'))
        return username.lower()


class LoginForm(AuthenticationForm):
    username=UsernameField(
        label='Username or Email',
        widget=forms.TextInput(attrs={'class':'input100','placeholder':'Type your username'})
    )
    password=forms.CharField(
        label="Password",
		strip=False,
		widget=forms.PasswordInput(attrs={'class':'input100','placeholder':'Type your password'}),
    )

    def clean(self):
        self.cleaned_data['username']=self.cleaned_data['username'].lower()
        return self.cleaned_data


class CustomPasswordResetForm(PasswordResetForm):

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label='Email'
        self.fields['email'].widget.attrs={'class':'input100','placeholder':'Type your email'}

    def clean_email(self):
        return self.cleaned_data['email'].lower()    

class CustomPasswordConfirmForm(SetPasswordForm):
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].label='New Password'
        self.fields['new_password2'].label='Confirm Password'
        self.fields['new_password1'].widget.attrs={'data-toggle':'popover','data-trigger':'focus','class':'input100','placeholder':'Type your password','data-placement':'top','data-container':'body'}
        self.fields['new_password2'].widget.attrs={'class':'input100','placeholder':'Type your password'}
    
class UserUpdateForm(forms.ModelForm):

    class Meta:
        model=get_user_model()
        fields=('username','email','first_name','last_name')

    def __init__(self,*args, **kwargs):
        self.active_user=kwargs.pop('current_user')
        super().__init__(*args, **kwargs)
        self.fields['username'].label='Username'
        self.fields['username'].widget.attrs={'data-toggle':'popover','data-trigger':'focus','class':'input100','placeholder':'Type your username','data-content':self.fields['username'].help_text,'data-placement':'top','data-container':'body'}
        self.fields['email'].label="Email"
        self.fields['email'].widget.attrs={'class':'input100','placeholder':'Type your email','required':True}
        self.fields['first_name'].label='First Name'
        self.fields['first_name'].widget.attrs={'class':'input100','placeholder':'Type your first name'}
        self.fields['last_name'].label='Last Name'
        self.fields['last_name'].widget.attrs={'class':'input100','placeholder':'Type your last name'}

    def clean_email(self):
        email=self.cleaned_data['email']
        if get_user_model().objects.filter(~Q(email__iexact=self.active_user.email),Q(email__iexact=email)).exists():
            raise forms.ValidationError(_('User with this email address already exists.'))
        return email.lower()

    def clean_username(self):
        username=self.cleaned_data['username']
        if get_user_model().objects.filter(~Q(username__iexact=username),Q(username__iexact=username)).exists():
            raise forms.ValidationError(_('User with this username already exists'))
        return username.lower()

class UserPasswordUpdateForm(PasswordChangeForm):

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label='Old Password'
        self.fields['new_password1'].label='New Password'
        self.fields['new_password2'].label='Confirm Password'
        self.fields['new_password1'].widget.attrs={'data-toggle':'popover','data-trigger':'focus','class':'input100','placeholder':'Type your password','data-placement':'top','data-container':'body'}
        self.fields['new_password2'].widget.attrs={'class':'input100','placeholder':'Type your password'}
        self.fields['old_password'].widget.attrs={'class':'input100','placeholder':'Type your old password'}


class AddressBookCreateForm(forms.ModelForm):
    
    class Meta:
        model=AddressBook
        exclude = ('user',)

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs={'class':'form-control','placeholder':'First Name'}
        self.fields['last_name'].widget.attrs={'class':'form-control','placeholder':'Last Name'}
        self.fields['address'].widget.attrs={'class':'form-control','placeholder':'Address'}
        self.fields['city'].widget.attrs={'class':'form-control','placeholder':'City'}
        self.fields['country'].help_text='Currently Delivery Available Within Pakistan Only'
        self.fields['country'].widget.attrs={'class':'form-control','placeholder':'Country','data-content':self.fields['country'].help_text,'readonly':True,'value':'Pakistan','data-toggle':'popover','data-trigger':'focus','data-placement':'top','data-container':'body'}
        self.fields['zip_code'].widget.attrs={'class':'form-control','placeholder':'Zip Code'}
        self.fields['phone_number'].widget.attrs={'class':'form-control','placeholder':'Phone Number'}
        self.fields['is_default'].label='Set as default address'
        self.fields['is_default'].widget.attrs={'class':'custom-control-input'}

    def clean_zip_code(self):
        zip_code=self.cleaned_data['zip_code']
        if zip_code != '':
            if zip_code.isdigit(): 
                return zip_code
            else:
                raise forms.ValidationError(_('Make Sure that you provide correct zip code(all numeric)'))     
        return zip_code

      
        

        
            


        