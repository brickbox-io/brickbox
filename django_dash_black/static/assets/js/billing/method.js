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


        const form = document.getElementById('payment-form');

        form.addEventListener('submit', async (event) => {
            event.preventDefault();

            const { error } = await stripe.confirmSetup({
                //`Elements` instance that was used to create the Payment Element
                elements,
                confirmParams: {
                    return_url: 'https://dev.brickbox.io/dash/billing',
                }
            });

            if (error) {
                // This point will only be reached if there is an immediate error when
                // confirming the payment. Show error to your customer (e.g., payment
                // details incomplete)
                const messageContainer = document.querySelector('#error-message');
                messageContainer.textContent = error.message;
            } else {
                // Your customer will be redirected to your `return_url`. For some payment
                // methods like iDEAL, your customer will be redirected to an intermediate
                // site first to authorize the payment, then redirected to the `return_url`.
            }
        });
    }

    xhttp.open('POST', url, true);
    xhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xhttp.send(formData);

}
