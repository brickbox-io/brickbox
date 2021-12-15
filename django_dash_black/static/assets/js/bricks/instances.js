/* ------------------------------ Create New VM ----------------------------- */
function CreateNewBrick(selected_gpu) {
    var formData = new FormData();
    var xhttp = new XMLHttpRequest();
    var url = '/vm/create/'

    formData.append('selected_gpu', selected_gpu);

    xhttp.onload = function () {
        BrickNotice('bottom', 'center', 'Firing Bricks');
        var vm_status = JSON.parse(this.responseText);
        document.getElementById("brick_wall").innerHTML = vm_status.table;
        CheckBrickStatus(vm_status.brick_id);

        // setTimeout(() => {
        //     CheckBrickStatus(BrickInfo);
        // }, 5000);
    }

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send(formData);
}


/* --------------------------- Check Brick Status --------------------------- */
function CheckBrickStatus(BrickID) {
    var formData = new FormData();
    var xhttp = new XMLHttpRequest();
    var url = '/vm/status/'

    formData.append('BrickID', BrickID);

    xhttp.onload = function () {
        var vm_status = JSON.parse(this.responseText);
        console.log(vm_status);
        if (vm_status.changes != true) {
            setTimeout(() => {
                CheckBrickStatus(BrickID);
            }, 5000);
        }
        else {
            document.getElementById("brick_wall").innerHTML = vm_status.table;
        };
    }

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send(formData);
}

/* ---------------------------- Copy To Clipbard ---------------------------- */
function CopySSH(ssh_id) {
    var copyText = document.getElementById(ssh_id);
    var textArea = document.createElement("textarea");
    textArea.value = copyText.textContent;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand("Copy");
    textArea.remove();
    CoppiedNotice('bottom', 'center');
}

/* ----------------------------- Brick Commands ----------------------------- */
function BrickPause(brick_id) {
    var formData = new FormData();
    var xhttp = new XMLHttpRequest();
    var url = '/vm/brick/pause/'

    formData.append('brick_id', brick_id);

    xhttp.onload = function () {
        BrickNotice('bottom', 'center', 'Brick Paused');
    }

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken)
    xhttp.send(formData);
}

function BrickPlay(brick_id) {
    var formData = new FormData();
    var xhttp = new XMLHttpRequest();
    var url = '/vm/brick/play/'

    formData.append('brick_id', brick_id);

    xhttp.onload = function () {
        BrickNotice('bottom', 'center', 'Brick Booting');
    }

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken)
    xhttp.send(formData);
}

function BrickReboot(brick_id) {
    var formData = new FormData();
    var xhttp = new XMLHttpRequest();
    var url = '/vm/brick/reboot/'

    formData.append('brick_id', brick_id);

    xhttp.onload = function () {
        document.getElementById('status_text').innerHTML = "Rebooting"
        document.getElementById('reboot_button').disabled = true;
        document.getElementById('power_button').disabled = true;
        BrickNotice('bottom', 'center', 'Brick Restarting');
    }

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken)
    xhttp.send(formData);
}

function BrickDestroy(brick_id, brick_name) {
    $("#brick_destroy_confirmation").modal('toggle');

    document.getElementById("destry_notice_text").innerHTML="Brick will be turned into dust and can not be recovered, are you sure you want to destroy "+ brick_name + "?";

    $("#confirm_button").click(function () {
        $("#brick_destroy_confirmation").modal('toggle');
        var formData = new FormData();
        var xhttp = new XMLHttpRequest();
        var url = '/vm/brick/destroy/'

        formData.append('brick_id', brick_id);

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

/* --------------------------------- Notices -------------------------------- */
function CoppiedNotice(from, align) {
    color = Math.floor((Math.random() * 4) + 1);

    $.notify({
        icon: "tim-icons icon-single-copy-04",
        message: "Copied!"

    }, {
        type: type[color],
        timer: 3000,
        placement: {
            from: from,
            align: align
        }
    });
}

function BrickNotice(from, align, notice) {
    color = Math.floor((Math.random() * 4) + 1);

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
