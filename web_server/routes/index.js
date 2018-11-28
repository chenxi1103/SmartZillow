var express = require('express');
var router = express.Router();
var User = require('../model/user')

/* GET home page. */
router.get('/', function(req, res, next) {
  res.render('index', { title: 'Smart Zillow' });
});

/* login page. */
router.get('/login', function(req, res, next) {
  res.render('login', { title: 'Smart Zillow: Login' });
});

/* login */
router.post('/login', function(req, res, next) {
  res.render('login', { title: 'Smart Zillow: Login' });
});

/* register page. */
router.get('/register', function(req, res, next) {
  res.render('register', { title: 'Smart Zillow: Register' });
});

/* register */
router.post('/register', function(req, res, next) {
  var email = req.body.email;
  var password = req.body.password;
  User.find({email: email}, function(err, users){
  		if(err) throw err;
  		if(users.length == 0){
  			var newUser = User({
  				email: email,
  				password: password
  			})
  			newUser.save(function(err){
  				if(err) throw err;
  				res.redirect('/');
  			})
  		}else{
  			res.redirect('/')
  		}
  })
});
module.exports = router;
