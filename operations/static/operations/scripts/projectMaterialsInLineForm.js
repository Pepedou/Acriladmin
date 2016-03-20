/**
 * Created by José Luis Valencia Herrera on 19/03/16.
 */

var projectMaterialsRows;

$(document).ready(function () {
    $("#projectmaterialsentry_set-group").on("DOMNodeInserted DOMNodeRemoved", addListenersToMaterialEntries);
    addListenersToMaterialEntries();
});

/** Adds the event listeners to the select and input elements in the project's products rows. */
function addListenersToMaterialEntries() {
    projectMaterialsRows = $("tr[id^='projectmaterialsentry_set']");
    $(projectMaterialsRows).each(function () {
        var select = $(this).find("td div select");
        var quantityInput = $(this).find("td input[name*='quantity']");
        var costInput = $(this).find("td input[name*='material_cost']");
        var deleteCheckbox = $(this).find("td input[name*='DELETE']");

        var params = {
            select: select,
            quantityInput: quantityInput,
            costInput: costInput,
            deleteCheckbox: deleteCheckbox
        };

        select.on("change", params, onMaterialDataChanged);
        deleteCheckbox.on("change", params, onMaterialDataChanged);
        quantityInput.on("change", params, onMaterialDataChanged);

        /* TODO: Check if this event could be triggered in an onload or similar. */
        select.change();
    });
}

/** Updates the subtotal cost per material when the material or the quantity in the row changes. */
function onMaterialDataChanged(params) {
    var selectedMaterialCost = new MaterialCost();
    var selectedMaterialId = parseInt(params.data.select.val());

    if (!selectedMaterialId) return;

    selectedMaterialCost.getMaterialPriceByMaterialId(selectedMaterialId, function () {
        var quantity = parseInt(params.data.quantityInput.val());
        var totalCost = quantity * selectedMaterialCost.cost;

        if (totalCost < 0) totalCost = 0;

        if (params.data.deleteCheckbox.prop('checked')) {
            totalCost = 0;
        }

        params.data.costInput.val(totalCost.toFixed(2));

        updateTotalCost();
    });
}