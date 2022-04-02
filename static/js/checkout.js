

$('#bill_saved_address').on('change',function(e){
    
    var address_pk=$(this).val();
    if(address_pk=='-1')
    {
        document.getElementById('Checkout_out_form').reset();
        return;
    }
    else
    {
    $.ajax({
        url:'http://127.0.0.1:8000/order/checkout/getAddress/',
        dataType:'json',
        method:'GET',
        data:{
            'id':address_pk,
        },
        success:function(data){
            var model=JSON.parse(data);
            var fields=model[0]['fields'];
            $('#bill_first_name').val(fields['first_name']);
            $('#bill_last_name').val(fields['last_name']);
            $('#bill_city').val(fields['city']);
            $('#bill_zipcode').val(fields['zip_code']);
            $('#bill_phone_number').val(fields['phone_number']);
            $('#bill_address').val(fields['address']);
        },
        failure:function()
        {
            alert('Server Error Kindly Try Again Later..');
        }
    });
}

});



function handleshipchange()
{
    var address_pk=$('#ship_address_saved').val();
    if(address_pk=='-1')
    {
        document.getElementById('Checkout_out_form').reset();
        return;
    }
    else
    {
    $.ajax({
        url:'http://127.0.0.1:8000/order/checkout/getAddress/',
        dataType:'json',
        method:'GET',
        data:{
            'id':address_pk,
        },
        success:function(data){
            var model=JSON.parse(data);
            var fields=model[0]['fields'];
            $('#ship_first_name').val(fields['first_name']);
            $('#ship_last_name').val(fields['last_name']);
            $('#ship_city').val(fields['city']);
            $('#ship_zipcode').val(fields['zip_code']);
            $('#ship_phone_number').val(fields['phone_number']);
            $('#ship_address').val(fields['address']);
        },
        failure:function()
        {
            alert('Server Error Kindly Try Again Later..');
        }
        });
    }

}
