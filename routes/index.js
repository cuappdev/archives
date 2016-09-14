var express = require('express');
var router = express.Router();

var schedules = require('../TCATJson/route-schedules/route-schedules.json');
var stopLocations = require('../TCATJson/stop-locations/stop-locations.json');
var stopSchedules = require('../TCATJson/stop-schedules/stop-schedules.json');

/* GET home page. */
router.get('/', function(req, res, next) {
  res.json({"message": "Success! You connected."});
});

router.get('/schedules', function(req, res, next) {
  res.json(schedules).status(200);
});

router.get('/stop-locations', function(req, res, next) {
  res.json(stopLocations).status(200);
});


router.get('/stop-schedules', function(req, res, next) {
  res.json(stopSchedules).status(200);
});

module.exports = router;
