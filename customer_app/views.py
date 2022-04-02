from django.shortcuts import render,redirect
from django.views.generic import CreateView,UpdateView,TemplateView,ListView,DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from .forms import (Register_User_Form,LoginForm,CustomPasswordResetForm,CustomPasswordConfirmForm,UserUpdateForm,UserPasswordUpdateForm,
                    AddressBookCreateForm)
from .models import AddressBook                        
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.http import Http404
from django.utils.translation import ugettext as _
from django.contrib.auth import authenticate,login
from django.conf import settings
from django.db.models import Q
from django.core.exceptions import ValidationError
from django.contrib.auth.views import PasswordResetView,PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView

def ActivateUserAccountView(request,uid64,token):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        user=get_user_model().objects.get(pk=uid)
    except:
        user=None
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        messages.success(request,_('Congratulations! Your Account Has been activated now you can proceed to logging yourself in..'))
        return redirect('customer_app:login')
    else:
        raise Http404(_('Activation Link is Invalid'))  


def SendAccountActivationLinkView(request,uid64):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        user=get_user_model().objects.get(pk=uid)
    except:
        user=None
    if user is not None:
        current_site=get_current_site(request)
        mail_subject='Activate Your Account'
        mail_message=render_to_string('accounts/account_activate.html',{
              'user':user,
              'domain':current_site.domain,
              'uid':urlsafe_base64_encode(force_bytes(user.pk)),
              'token':account_activation_token.make_token(user)  
            
            })

        mail_to_send=EmailMessage(
                mail_subject,
                mail_message,
                to=[user.email]
            )
        mail_to_send.send(fail_silently=True)
        messages.success(request,_('Activation Link Has been sent kindly verify your email inorder to activate your account'))            
        return redirect('customer_app:login')
    else:
        raise Http404()


class SignUpView(CreateView):
    template_name='accounts/register.html'
    model=get_user_model()
    form_class=Register_User_Form
    success_url=reverse_lazy('index')

    def post(self,request,*args, **kwargs):
        form=Register_User_Form(request.POST)
        
        if form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.save()
            current_site=get_current_site(request)
            mail_subject='Activate Your Account'
            mail_message=render_to_string('accounts/account_activate.html',{
              'user':user,
              'domain':current_site.domain,
              'uid':urlsafe_base64_encode(force_bytes(user.pk)),
              'token':account_activation_token.make_token(user)  
            
            })

            mail_to_send=EmailMessage(
                mail_subject,
                mail_message,
                to=[form.cleaned_data['email']]
            )

            mail_to_send.send(fail_silently=True)
            messages.success(request,_('Your Account is successfully created kindly verify your email inorder to activate your account'))
            return redirect('customer_app:register')
        else:
            return render(request,self.template_name,{'form':form})    



class SignInView(LoginView):
    template_name='accounts/login.html'
    authentication_form=LoginForm

    def post(self,request,*args, **kwargs):
        form=LoginForm(data=request.POST)
        
        if form.is_valid():
            user=authenticate(request,username=form.cleaned_data['username'],password=form.cleaned_data['password'])
            if user is not None:
                last_login=user.last_login
                login(request,user)
                return_to=None
                try:
                    return_to=redirect(self.request.GET.get('next'))
                except:    
                    return_to=redirect(settings.LOGIN_REDIRECT_URL)
                    if last_login == None:
                        return redirect('customer_app:my_account_pinfo')
                    else:
                        return return_to    
            else:
                try:
                    user=get_user_model().objects.get(
                                                    Q(email__iexact=form.cleaned_data['username']) | 
                                                    Q(username__iexact=form.cleaned_data['username']) 
                                                    )
                except:
                    form.add_error('username',ValidationError(_('Invalid Credentials')))
                    return render(request,self.template_name,{'form':form})
                else:
                    if not user.is_active:
                        return render(request,self.template_name,{'form':form,
                                                                 'have_link':True,
                                                                 'uid':urlsafe_base64_encode(force_bytes(user.pk))
                                                                 })
                    else:
                        form.add_error('password',ValidationError(_('Invalid Credentials')))
                        return render(request,self.template_name,{'form':form})
        else:
            return render(request,self.template_name,{'form':form})    

class PasswordResetClassView(PasswordResetView):
    template_name='Password_reset/password_reset_form.html'
    email_template_name='Password_reset/password_reset_email.html'
    subject_template_name='Password_reset/password_reset_subject.txt'
    success_url=reverse_lazy('customer_app:password_reset_done')
    form_class=CustomPasswordResetForm

class PasswordConfirmClassView(PasswordResetConfirmView):
    template_name='Password_reset/password_reset_confirm.html'
    success_url=reverse_lazy('customer_app:password_reset_confirm_done')
    form_class=CustomPasswordConfirmForm


class UserUpdateView(SuccessMessageMixin,LoginRequiredMixin,UpdateView):
    template_name='Customer_section/editaccount.html'
    form_class=UserUpdateForm
    success_url=reverse_lazy('customer_app:my_account_pinfo')
    success_message='Personal Info updated successfully..'
    model=get_user_model()

    def get_object(self):
        return self.request.user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['current_user']=self.request.user
        return kwargs    

class UserOldPasswordUpdateView(SuccessMessageMixin,LoginRequiredMixin,PasswordChangeView):
    template_name='Customer_section/editpassword.html'
    form_class=UserPasswordUpdateForm
    success_url=reverse_lazy('customer_app:my_account_password')
    success_message='Password Updated..'


class AddressBookCreateView(LoginRequiredMixin,CreateView):
    template_name='Customer_section/addressdisplayform.html'
    model=AddressBook
    success_url=reverse_lazy('customer_app:address_book_list')
    form_class=AddressBookCreateForm

    def form_valid(self,form):
        self.object=form.save(commit=False)
        self.object.user=self.request.user
        self.object.save()
        return super().form_valid(form)

class AddressBookListView(LoginRequiredMixin,ListView):
    model=AddressBook
    template_name='Customer_section/addressbooklist.html'
    context_object_name='all_address'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('-is_default','-pk')

class AddressBookUpdateView(LoginRequiredMixin,UpdateView):
    model=AddressBook
    template_name='Customer_section/addressbookupdate.html'
    success_url=reverse_lazy('customer_app:address_book_list')
    form_class=AddressBookCreateForm

class AddressBookDeleteView(LoginRequiredMixin,DeleteView):
    model=AddressBook
    success_url=reverse_lazy('customer_app:address_book_list')
    



    

    

