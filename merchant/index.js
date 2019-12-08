const express = require('express');
const qs = require('qs');
const FormData = require('form-data');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;
const axios = require('axios');
const targetBaseUrl = 'http://localhost:3000/';
const router = express.Router();

const API_OTP = "http://172.20.10.5:8080/initiate_payment";
const API_CON = "http://172.20.10.5:8080/merchant_confirm_transaction";

// app.use(express.static(`${__dirname}/public`));
app.use(express.static(`${__dirname}/public`), router);

app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});


router.get('/', (req, res, next) => {
  res.sendFile(`${__dirname}/public/index.html`);
});



//Request for OTP Initation//
router.get('/confirm', (req, res) => {
  let mobile = req.query.mobile;
  let amount = req.query.amount;
  let seller_id = 1;

  console.log(mobile);
  axios({
    method:'post',
    url: API_OTP,
    data: qs.stringify({ 'money': amount, 'seller_id': seller_id, 'user_phone': mobile })
  })
  .then(response => {
    console.log(response.data.url);
    console.log(response.data.explanation);
    res.sendFile((`${__dirname}/public/confirmationPage.html`));
  })
  .catch(error => {
    console.log(error);
  });

});


router.post('/success', (req, res) => {
  
  let otp = req.query.otp;
  let seller_id = 1;

  axios({
    method:'post',
    url: API_CON,
    data: qs.stringify({ 'otp': otp, 'seller_id': seller_id, 'user_phone': '9663269499' })
  })
  .then(response => {
    console.log(response.data.url);
    console.log(response.data.explanation);
    res.sendFile((`${__dirname}/public/success.html`));
  })
  .catch(error => {
    console.log(error);
  });

});


router.post('/home', (req, res) => {
  res.sendFile((`${__dirname}/public/index.html`));
});