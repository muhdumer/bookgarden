from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
import json
from product_app.models import Book
from .utils import get_new_cart_items_subtotal
from django.http import Http404


class HomePage(TemplateView):
    template_name='index.html'

def ContactUsView(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        subject='Contact us request from {}'.format(name)
        message=request.POST['message']
        email_body="Name: {}\nMessage: {}\nMail to Reply: {}\n".format(name,message,email)
        try:
            send_mail(
                subject,
                email_body,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False
            )
        except:
            messages.error(request,_("Due to some reason response wasn't recorded kindly send it again"))
        else:
            messages.success(request,_("Your response has been recorded we will get back to you soon"))
    
    return render(request,"contact-us.html")

class AboutUsView(TemplateView):
    template_name='about-us.html'

def CartDisplayView(request):
    if request.method=='POST':
        raise Http404()
    else:
        context={}
        cart=None
        try:
            cart=request.COOKIES['cart']
        except:
            cart=None
            
        if(cart==None or len(json.loads(cart))==0):
            context['is_empty']=True
            context['subtotal']=0
            context['tax']=0
            context['total']=0
            return render(request,'cart.html',context)
        else:
            cart=json.loads(cart)
            context['items_list'],context['subtotal']=get_new_cart_items_subtotal(cart)
            context['tax']=round(context['subtotal']*0.13,2)
            context['total']=round(context['subtotal']+context['tax'],2)
            return render(request,'cart.html',context)

            
            






