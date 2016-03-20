/**
 * Created by José Luis Valencia Herrera on 19/03/16.
 */

var projectProductsRows;

$(document).ready(function () {
    $("#projectproductsentry_set-group").on("DOMNodeInserted DOMNodeRemoved", addListenersToProductEntries);
    addListenersToProductEntries();
});

/** Adds the event listeners to the select and input elements in the project's products rows. */
function addListenersToProductEntries() {
    projectProductsRows = $("tr[id^='projectproductsentry_set']");
    $(projectProductsRows).each(function () {
        var select = $(this).find("td div select");
        var quantity_input = $(this).find("td input[name*='quantity']");
        var costInput = $(this).find("td input[name*='product_price']");
        var deleteCheckbox = $(this).find("td input[name*='DELETE']");

        var params = {
            select: select,
            quantity_input: quantity_input,
            costInput: costInput,
            deleteCheckbox: deleteCheckbox
        };

        select.on("change", params, onProductDataChanged);
        deleteCheckbox.on("change", params, onProductDataChanged);
        quantity_input.on("change", params, onProductDataChanged);

        /* TODO: Check if this event could be triggered in an onload or similar. */
        select.change();
    });
}

/** Updates the subtotal cost per product when the product or the quantity in the row changes. */
function onProductDataChanged(params) {
    var selectedProductPrice = new ProductPrice();
    var selectedProductId = parseInt(params.data.select.val());

    if (!selectedProductId) return;

    selectedProductPrice.getProductPriceByProductId(selectedProductId, function () {
        var quantity = parseInt(params.data.quantity_input.val());
        var totalCost = quantity * selectedProductPrice.price;

        if (totalCost < 0) totalCost = 0;

        if (params.data.deleteCheckbox.prop('checked')) {
            totalCost = 0;
        }

        params.data.costInput.val(totalCost.toFixed(2));

        updateTotalCost();
    });
}

