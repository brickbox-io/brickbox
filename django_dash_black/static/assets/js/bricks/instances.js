function CreateNewBrick() {
    var formData = new FormData();
    var xhttp = new XMLHttpRequest();
    var url = '/vm/create/'

    xhttp.onload = function () {
        BrickNotice('bottom', 'center', 'Preparing Brick');
    }

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken)
    xhttp.send(formData);
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
        BrickNotice('bottom', 'center', 'Brick Restarting');
    }

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken)
    xhttp.send(formData);
}

function BrickDestroy(brick_id) {
    var formData = new FormData();
    var xhttp = new XMLHttpRequest();
    var url = '/vm/brick/destroy/'

    formData.append('brick_id', brick_id);

    xhttp.onload = function () {
        BrickNotice('bottom', 'center', 'Brick Crumbled');
    }

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken)
    xhttp.send(formData);
}

/* --------------------------------- Notices -------------------------------- */
function CoppiedNotice(from, align) {
    color = Math.floor((Math.random() * 4) + 1);

    $.notify({
        icon: "tim-icons icon-single-copy-04",
        message: "Coppied!"

    }, {
        type: type[color],
        timer: 3000,
        placement: {
            from: from,
            align: align
        }
    });
}
