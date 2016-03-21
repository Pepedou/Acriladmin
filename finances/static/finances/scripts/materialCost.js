/**
 * Created by José Luis Valencia Herrera on 20/03/16.
 */

/* Globally defined at the admin base template. */
var APP_DOMAIN;

/** Describes the cost of a certain material. */
function MaterialCost() {
    var self = this;
    self.materialId = 0;
    self.cost = 0.0;
    self.authorized_by_id = 0;
    self.successCallback = null;

    this.getMaterialPriceByMaterialId = function (materialId, successCallback) {
        var url = APP_DOMAIN + "/api/finances/materialcost/" + materialId;
        var ajaxParams = {
            method: 'GET',
            success: this.onAjaxSuccess,
            error: this.onAjaxError
        };
        this.successCallback = successCallback;

        $.ajax(url, ajaxParams);
    };

    this.onAjaxSuccess = function (data, textStatus) {
        if (textStatus !== "success") {
            alert("No se pudo obtener el precio individual de los materiales.");
            return;
        }

        self.materialId = data.material;
        self.cost = data.cost;
        //noinspection JSUnresolvedVariable
        self.authorized_by_id = data.authorized_by;

        if (self.successCallback) {
            self.successCallback(data);
        }
    };

    this.onAjaxError = function (jqXHR) {
        var errorMessage;

        if (jqXHR.status === 404) {
            errorMessage = "El costo del material seleccionado no se ha dado de alta.";
        }
        else {
            alert("No se pudo actualizar el costo del material.");
        }

        alert(errorMessage);
    };
}

