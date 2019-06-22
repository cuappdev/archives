var express = require('express');
var router = express.Router();
var rp = require('request-promise');

var constants = require('./constants.js');

var options = {
    method: 'POST',
    uri: constants.REGISTER_URL,
    body: {
        'device_type' : constants.IOS_DEVICE,
        'test-type' : constants.TEST_TYPE
    },
    headers : {
      "Authorization": "Basic NEEDS_CHANGING",
      "Content-Type": constants.CONTENT_TYPE
    },
    json: true
};

var register_options = {
    method: 'POST',
    uri: TEMPO_BACKEND,
    body: {},
    headers : {
      "Content-Type": "application/json"
    },
    json: true
};

var push_options = {
  method: 'POST',
  uri: PUSH_URL,
  body : {},
  headers : {
    "Authorization": "Basic NEEDS_CHANGING",
    "Content-Type": "application/json"
  },
  json: true
}

/* GET home page. */
router.get('/', function(req, res, next) {
  res.json({"message": "success!"})
});

router.post('/push', function(req, res, next) {
  var app = req.body.app;
  var appID = process.env[app];
  push_options.body.app_id = appID;
  push_options.body.include_player_ids = req.body.target_ids;
  push_options.body.contents = {"en" : req.body.message}
  console.log(push_options);
  rp(push_options)
      .then(function (parsedBody) {
          console.log("success");
          console.log(parsedBody)
          res.status(200).json({"success": "Message successfully sent."})
      })
      .catch(function (err) {
        console.log("error!")
        console.log(err)
      });
});

router.post('/register_user', function(req, res, next) {
  var app = req.body.app;
  var appID = process.env[app];
  options.body.app_id = appID;
  options.body.identifier = req.body.push_id;

  rp(options)
      .then(function (parsedBody) {
          var new_options = register_options;
          new_options.body = {
            user_id : req.body.user_id,
            push_id : parsedBody.id,
            app_id  : process.env[req.body.app]
          }
          rp(new_options)
              .then(function (parsedBody) {
                  console.log("success2");
                  console.log(parsedBody)
                  res.status(200).json({"success": "User successfully registered."})
              })
              .catch(function (err) {
                console.log("error!")
                console.log(err)
              });
      })
      .then(function (parsedBody) {
        console.log("WOOOOOOO")
      })
      .catch(function (err) {
        console.log("error!")
        console.log(err)
      });
});

router.get('/register_test_user', function(req, res, next){
  var app = "TEMPO";
  var appID = process.env[app];
  options.body.app_id = appID;
  options.body.identifier = req.body.push_id;
  console.log(options)

  rp(options)
      .then(function (parsedBody) {
          console.log(parsedBody)
          res.status(200).json({"success": "User successfully registered."})
      })
      .catch(function (err) {
        console.log("error!")
        console.log(err)
      });
})

module.exports = router;
