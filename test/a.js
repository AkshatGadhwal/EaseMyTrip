// express server on port 3000
var express = require('express');
var app = express();

app.get('/', function (req, res) {
  res.send('Hello World!');
});

app.listen(3000, function () {
  console.log('Example app listening on port 3000!');
});

// return current time
app.get('/time', function (req, res) {
    res.send(new Date().toString());
});
