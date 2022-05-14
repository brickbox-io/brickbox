/* ----------------------------- Add New Script ----------------------------- */
function AddScript() {
    $("#add_script").modal('toggle');
}

function DeleteScriptModal(script_id, script_name) {
    document.getElementById("delete_script_button").dataset.script_id = script_id;
    document.getElementById("script_name_confirmation").innerHTML = "Deleting: " + script_name;
    $("#delete_script").modal('toggle');
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

/* ------------------------------- Edit Script ------------------------------ */
function EditScript(script_id) {
    var xhttp = new XMLHttpRequest();
    var url = '/dashboard/tab/developer/script_edit/'+script_id;

    xhttp.onload = function () {
        var response = JSON.parse(this.responseText);
        document.getElementById("update_script_button").dataset.script_id = script_id;
        document.getElementById("edit_script_name").value = response['script_name'];
        document.getElementById("edit_script_description").value = response['script_description'];
        document.getElementById("edit_script_code").value = response['script_code'];
        $("#edit_script").modal('toggle');
    };

    xhttp.open('GET', url);
    xhttp.send();
}

/* ------------------------------ Update Script ----------------------------- */
function UpdateScript(script_id) {
    var script_name = document.getElementById("edit_script_name").value;
    var script_description = document.getElementById("edit_script_description").value;
    var script_code = document.getElementById("edit_script_code").value;

    var formData = new FormData();
    var xhttp = new XMLHttpRequest();
    var url = '/dashboard/tab/developer/script_update'

    formData.append('script_id', script_id);
    formData.append('script_name', script_name);
    formData.append('script_description', script_description);
    formData.append('script_code', script_code);

    xhttp.onload = function () {
        $("#edit_script").modal('toggle');
    }

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send(formData);
}

/* ------------------------------ Delete Script ----------------------------- */
function DeleteScript(script_id) {
    var formData = new FormData();
    var xhttp = new XMLHttpRequest();
    var url = '/dashboard/tab/developer/script_delete'

    formData.append('script_id', script_id);

    xhttp.onload = function () {
        $("#delete_script").modal('toggle');
    }

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send(formData);
}
