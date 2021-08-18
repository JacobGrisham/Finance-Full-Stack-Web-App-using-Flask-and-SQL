// --------------------------------------
// Google Analytics
// --------------------------------------
window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());

gtag('config', 'G-36KQSD0BWH');


// --------------------------------------
// Disable form submissions if there are invalid fields
// --------------------------------------
(function () {
  'use strict'

  window.addEventListener('load', function() {
    // Fetch all the forms we want to apply custom validation styles
    var inputs = document.getElementsByClassName('form-control')

    // Loop over each input and watch blue event
    var validation = Array.prototype.filter.call(inputs, function(input) {

      input.addEventListener('blur', function(event) {
        // reset
        input.classList.remove('is-invalid')
        input.classList.remove('is-valid')

        if (input.checkValidity() === false) {
            input.classList.add('is-invalid')
            input.nextElementSibling.nextElementSibling.classList.remove('spaceholder')
        }
        else {
            input.classList.add('is-valid')
            input.nextElementSibling.nextElementSibling.classList.remove('spaceholder')
        }
      }, false);
    });
  }, false);

  // Fetch all the forms we want to apply custom Bootstrap validation styles to
  var forms = document.querySelectorAll('.needs-validation');

  // Loop over them and prevent submission
  Array.prototype.slice.call(forms)
    .forEach(function (form) {
      form.addEventListener('submit', function (event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })

})()

// --------------------------------------
// Copyright Date
// --------------------------------------
var date = new Date();
var year = date.getFullYear();

document.getElementById("date").innerHTML = year;