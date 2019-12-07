
const button2 = document.getElementById('ntButton');
button.addEventListener('click', function(e) {
  console.log('button was clicked');

  fetch('/ntClicked', {method: 'POST'})
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