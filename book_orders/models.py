from django.db import models
from django.contrib.auth import get_user_model
from product_app.models import Book
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.utils import timezone
    

User=get_user_model()

ORDER_STATUS_CHOICES=(
    (1,'Not confirmed'),
    (2,'Confirmed'),
    (3,'Delivered')
)

PAYMENT_STATUS_CHOICES=(
    (0,'Not Paid'),
    (1,'Paid'),
)

class ShortBookInformation(models.Model):
    book_name=models.CharField(max_length=264,verbose_name="Book Name",blank=False)
    book_price=models.PositiveIntegerField(verbose_name="Display Price")

    def __str__(self):
        return self.book_name


class Order(models.Model):
    #Creating Billing Side Attributes
    billing_first_name=models.CharField(max_length=100,blank=False)
    billing_last_name=models.CharField(max_length=100,blank=False)
    billing_email=models.EmailField(max_length=254,blank=True)
    billing_address=models.CharField(max_length=364,blank=False)
    billing_phone_number=models.CharField(max_length=20,blank=False)
    #Creating Shipping Side Attributes
    shipping_first_name=models.CharField(max_length=100,blank=False)
    shipping_last_name=models.CharField(max_length=100,blank=False)
    shipping_email=models.EmailField(max_length=254,blank=True)
    shipping_address=models.CharField(max_length=364,blank=False)
    shipping_phone_number=models.CharField(max_length=20,blank=False)
    #If Order belongs to an authenticated user this field will have its reference else it will be null
    customer=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    #Books in order having manytomanyfield
    books=models.ManyToManyField(Book,through='OrderItem')
    # Order Status
    order_status=models.IntegerField(choices=ORDER_STATUS_CHOICES,default=1)
    #Payment Status
    payment_status=models.IntegerField(choices=PAYMENT_STATUS_CHOICES,default=0)
    #Order Guideline
    order_guideline=models.TextField(blank=True)
    #Date time of order
    order_created_date=models.DateTimeField(blank=False,null=False,default=timezone.now)


    def __str__(self):
        return str(self.pk)


class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    book=models.ForeignKey(Book,on_delete=models.SET_NULL,null=True)
    quantity=models.PositiveIntegerField(default=0,blank=False)
    short_book_info=models.ForeignKey(ShortBookInformation,on_delete=models.CASCADE,null=True)

    def __str__(self):
        return str(self.order)



@receiver(pre_delete, sender=Book)
def pre_delete_receiver(sender,instance,**kwargs):
    all_order_items=instance.orderitem_set.all()
    if all_order_items.count() != 0:
        book_name=instance.book_name
        book_price=instance.book_price
        short_info_obj=ShortBookInformation(book_name=book_name,book_price=book_price)
        short_info_obj.save()
        for obj in all_order_items:
            obj.short_book_info=short_info_obj
            obj.save()




    





    