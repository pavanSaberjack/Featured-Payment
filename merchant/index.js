const express = require('express');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.static(`${__dirname}/public`));

app.listen(PORT, () => {
  console.log(`Listening on port ${PORT}`);
});


function verify(phoneNumber) {
  return client.phoneNumbers(phoneNumber).fetch()
    .then(numberData => true, err => false);
}

app.get('/', (req, res, next) => {
  res.sendFile(`${__dirname}/index.html`);
});




app.get('/check/:number', (req, res) => {
  verify(req.params.number)
    .then(valid => {
      res.send({ valid });
    })
    .catch(err => {
      console.error(err.message);
      res.status(500).send('An unexpected error occurred');
    });
});


app.post('/process', (req, res) => {
  verify(req.params.number)
    .then(valid => {
      res.send({ valid });
    })
    .catch(err => {
      console.error(err.message);
      res.status(500).send('An unexpected error occurred');
    });
});


app.post('/clicked', (req, res) => {
  const click = {clickTime: new Date()};
  console.log(click);

  console.log('click added to db');
  res.sendStatus(201);

});