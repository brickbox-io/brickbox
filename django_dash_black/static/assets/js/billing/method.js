function AddMethod() {
    var formData = new FormData();
    var xhttp = new XMLHttpRequest();
    var url = '/data/stripe/pay/method';

    xhttp.onload = function () {
        console.log(this.responseText);
        client_secret = this.responseText;
        const options = {
            clientSecret: client_secret,
            // Fully customizable with appearance API.
            appearance: {/*...*/ },
        };

        // Set up Stripe.js and Elements to use in checkout form, passing the client secret obtained in step 2
        const elements = stripe.elements(options);

        // Create and mount the Payment Element
        const paymentElement = elements.create('payment');
        paymentElement.mount('#payment-element');


        $("#payment_method").modal('toggle');
    }

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send(formData);

}
