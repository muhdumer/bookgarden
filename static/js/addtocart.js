
function getSize(obj)
{
    var size = 0, key;
    for (key in obj) 
    {
        if (obj.hasOwnProperty(key)) 
        size++;
    }
    return size;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$('#addtocart_form').on('submit',function(e){
    e.preventDefault();
    
    var cart={};
    if(getCookie('cart')!=null||getCookie('cart')!=undefined)
    {
        cart=JSON.parse(getCookie('cart'));
    }

    var qty=$("#qty").val();
    var pk=$(this).attr('data-id');
    
    var text='Product Added to cart..';
    if(cart[pk]!=undefined||cart[pk]!=null)
    text='Quanity Updated..';

    cart[pk]=qty;
    document.cookie='cart='+JSON.stringify(cart)+";domain=;path=/"
    toastr.success(text);

    $('#navbar-cartcount').find("span").html('('+getSize(cart)+')');

});

$('.anchor-cart').on('click',function(e){
    e.preventDefault();
    var pk=$(this).attr('data-id');
    console.log(pk);
    var cart={};
    if(getCookie('cart')!=null||getCookie('cart')!=undefined)
    {
        cart=JSON.parse(getCookie('cart'));
    }

    if(cart[pk]==undefined||cart[pk]==null)
    {
        cart[pk]=1;
        toastr.success('Product Added to cart..');
    }
    else
    {
        toastr.info('Product already added to cart..');     
    }
    document.cookie='cart='+JSON.stringify(cart)+";domain=;path=/"
    $('#navbar-cartcount').find("span").html('('+getSize(cart)+')');


});


function qtyMinus(obj)
{
    var effect = obj.nextElementSibling;
    var subtotal_tag= document.getElementById('subtotal');
    var total_tag=document.getElementById('total');
    var tax_tag=document.getElementById('tax'); 
    var subtotal=parseFloat(subtotal_tag.innerHTML);
    var td_element=obj.parentElement.parentElement.parentElement;
    var price=parseFloat(td_element.previousElementSibling.firstElementChild.innerHTML.slice(3));
    var item_pk=td_element.parentElement.getAttribute('data-id');
    var outer_div=td_element.parentElement.parentElement.parentElement.parentElement;

    var qty = effect.value; 
    if(!isNaN( qty ) && qty>0) 
    effect.value--;

    subtotal=subtotal-price;
    if(subtotal==0)
    {
        $('#checkout-btn').attr({
            'href':'#',
            'title':'Cart Empty',
             'data-toggle':'popover',
            'data-trigger':'hover',
            'data-content':'Cart is empty kindly fill it up..'
        });
        $('#checkout-btn').popover();
    }
    tax=Math.round(0.3*subtotal);

    subtotal_tag.innerHTML=subtotal;
    tax_tag.innerHTML=tax;
    total_tag.innerHTML=Math.round(subtotal+tax);

    var cart={};
    if(getCookie('cart')!=null||getCookie('cart')!=undefined)
    {
        cart=JSON.parse(getCookie('cart'));
    }

    if(effect.value == 0)
    {
        td_element.parentElement.remove();
        delete cart[item_pk];
        $('#navbar-cartcount').find("span").html('('+getSize(cart)+')');
        if(subtotal==0)
        {
            outer_div.innerHTML="<p><i><b>Cart is empty kindly add some books</b></i></p>"
        }
    }
    else
    {
        cart[item_pk]=effect.value;
    }
    document.cookie='cart='+JSON.stringify(cart)+";domain=;path=/";
    toastr.success('Cart Updated..');
    return false;
}

function qtyPlus(obj)
{
    var effect = obj.nextElementSibling;
    var subtotal_tag= document.getElementById('subtotal');
    var total_tag=document.getElementById('total');
    var tax_tag=document.getElementById('tax'); 
    var subtotal=parseFloat(subtotal_tag.innerHTML);
    var td_element=obj.parentElement.parentElement.parentElement;
    var price=parseFloat(td_element.previousElementSibling.firstElementChild.innerHTML.slice(3));
    var item_pk=td_element.parentElement.getAttribute('data-id');
    var effect = obj.previousElementSibling; 
    var qty = effect.value; 

    if( !isNaN( qty )) 
    effect.value++;
    
    subtotal=subtotal+price;
    tax=Math.round(0.3*subtotal);

    subtotal_tag.innerHTML=subtotal;
    tax_tag.innerHTML=tax;
    total_tag.innerHTML=Math.round(subtotal+tax);

    var cart={};
    if(getCookie('cart')!=null||getCookie('cart')!=undefined)
    {
        cart=JSON.parse(getCookie('cart'));
    }

    if(effect.value == 0)
    {
        td_element.parentElement.remove();
        delete cart[item_pk];
        $('#navbar-cartcount').find("span").html('('+getSize(cart)+')');
    }
    else
    {
        cart[item_pk]=effect.value;
    }
    document.cookie='cart='+JSON.stringify(cart)+";domain=;path=/";
    toastr.success('Cart Updated..');
    return false;
}


