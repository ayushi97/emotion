var port = 3000;
var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var morgan = require('morgan');
var cors = require('cors');
var zerorpc = require("zerorpc");

var server = new zerorpc.Server({
    hello: function(name, reply) {
        reply(null, "Hello, " + name);
    }
});

server.bind("tcp://127.0.0.1:4242");

app.use(morgan('dev'));
app.use(cors());


app.listen(port);
console.log('Server running !!');