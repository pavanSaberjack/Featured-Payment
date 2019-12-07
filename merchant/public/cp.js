
const button1 = document.getElementById('otpButton');
button.addEventListener('click', function(e) {
  console.log('button was clicked');

  fetch('/otpClicked', {method: 'POST'})
    .then(function(response) {
      if(response.ok) {
        console.log('Click was recorded');
        return;
      }
      throw new Error('Request failed.');
    })
    .catch(function(error) {
      console.log(error);
    });
});
