function myFunction() {
	const x = document.getElementById("nav-links");
	if (x.style.display === "flex") {
		x.style.display = "none";

	} else {
		x.style.display = "flex";
	}
}

// Get the modal
var legalmodal = document.getElementById("legalModal");

// Get the button that opens the modal
var legalbtn = document.getElementById("legal");

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close")[0];

// When the user clicks on the button, open the modal
legalbtn.onclick = function() {
legalmodal.style.display = "flex";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
legalmodal.style.display = "none";
}

 // Get the modal
 var contactmodal = document.getElementById("contactModal");

// Get the button that opens the modal
var contactbtn = document.getElementById("contact");

// Get the <span> element that closes the modal
var cspan = document.getElementsByClassName("contactclose")[0];

// When the user clicks on the button, open the modal
contactbtn.onclick = function() {
contactmodal.style.display = "flex";
}

// When the user clicks on <span> (x), close the modal
cspan.onclick = function() {
contactmodal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
	if (event.target == contactmodal) {
		contactmodal.style.display = "none";
	} else if (event.target == legalmodal) {
		legalmodal.style.display = "none";
	}
}