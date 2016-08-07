// JavaScript Document

//ready
$(document).ready(function(){

//    $('input[type="text"]').bind( "change keyup input click" , function() {
//        if(this.value.match(/[^0-9]/g)){
//            this.value = this.value.replace(/[^0-9]/g, '');
//        }
//    });

    // using jQuery
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $('.cart-table input[type="number"]').bind( "change keyup" , function(e) {
        var product_id = $(this).attr('data-id'),
            new_quantity = $(this).val();
        $.ajax({
            url: "/cart/",
            type: "POST",
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            data: ({product_id: product_id, new_quantity: new_quantity}),
            dataType: "html",
            success: function (data) {
                $("body").html(data);
            }
        });
    });
    
});