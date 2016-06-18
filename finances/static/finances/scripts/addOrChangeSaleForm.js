/**
 * Created by José Luis Valencia Herrera on 5/03/16.
 */

var subtotalInput;
var shippingInput;
var discountInput;
var discountPercentageInput;
var totalParagraph;

$(document).ready(function () {
    subtotalInput = $("#id_subtotal");
    shippingInput = $("#id_shipping_and_handling");
    discountInput = $("#id_discount");
    discountPercentageInput = $("#id_discount_percentage");
    totalParagraph = $("label:contains('Monto:')").next("p");

    totalParagraph.css("font-weight", "bold");

    subtotalInput.on("change", null, null, function () {
        updateDiscountPercentage();
        updateTotal();
    });

    shippingInput.on("change", null, null, function () {
        updateTotal();
    });

    discountInput.on("change", null, null, function () {
        updateDiscountPercentage();
        updateTotal();

    });

    discountPercentageInput.on("change", null, null, function () {
        updateDiscount();
        updateTotal();
    });
});

function updateDiscountPercentage() {
    var discount = parseFloat(discountInput.val());
    var subtotal = parseFloat(subtotalInput.val());

    if (discount > subtotal) {
        discount = subtotal;
        discountInput.val(discount);
    }
    else if (discount < 0) {
        discount = 0;
        discountInput.val(discount);
    }

    var discountPercentageNum = discount * 100 / subtotal;

    if (discountPercentageNum > 100) {
        discountPercentageNum = 100;
    }

    discountPercentageInput.val(Math.floor(discountPercentageNum));
}

function updateTotal() {
    var subtotal = parseFloat(subtotalInput.val());
    var shipping = parseFloat(shippingInput.val());
    var discount = parseFloat(discountInput.val());

    var total = subtotal + shipping - discount;

    totalParagraph.html(total);
}

function updateDiscount() {
    var subtotal = parseFloat(subtotalInput.val());
    var discountPercentage = parseInt(discountPercentageInput.val());

    if (discountPercentage > 100) {
        discountPercentage = 100;
        discountPercentageInput.val(discountPercentage);
    }
    else if (discountPercentage < 0) {
        discountPercentage = 0;
        discountPercentageInput.val(discountPercentage);
    }

    var discount = subtotal * (discountPercentage / 100);

    discountInput.val(Math.floor(discount));
}
