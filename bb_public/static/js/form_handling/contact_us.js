function submit_message() {
    var name = document.getElementById("contact_us_name").value;
    var email = document.getElementById("contact_us_email").value;
    var message = document.getElementById("contact_us_message").value;

    var formData = new FormData();
    var xhttp = new XMLHttpRequest();
    var url = '/forms/contact_us';

    formData.append('name', name);
    formData.append('email', email);
    formData.append('message', message);

    xhttp.onload = function () {
        if (this.status == 200) {
            document.getElementById("contact_us_form").innerHTML = this.responseText;
        }
    }

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send(formData);
}
