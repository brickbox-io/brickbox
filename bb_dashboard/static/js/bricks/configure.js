function OpenConfiguration(brick_id) {
    var formData = new FormData();
    var xhttp = new XMLHttpRequest();
    var url = '/vm/brick/info'

    formData.append('brick_id', brick_id);

    xhttp.onload = function () {
        var birck_info = JSON.parse(this.responseText);
        console.log(birck_info);

        document.getElementById('config-current_gpu').innerHTML = birck_info.gpu_count;
        document.getElementById('config-current_gpu').dataset.count = birck_info.gpu_count;

        document.getElementById('config-current_cpu').innerHTML = birck_info.cpu_count;
        document.getElementById('config-current_cpu').dataset.count = birck_info.cpu_count;

        document.getElementById('config-current_memory').innerHTML = birck_info.memory_quantity;
        document.getElementById('config-current_memory').dataset.count = birck_info.memory_quantity;

        document.getElementById('SaveResourceChanges').dataset.brick_id = brick_id;

        $("#brick_configure").modal('toggle');
    };

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send(formData);
}

function IncreaseResourceCount(resource) {
    var count = parseInt(document.getElementById('config-current_'+ resource).dataset.count);
    var new_count = parseInt(count) + 1;

    document.getElementById('config-current_'+ resource).innerHTML = new_count;
    document.getElementById('config-current_'+ resource).dataset.count = new_count;
}

function DecreaseResourceCount(resource) {
    var count = parseInt(document.getElementById('config-current_'+ resource).dataset.count);
    var new_count = parseInt(count) - 1;

    document.getElementById('config-current_'+ resource).innerHTML = new_count;
    document.getElementById('config-current_'+ resource).dataset.count = new_count;
}

function SaveResourceChanges(brick_id) {
    var formData = new FormData();
    var xhttp = new XMLHttpRequest();
    var url = '/vm/brick/update_resources'

    formData.append('brick_id', brick_id);
    formData.append('gpu_count', document.getElementById('config-current_gpu').dataset.count);
    formData.append('cpu_count', document.getElementById('config-current_cpu').dataset.count);
    formData.append('memory_quantity', document.getElementById('config-current_memory').dataset.count);

    xhttp.onload = function () {
        $("#brick_configure").modal('toggle');
    };

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send(formData);
}
