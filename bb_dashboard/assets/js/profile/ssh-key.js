/* ------------------------------- Add SSH Key ------------------------------ */
function AddSHH() {
    $("#new_ssh_key").modal('toggle');
}

function SaveKey() {
    var formData = new FormData();
    var xhttp = new XMLHttpRequest();
    var url = '/data/key/add';

    var ssh_key = document.getElementById('ssh_key').value;
    ssh_key = ssh_key.replace(/(\r\n|\n|\r)/gm, "");
    var ssh_name = document.getElementById('ssh_name').value;
    formData.append('ssh_key', ssh_key);
    formData.append('ssh_name', ssh_name);

    xhttp.onload = function () {
        $("#new_ssh_key").modal('toggle');
        var key_status = JSON.parse(this.responseText);
        if (key_status.saved != true) {
           KeyNotice('bottom', 'center', 'Error Saving Key', 4);
        }
        else {
          KeyNotice('bottom', 'center', 'Key Added', 2);
        };
    }

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send(formData);
}

/* --------------------------------- Notices -------------------------------- */
function KeyNotice(from, align, notice, color = 1) {
    $.notify({
        icon: "tim-icons icon-bell-55",
        message: notice

    }, {
        type: type[color],
        timer: 3000,
        placement: {
            from: from,
            align: align
        }
    });
}
