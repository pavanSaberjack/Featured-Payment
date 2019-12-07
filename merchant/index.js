const express = require('express');

const app = express();
const PORT = process.env.PORT || 3000;
const axios = require('axios');
const targetBaseUrl = 'http://localhost:3000/';

const API_OTP = "https://www.google.com";
const API_CON = "https://www.google.com";

app.use(express.static(`${__dirname}/public`));

app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});


app.get('/', (req, res, next) => {
  res.sendFile(`${__dirname}/public/index.html`);
});



//Request for OTP Initation//
app.post('/confirm', (req, res) => {
  
  axios.get(API_OTP)
  .then(response => {
    console.log(response.data.url);
    console.log(response.data.explanation);
    res.render('/confirmationPage.html')
    // res.redirect('confirmationPage.html');
  })
  .catch(error => {
    console.log(error);
  });

});


app.post('/otpClicked', (req, res) => {
  
  axios.get(API_CON)
  .then(response => {
    console.log(response.data.url);
    console.log(response.data.explanation);
    res.redirect(targetBaseUrl + `success.html`);
  })
  .catch(error => {
    console.log(error);
  });

});


app.post('/ntClicked', (req, res) => {
  res.redirect(targetBaseUrl + `index.html`);
});