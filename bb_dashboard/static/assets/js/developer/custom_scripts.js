/* ----------------------------- Add New Script ----------------------------- */
function AddScript() {
    $("#add_script").modal('toggle');
}

function DeleteScriptModal() {
    $("#delete_script").modal('toggle');
    console.log('itworks')
}

function AddNewScript() {
    var script_name = document.getElementById("script_name").value;
    var script_description = document.getElementById("script_description").value;
    var script_code = document.getElementById("script_code").value;

    $("#add_script").modal('toggle');

    var formData = new FormData();
    var xhttp = new XMLHttpRequest();
    var url = '/dashboard/tab/developer/script_add/'

    formData.append('script_name', script_name);
    formData.append('script_description', script_description);
    formData.append('script_code', script_code);

    xhttp.onload = function () {
    }

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send(formData);
}

