function PayBalance() {
    var formData = new FormData();
    var xhttp = new XMLHttpRequest();
    var url = "/bb_billing/manual_payment";

    xhttp.onload = function () {
        var payment_status = JSON.parse(this.responseText);
        document.getElementById("cycle_total").innerHTML = "USAGE | $" + payment_status.balance ;
        PaymentNotice('bottom', 'center', payment_status.notice, 2);
    };

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send(formData);
}


/* --------------------------------- Notices -------------------------------- */
function PaymentNotice(from, align, notice, color = 1) {
    $.notify({
        icon: "tim-icons icon-bell-55",
        message: notice

    }, {
        type: type[color],
        timer: 5000,
        placement: {
            from: from,
            align: align
        }
    });
}
