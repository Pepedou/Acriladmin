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

    /**
     * Obtains the product's price for the product that matches the given ID.
     * @param productId The ID of the product.
     * @param successCallback The callback to be run on success.
     */
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

    /**
     * Obtains the product's price for the product that matches the given description.
     * @param productDescription The exact description of the product ID.
     * @param successCallback The callback to be run on success.
     */
    this.getProductPriceByProductDescription = function (productDescription, successCallback) {
        var url = APP_DOMAIN + "/api/finances/productprice/";
        var ajaxParams = {
            method: 'GET',
            data: {
                product_description: encodeURIComponent(productDescription)
            },
            success: this.onAjaxSuccess,
            error: this.onAjaxError
        };

        this.successCallback = successCallback;

        $.ajax(url, ajaxParams);
    };

    /**
     * The success callback for the AJAX call.
     * @param data Returned data.
     * @param textStatus The returned status.
     */
    this.onAjaxSuccess = function (data, textStatus, jqXHR) {
        if (textStatus !== "success" || jqXHR.status !== 200) {
            alert("No se pudo obtener el precio individual de los productos.");
            return;
        }

        self.productId = data.product;
        self.price = data.price;
        //noinspection JSUnresolvedVariable
        self.authorized_by_id = data.authorized_by;

        if (self.successCallback) {
            self.successCallback(data, textStatus, jqXHR);
        }
    };

    /**
     * The error callback for the AJAX call.
     * @param jqXHR Contains the error status.
     */
    this.onAjaxError = function (jqXHR) {
        var errorMessage;

        if (jqXHR.status === 404) {
            errorMessage = "El precio del producto seleccionado no se ha dado de alta.";
        }
        else {
            alert("No se pudo obtener el precio del producto.");
        }

        alert(errorMessage);
    };
}

