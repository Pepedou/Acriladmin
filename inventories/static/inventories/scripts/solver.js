/**
 * Created by José Luis Valencia Herrera on 8/09/16.
 */

/**
 * Configures the selectAllCheckbox so that when it is clicked
 * the checkboxes of the product lines are toggled.
 */
function initSelectAllCheckbox() {
    var selectAllProductLinesCheckbox = $("#id_select_all_product_lines");

    selectAllProductLinesCheckbox.on("change", function () {
        var productLinesCheckboxes = $("input[name='product_lines']");

        productLinesCheckboxes.prop("checked", !productLinesCheckboxes.prop("checked"));

        var label = $(this).siblings("label");
        label.html(label.html() === "Todas:" ? "Ninguna:" : "Todas:");
    });
}

$(document).ready(function () {
    initSelectAllCheckbox();
});
