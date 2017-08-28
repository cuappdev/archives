import basicAuth from 'basic-auth';

export default function(req, res, next) {
  function unauthorized(res) {
    res.set('WWW-Authenticate', 'Basic realm=Authorization Required');
    return res.sendStatus(401);
  };

  var user = basicAuth(req);

  if (!user || !user.name || !user.pass) {
    return unauthorized(res);
  };

  if (user.name === 'cuappdev' && user.pass === 'railroad') {
    return next();
  } else {
    return unauthorized(res);
  };
}
