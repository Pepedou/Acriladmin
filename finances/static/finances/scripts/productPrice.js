/**
 * Created by José Luis Valencia Herrera on 19/03/16.
 */

/* Globally defined at the admin base template. */
var APP_DOMAIN;

function ProductPrice() {
    var self = this;
    self.productId = 0;
    self.price = 0.0;
    self.authorized_by_id = 0;
    self.successCallback = null;

    this.getProductPriceByProductId = function (productId, successCallback) {
        var url = APP_DOMAIN + "/api/finances/productprice/" + productId;
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
            alert("No se pudo obtener el precio individual de los productos.");
            return;
        }

        self.productId = data.product;
        self.price = data.price;
        //noinspection JSUnresolvedVariable
        self.authorized_by_id = data.authorized_by;

        if (self.successCallback) {
            self.successCallback(data);
        }
    };

    this.onAjaxError = function (jqXHR) {
        var errorMessage;

        if (jqXHR.status === 404) {
            errorMessage = "El precio del producto seleccionado no se ha dado de alta.";
        }
        else {
            alert("No se pudo actualizar el costo del producto.");
        }

        alert(errorMessage);
    };
}

