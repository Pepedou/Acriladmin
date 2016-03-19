/**
 * Created by José Luis Valencia Herrera on 19/03/16.
 */

var projectProductsRows;

$(document).ready(function () {
    $("#projectproductsentry_set-group").on("DOMNodeInserted DOMNodeRemoved", addListeneres);
    addListeneres();
});

function addListeneres() {
    projectProductsRows = $("tr[id^='projectproductsentry_set']");
    $(projectProductsRows).each(function (index, value) {
        var select = $(this).find("td div select");
        var quantity_input = $(this).find("td input[name*='quantity']");
        var cost_input = $(this).find("td input[name*='product_price']");

        var params = {
            select: select,
            quantity_input: quantity_input,
            cost_input: cost_input,
        };

        select.on("change", params, onRowDataChanged);
        quantity_input.on("change", params, onRowDataChanged);
    });
}

function onRowDataChanged(params) {
    var selectedProductPrice = new ProductPrice();
    var selectedProductId = parseInt(params.data.select.val());

    if (!selectedProductId) return;

    selectedProductPrice.getProductPriceByProductId(selectedProductId, function (data) {
        var quantity = parseInt(params.data.quantity_input.val());
        var totalCost = quantity * selectedProductPrice.price;

        if (totalCost < 0) totalCost = 0;

        params.data.cost_input.val(totalCost);
    });
}