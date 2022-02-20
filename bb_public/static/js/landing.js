// Submit email via ajax
function SubmitEmail() {
    var formData = new FormData();
    var xhttp = new XMLHttpRequest();
    var url = '/forms/email_list/'

    formData.append('email', document.getElementById('email').value);

    // Onoad replace email input with confirmation message.
    xhttp.onload = function () {
        if (this.status == 200) {
            // fade(document.getElementById('email_input'));
            document.getElementById('email_input').innerHTML = "";
            document.getElementById('email_input').style.opacity = 0;
            document.getElementById('email_input').innerHTML = this.responseText;
            unfade(document.getElementById('email_input'));
        }
    }

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send(formData);

}

// Fade element out
function fade(element) {
    var op = 1;  // initial opacity
    var timer = setInterval(function () {
        if (op <= 0.1) {
            clearInterval(timer);
            element.style.display = 'none';
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op -= op * 0.1;
    }, 50);
}

// Fade element in
function unfade(element) {
    var op = 0.1;  // initial opacity
    element.style.display = 'block';
    var timer = setInterval(function () {
        if (op >= 1) {
            clearInterval(timer);
        }
        element.style.opacity = op;
        element.style.filter = 'alpha(opacity=' + op * 100 + ")";
        op += op * 0.1;
    }, 50);
}
