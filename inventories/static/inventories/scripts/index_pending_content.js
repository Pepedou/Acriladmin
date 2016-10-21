/**
 * Created by José Luis Valencia Herrera on 20/10/16.
 */

/**
 * Sends an AJAX request to the provided URL with the given parameters
 * using the post method.
 * @param params A plain object with the following fields:
 * url: URL where the confirm or cancel service is hosted.
 * model: The class' model.
 * pk: The object's primary key.
 * action: A string with either "confirm" or "cancel".
 */
function confirmOrCancelInventoryMovement(params) {
    var url = params.url;
    var model = params.model;
    var pk = params.pk;
    var action = params.action;

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
                if (textStatus === "success") {
                    alert(data);
                }
            },
            error: function (jqXHR, textStatus, errorThrown) {
                if (textStatus) {
                    alert(textStatus);
                }
            }
        }
    )
}