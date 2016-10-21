/**
 * Created by José Luis Valencia Herrera on 20/10/16.
 */

var alertModal = null;
var alertContent = null;

/**
 * Sends an AJAX request to the provided URL with the given parameters
 * using the post method.
 * @param params A plain object with the following fields:
 * url: URL where the confirm or cancel service is hosted.
 * model: The class' model.
 * pk: The object's primary key.
 * action: A string with either "confirm" or "cancel".
 */
function confirmOrCancelInventoryMovement(params, calling_row) {
    var url = APP_DOMAIN + params.url;
    var model = params.model;
    var pk = params.pk;
    var action = params.action;
    var csrftoken = getCookie('csrftoken');
    alertModal = $("#alertModal");
    alertContent = $("#alertContent");

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $.ajax(
        url, {
            data: {
                'model': model,
                'pk': pk,
                'action': action
            },
            method: 'post',
            datatype: 'json',
            success: function (data, textStatus, jqXHR) {
                onAjaxSuccess(textStatus, data, calling_row);
            },
            error: function () {
                alertContent.html("Ocurrió un error al enviar la petición al servidor [" +
                data ? data : "NA" + "].");
                alertModal.modal();
            }
        }
    )
}

/**
 * Displays response message in the alert modal.
 * @param textStatus From the AJAX response.
 * @param data From the AJAX response.
 * @param calling_row The row that called the AJAX request.
 */
function onAjaxSuccess(textStatus, data, calling_row) {
    if (textStatus == "success" && data.success == true) {
        var sectionDiv = calling_row.parent(".section");

        calling_row.remove();

        if (sectionDiv.children().length == 1) {
            sectionDiv.remove();
        }

        alertContent.html(data.message);
        alertModal.modal();
    }
    else {
        alertContent.html("Ocurrió un error al procesar la petición en el servidor [" +
            data.message + "].");
        alertModal.modal();
    }
}