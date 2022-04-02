from django.contrib import admin
from .models import Order,OrderItem,ShortBookInformation
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter


class OrderNumberFilter(SimpleListFilter):
    title=_('Order Number')
    parameter_name='o_nfilter'

    def lookups(self,request,model_admin):
        return (
            ('id','by Order#'),
        )

    def queryset(self,request,queryset):
        if self.value() == 'id':
            return queryset.order_by('pk')
        else:
            return queryset.all()    

class OrderStatus(SimpleListFilter):
    title=_('Order Status')
    parameter_name='o_sfilter'

    def lookups(self,request,model_admin):
        return(
            ('1','by not confirmed'),
            ('2','by confirmed'),
            ('3','by delivered')
        )
    
    def queryset(self,request,queryset):
        if self.value()=='1':
            return queryset.filter(order_status=1)
        elif self.value()=='2':
            return queryset.filter(order_status=2)
        elif self.value()=='3':
            return queryset.filter(order_status=3)
        else:
            return queryset

class PaymentStatus(SimpleListFilter):
    title=_('Payment Status')
    parameter_name='p_sfilter'

    def lookups(self,request,model_admin):
        return(
            ('0','by not paid'),
            ('1','by paid'),
        )
    
    def queryset(self,request,queryset):
        if self.value()=='0':
            return queryset.filter(payment_status=0)
        elif self.value()=='1':
            return queryset.filter(payment_status=1)
        else:
            return queryset
        

class OrderAdminPage(admin.ModelAdmin):
    list_filter =(OrderNumberFilter,OrderStatus,PaymentStatus)
    list_display=['id','customer','order_status','payment_status','order_created_date']
    readonly_fields=['order_created_date']
    search_fields=('id','billing_first_name','billing_last_name','shipping_first_name','shipping_last_name')

    fieldsets=(
        (
            _('Billing Address'),
            {'fields':('billing_first_name','billing_last_name','billing_address','billing_email','billing_phone_number')}
        ),
        (
            _('Shipping Address'),
            {'fields':('shipping_first_name','shipping_last_name','shipping_address','shipping_email','shipping_phone_number')}
        ),
        (   
            _('Order Guideline by Customer'),
            {'fields':('order_guideline',),}
        ),
        (
            _('Other Order Info'),
            {'fields':('customer','order_status','payment_status','order_created_date')}
        )
    )

class OrderItemAdminPage(admin.ModelAdmin):
    list_display=['order','book','quantity']
    search_fields=('order__id','book__book_name')



admin.site.register(Order,OrderAdminPage)
admin.site.register(OrderItem,OrderItemAdminPage)
admin.site.register(ShortBookInformation)

