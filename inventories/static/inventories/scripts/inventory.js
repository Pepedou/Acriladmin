/**
 * Created by José Luis Valencia Herrera on 16/04/16.
 */

$(document).ready(function () {
    var table = $("#inventoryTable").DataTable({
        "language": {
            "url": "//cdn.datatables.net/plug-ins/1.10.11/i18n/Spanish.json"
        }
    });

    var inputArray = $("input")

    inputArray.on("change", function () {
        $(this).css("border", "2px solid red");
    });

    var csrftoken = getCookie('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    inputArray.keyup(function (e) {
        var input = $(this);
        var productId = parseInt(input.parent().siblings("input[name=product_id]").val());
        var itemId = input.parent().siblings("input[name=item_id]").val();
        var inventoryId = parseInt(input.parent().siblings("input[name=inventory_id]").val());
        var quantity = parseInt(input.val());

        if (e.keyCode == 13) {
            $.ajax({
                url: PRODUCT_INV_ITEM_API_URL + itemId + "/",
                method: "PUT",
                data: {
                    product: productId,
                    inventory: inventoryId,
                    quantity: quantity
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    alert("No se pudo actualizar el inventario. Error: " + errorThrown);
                },
                success: function () {
                    input.css("border", "2px solid green");
                    setTimeout(function () {
                        input.css("border", "");
                    }, 200);
                }
            });

        }
    })
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // These HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}