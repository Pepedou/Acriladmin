/**
 * Created by José Luis Valencia Herrera on 19/03/16.
 */

var projectProductsRows;

$(document).ready(function () {
    $("#projectproductsentry_set-group").on("DOMNodeInserted DOMNodeRemoved", addListeners);
    $("#id_cost").attr("readonly", "readonly");
    addListeners();
});

/** Adds the event listeners to the select and input elements in the project's products rows. */
function addListeners() {
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
            deleteCheckbox: deleteCheckbox,
        };

        select.on("change", params, onRowDataChanged);
        deleteCheckbox.on("change", params, onRowDataChanged);
        quantity_input.on("change", params, onRowDataChanged);

        /* TODO: Check if this event could be triggered in an onload or similar. */
        select.change();
    });
}

/** Updates the subtotal cost per product when the product or the quantity in the row changes. */
function onRowDataChanged(params) {
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

/** Updates the project's total cost by adding up all the products' prices. */
function updateTotalCost() {
    var totalCost = 0.0;
    var productsCostsSet = $(projectProductsRows).find("td input[name*='product_price']");
    var totalCostInput = $("#id_cost");

    $(productsCostsSet).each(function () {
        var product_subtotal = parseFloat($(this).val());

        if (!isNaN(product_subtotal)) {
            totalCost += product_subtotal;
        }
    });

    totalCostInput.val(totalCost.toFixed(2));
}