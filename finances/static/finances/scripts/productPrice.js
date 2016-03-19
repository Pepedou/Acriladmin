/**
 * Created by José Luis Valencia Herrera on 19/03/16.
 */

/* Globally defined at the admin base template. */
var APP_DOMAIN;

function ProductPrice() {
    var self = this;
    this.productId = 0;
    this.price = 0.0;
    this.authorized_by_id = 0;
    this.successCallback = null;

    this.getProductPriceByProductId = function (productId, successCallback) {
        var url = APP_DOMAIN + "/api/finances/productprice/" + productId;
        var ajaxParams = {
            method: 'GET',
            success: this.onAjaxSuccess,
            error: this.onAjaxError
        };
        this.successCallback = successCallback;

        $.ajax(url, ajaxParams);
    }

    this.onAjaxSuccess = function (data, textStatus, jqXHR) {
        if (textStatus !== "success") {
            alert("No se pudo obtener el precio individual de los productos.");
            return;
        }

        self.productId = data.product;
        self.price = data.price;
        self.authorized_by_id = data.authorized_by;

        if (self.successCallback) {
            self.successCallback(data);
        }
    }

    this.onAjaxError = function (jqXHR, textStatus, errorThrown) {
        alert("No se pudo actualizar el precio del producto.");
    }
}

