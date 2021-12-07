/* ----------------------------- Term Agreement ----------------------------- */
function TermsAgreement() {
    $("#terms_agreement_signature").modal('toggle');

    $("#confirm_button").click(function () {
        $("#terms_agreement_signature").modal('toggle');
        var formData = new FormData();
        var xhttp = new XMLHttpRequest();
        var url = '/colo/agreement/'

        user_id = document.getElementById("confirm_button").dataset.client;

        formData.append('user_id', user_id);

        xhttp.onload = function () {
            var vm_status = JSON.parse(this.responseText);
            BrickNotice('bottom', 'center', 'Terms Signed');
        }

        xhttp.open('POST', url, true);
        xhttp.setRequestHeader("X-CSRFToken", csrftoken);
        xhttp.send(formData);
    });

}

/* ------------------------------- ETH Address ------------------------------ */
function ETH_Address() {
    $("#eth_address").modal('toggle');

    $("#confirm_button").click(function () {
        $("#eth_address").modal('toggle');
        var formData = new FormData();
        var xhttp = new XMLHttpRequest();
        var url = '/colo/eth_address/'

        user_id = document.getElementById("confirm_button").dataset.client;

        formData.append('user_id', user_id);

        xhttp.onload = function () {
            var vm_status = JSON.parse(this.responseText);
            BrickNotice('bottom', 'center', 'ETH Address Added');
        }

        xhttp.open('POST', url, true);
        xhttp.setRequestHeader("X-CSRFToken", csrftoken);
        xhttp.send(formData);
    });
}
