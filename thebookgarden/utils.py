from product_app.models import Book
def get_new_cart_items_subtotal(cart):
    purchased_book_list=[]
    quantity_of_book=[]
    subtotal=0
    for item_pk,item_quantity in cart.items():
        item_pk=int(item_pk)
        item_quantity=int(item_quantity)
        obj=None
        try:
            obj=Book.objects.get(pk=item_pk)
        except:
            obj=None

        if obj!=None:
            purchased_book_list.append(obj)
            quantity_of_book.append(item_quantity)
            subtotal+=int(obj.book_price)*int(item_quantity)
    return (zip(purchased_book_list,quantity_of_book),subtotal)        
