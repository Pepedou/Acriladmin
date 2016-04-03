/**
 * Created by José Luis Valencia Herrera on 3/04/16.
 */

$(document).ready(function () {
    var isCompositeCheckbox = $("input#id_is_composite");
    var productComponentsFieldset = $("div#productcomponent_set-group");

    setViewsInLinesVisibility(isCompositeCheckbox, productComponentsFieldset);
    isCompositeCheckbox.on("click", null, {fieldset: productComponentsFieldset}, isCompositeCheckboxOnClick);
});

/**
 * Hides or shows the product's components fieldset depending on the checked attribute of the
 * isComositeCheckbox.
 * @param isCompositeCheckbox The checkbox used to mark if the product has comopnents.
 * @param productComponentsFieldset The fieldset's div.
 */
function setViewsInLinesVisibility(isCompositeCheckbox, productComponentsFieldset) {
    if (!isCompositeCheckbox.attr("checked")) {
        productComponentsFieldset.hide();
    }
}

function isCompositeCheckboxOnClick(event) {
    var isCompositeCheckbox = $(this);
    var productComponentsFieldset = event.data.fieldset;

    if (isCompositeCheckbox.attr("checked")) {
        isCompositeCheckbox.removeAttr("checked");
        productComponentsFieldset.hide();
    }
    else {
        isCompositeCheckbox.attr("checked", "checked");
        productComponentsFieldset.show();
    }
}