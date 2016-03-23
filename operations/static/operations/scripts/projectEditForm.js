/**
 * Created by José Luis Valencia Herrera on 20/03/16.
 */

var transactionsSelectBoxObserver = new MutationObserver(filteredTransactionsHaveBeenLoaded);

$(document).ready(function () {
    $("input#id_cost").attr("readonly", "readonly");
    var observerTarget = document.querySelector("#id_transactions");
    var observerConfig = {attributes: true};

    //noinspection JSCheckFunctionSignatures
    transactionsSelectBoxObserver.observe(observerTarget, observerConfig);
});

/**
 *  Callback function executed whenever the #id_transactions element's attributes are modified.
 *  Its purpose is to detect when the transaction's select box is modified to add the filters
 *  and bind the updateAmountPaid callback to the select box buttons's click event.
 */
function filteredTransactionsHaveBeenLoaded() {
    var allButtonsHaveBeenLoaded = true;
    var filteredTransactionsButtons = [$("#id_transactions_add_link"), $("#id_transactions_remove_link"),
        $("#id_transactions_add_all_link"), $("#id_transactions_remove_all_link")];

    filteredTransactionsButtons.forEach(function (entry) {
        if (entry.length > 0) {
            entry.off("click");
            entry.on("click", updateAmountPaid);
        }
        else {
            allButtonsHaveBeenLoaded = false;
        }
    });

    if (allButtonsHaveBeenLoaded) {
        transactionsSelectBoxObserver.disconnect();
    }
}

/** Updates the project's total cost by adding up all the products and materials' prices and costs. */
function updateTotalCost() {
    var totalCost = 0.00;
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

/** Updates the project's amount paid field by adding up all the selected transactions' amounts. */
function updateAmountPaid() {
    var amountPaid = 0.00;
    var amountPaidInput = $("input#id_amount_paid");

    $("select#id_transactions_to").children("option").each(function (index, transaction) {
        var splitTransaction = transaction.innerHTML.split('$');
        var transactionAmount = parseFloat(splitTransaction[splitTransaction.length - 1]);

        if (!isNaN(transactionAmount)) {
            amountPaid += transactionAmount;
        }
        else {
            alert("No se pudo obtener la cantidad de la transacción '" + transaction + "'");
        }
    });

    amountPaidInput.val(amountPaid.toFixed(2));
}