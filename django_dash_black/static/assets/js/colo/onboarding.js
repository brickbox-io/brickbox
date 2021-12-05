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
            BrickNotice('bottom', 'center', 'Brick Crumbled');
            document.getElementById("brick_wall").innerHTML = vm_status.table;
        }

        xhttp.open('POST', url, true);
        xhttp.setRequestHeader("X-CSRFToken", csrftoken);
        xhttp.send(formData);
    });

}

function ETH_Address() {
    $("#eth_address").modal('toggle');
    $("#confirm_button").click(function () {
        $("#eth_address").modal('toggle');

    });
}
