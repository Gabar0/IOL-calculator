//Global scripts
//document.getElementById
//document.querySelectorAll
//document.addEventListener
//

// This object maps IOL models to their corresponding A constant values
const iolModelToAConstant = {
  'Alcon SA60AT': 118.85,
  'Alcon SN60WF': 119,
  'Zeiss 829M': 118.32,
  'Zeiss 621P': 119.6,
  'Other Model': '' // Assuming empty value for "Other Model"
};

document.getElementById('iol-model-od').addEventListener('change', function () {
  // Get the selected IOL model
  const selectedModel = this.value;

  // Update the A constant input based on the selected model
  // If the model is not in the map, default to empty
  const aConstant = iolModelToAConstant[selectedModel] || '';
  document.getElementById('a-constant-od').value = aConstant;
});

document.getElementById('iol-model-os').addEventListener('change', function () {
  // Get the selected IOL model
  const selectedModel = this.value;

  // Update the A constant input based on the selected model
  // If the model is not in the map, default to empty
  const aConstant = iolModelToAConstant[selectedModel] || '';
  document.getElementById('a-constant-os').value = aConstant;
});

function resetForm() {
  // Select all input and select elements within the OD section
  const odInputs = document.querySelectorAll('.eye-section-OD input, .eye-section-OD select');
  // Reset each input/select to its default value
  odInputs.forEach(input => {
    input.value = input.defaultValue;
  });

  // Do the same for the OS section
  const osInputs = document.querySelectorAll('.eye-section-OS input, .eye-section-OS select');
  osInputs.forEach(input => {
    input.value = input.defaultValue;
  });
}





/*document.getElementById('al-od').addEventListener('input', function() {
    const value = parseFloat(this.value);
    const errorMessage = document.getElementById('error-message');
  
    if (value < 15.00 || value > 40.00) {
      this.classList.add('error');
      errorMessage.style.display = 'block';
    } else {
      this.classList.remove('error');
      errorMessage.style.display = 'none';
    }
  });
*/

function addValidationListener(inputId, min, max, errorMessageId) {
  document.getElementById(inputId).addEventListener('input', function () {
    const value = parseFloat(this.value);
    const errorMessage = document.getElementById(errorMessageId);

    if (value < min || value > max) {
      this.classList.add('error');
      errorMessage.style.display = 'block';
    } else {
      this.classList.remove('error');
      errorMessage.style.display = 'none';
    }
  });
}

document.addEventListener('DOMContentLoaded', function () {
  addValidationListener('al-od', 15.00, 40.00, 'error-message-al-od');
  addValidationListener('acd-od', 1.50, 6.00, 'error-message-acd-od');
  addValidationListener('k1-od', 35.00, 65.00, 'error-message-k1-od');
  addValidationListener('k2-od', 35.00, 65.00, 'error-message-k2-od');
});

document.addEventListener('DOMContentLoaded', function () {
  addValidationListener('al-os', 15.00, 40.00, 'error-message-al-os');
  addValidationListener('acd-os', 1.50, 6.00, 'error-message-acd-os');
  addValidationListener('k1-os', 35.00, 65.00, 'error-message-k1-os');
  addValidationListener('k2-os', 35.00, 65.00, 'error-message-k2-os');
});

// Attach the resetEyeSections function to the reset button
document.querySelector('button[type="reset"]').addEventListener('click', resetForm);






