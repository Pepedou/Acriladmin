/**
 * Created by José Luis Valencia Herrera on 20/03/16.
 */

$(document).ready(function () {
    $("#id_cost").attr("readonly", "readonly");
});

/** Updates the project's total cost by adding up all the products and materials' prices and costs. */
function updateTotalCost() {
    var totalCost = 0.0;
    var productsCostsSet = $(projectProductsRows).find("td input[name*='product_price']");
    var materialCostsSet = $(projectMaterialsRows).find("td input[name*='material_cost']");
    var totalCostInput = $("#id_cost");

    $(productsCostsSet).each(function () {
        var product_subtotal = parseFloat($(this).val());

        if (!isNaN(product_subtotal)) {
            totalCost += product_subtotal;
        }
    });

    $(materialCostsSet).each(function () {
        var materialSubtotal = parseFloat($(this).val());

        if (!isNaN(materialSubtotal)) {
            totalCost += materialSubtotal;
        }
    });

    totalCostInput.val(totalCost.toFixed(2));
}