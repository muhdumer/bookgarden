from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from customer_app.models import AddressBook
import json
from thebookgarden.utils import get_new_cart_items_subtotal
from django.http import JsonResponse
from django.core import serializers
from django.http import Http404
from .models import Order,OrderItem
from django.contrib.auth import get_user_model
from product_app.models import Book
from django.utils import timezone
from django.views.generic import ListView,DetailView
from .models import Order
from django.core import mail
from django.template.loader import render_to_string
from django.conf import settings
# Create your views here.

def create_order_item_instances(cart,order_obj):
    for key,qty in cart.items():
        key=int(key)
        qty=int(qty)
        book_obj=None
        try:
            book_obj=Book.objects.get(pk=key)
        except:
            book_obj=None
        if book_obj!=None:    
            orderitem_obj=OrderItem(order=order_obj,book=book_obj,quantity=qty,short_book_info=None)
            orderitem_obj.save()

def create_context_dictionary(order_obj):
    all_item_in_order=[]
    subtotal=0
    context={}
    for item in order_obj.orderitem_set.all():
        temp_dict={}
        qty=item.quantity
        price=0
        if item.book !=None:
            price=item.book.book_price
            temp_dict['book_name']=item.book.book_name
        elif item.short_book_info !=None:
            price=item.short_book_info.book_price
            temp_dict['book_name']=item.short_book_info.book_name

        temp_dict['price']=price
        temp_dict['quantity']=qty
        temp_dict['total']=price*qty
        all_item_in_order.append(temp_dict)
        subtotal+=(qty*price)

    context['subtotal']=subtotal
    context['tax']=round(subtotal*0.13,2)
    context['gross_total']=round(context['tax']+subtotal,2)
    context['all_item_in_order']=all_item_in_order
    context['order']=order_obj
    return context


def CheckoutOrderView(request):
    if request.method == 'POST':
        bfname=request.POST['first_name_bill']
        blname=request.POST['last_name_bill']
        bemail=request.POST['email_bill']
        bcountry=request.POST['country_bill']
        baddress=request.POST['address_bill']
        bcity=request.POST['city_bill']
        bzipcode=request.POST['zipcode_bill']
        bphone=request.POST['phone_number_bill']
        comment=request.POST['comment']
        checkbox=request.POST.get('ship_different',False)
        shipping_address=''
        billing_address=''
        sfname=bfname
        slname=blname
        semail=bemail
        sphone=bphone
        scountry=bcountry
        saddress=baddress
        scity=bcity
        szipcode=bzipcode
        if type(checkbox) == type('on') and checkbox=='on':
            sfname=request.POST['first_name_ship']
            slname=request.POST['last_name_ship']
            semail=request.POST['email_ship']
            scountry=request.POST['country_ship']
            saddress=request.POST['address_ship']
            scity=request.POST['city_ship']
            szipcode=request.POST['zipcode_ship']
            sphone=request.POST['phone_number_ship']

        billing_address=baddress+','+bcity+','
        if bzipcode == '':
            billing_address+=bcountry
        else:
            billing_address+=(bzipcode+','+bcountry)    

        shipping_address=saddress+','+scity+','
        if szipcode == '':
            shipping_address+=scountry
        else:
            shipping_address+=(szipcode+','+scountry)

        cart=None
        try:
            cart=request.COOKIES['cart']
        except:
            cart=None
        if cart==None or len(json.loads(cart))==0:
            raise Http404()
        else:
            user=None
            if request.user.is_authenticated:
                user=request.user
            order_obj=Order(billing_first_name=bfname,billing_last_name=blname,billing_email=bemail,
                            billing_address=billing_address,billing_phone_number=bphone,
                            shipping_first_name=sfname,shipping_last_name=slname,shipping_email=semail,
                            shipping_address=shipping_address,shipping_phone_number=sphone,
                            customer=user,order_status=1,payment_status=0,order_guideline=comment,order_created_date=timezone.now()
                            )
            order_obj.save()
            create_order_item_instances(json.loads(cart),order_obj)
            
            connection=mail.get_connection()  #for opening the connection
            
            if bemail =='' and request.user.is_authenticated:
                bemail=request.user.email

            mail_subject_customer='Order Details| The Book Garden'
            mail_subject_admin='You Got A New Order'

            context=create_context_dictionary(order_obj)

            mail_message=render_to_string('orderinvoice.html',context)
            all_messages=list()
            
            if bemail!='':
                mail_to_send=mail.EmailMessage(
                    mail_subject_customer,
                    mail_message,
                    to=[bemail]
                )
                mail_to_send.content_subtype = 'html'
                all_messages.append(mail_to_send)
            
            mail_to_send=mail.EmailMessage(
                mail_subject_admin,
                mail_message,
                to=[settings.EMAIL_HOST_USER]
            )
            mail_to_send.content_subtype = 'html'
            all_messages.append(mail_to_send)

            connection.send_messages(all_messages)
            response=redirect('order_app:checkout-order')
            response.delete_cookie('cart')
            response.set_cookie('order_set_true',1)
            return response                    
    else:
        context={}
        if request.user.is_authenticated:
            context['saved_address']=AddressBook.objects.filter(user=request.user).order_by('-is_default','-pk')
            if context['saved_address'].count()==0:
                context['no_address']=True
            else:
                context['no_address']=False

        cart=None
        try:    
            cart=request.COOKIES['cart']
        except:
            cart=None

        if cart==None or len(json.loads(cart))==0:
            context['is_empty']=True
            context['subtotal']=0
            context['tax']=0
            context['total']=0             
        else:
            context['is_empty']=False
            cart=json.loads(cart)
            _,context['subtotal']=get_new_cart_items_subtotal(cart)
            context['tax']=round(context['subtotal']*0.13,2)
            context['total']=round(context['subtotal']+context['tax'],2)
        return render(request,'checkout.html',context)
            
            
def getAddressObject(request):
    if request.is_ajax():
        address_pk=int(request.GET.get('id'))
        returned_dic= serializers.serialize('json',AddressBook.objects.filter(pk=address_pk))
        return JsonResponse(returned_dic,status=200,safe=False)

class OrderListView(ListView):
    template_name='orderlist.html'
    model=Order
    context_object_name='all_orders'


    def get_queryset(self):
        return self.model.objects.filter(customer=self.request.user).order_by('-pk')
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total=0
        tax=0
        subtotal=0
        total_list=[]
        if context['all_orders'].count()==0:
            context['is_empty']=True

        for order in context['all_orders']:
            for item in order.orderitem_set.all():
                qty=item.quantity
                price=0
                if item.book !=None:
                    price=item.book.book_price
                elif item.short_book_info !=None:
                    price=item.short_book_info.book_price
                subtotal+=(qty*price)
            tax=round(subtotal*0.13,2)
            total=round(tax+subtotal,2)
            total_list.append(total)
            total=tax=subtotal=0

        context['all_orders']=zip(context['all_orders'],total_list)
        return context
    
class OrderDetailView(DetailView):
    template_name='orderdetail.html'
    model=Order
    context_object_name='order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_item_in_order=[]
        subtotal=0
        obj=None
        try:
            obj=Order.objects.get(pk=self.kwargs.get('pk'))
        except:
            raise Http404()

        for item in obj.orderitem_set.all():
            temp_dict={}
            qty=item.quantity
            price=0
            if item.book !=None:
                price=item.book.book_price
                temp_dict['book_name']=item.book.book_name
            elif item.short_book_info !=None:
                price=item.short_book_info.book_price
                temp_dict['book_name']=item.short_book_info.book_name

            temp_dict['price']=price
            temp_dict['quantity']=qty
            temp_dict['total']=price*qty
            all_item_in_order.append(temp_dict)
            subtotal+=(qty*price)

        context['subtotal']=subtotal
        context['tax']=round(subtotal*0.13,2)
        context['gross_total']=round(context['tax']+subtotal,2)
        context['all_item_in_order']=all_item_in_order
        return context
    





    