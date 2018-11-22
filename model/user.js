var mongoose = require('mongoose');

var Schema = mongoose.Schema

var userSchema = new Schema({
	email: {type: String, require: true, unique: true},
	password: {type: String, require: true},
	create_at: Date,
	update_at: Date
});

//Run before really save the userSchema data
userSchema.pre('save', function(next){
	var currTime = new Date();
	//If user just change the password
	this.update_at = currTime;
	//If this is the first time that user register
	if(!this.create_at){
		this.create_at = currTime;
	}

	next();
})

var User = mongoose.model('users',userSchema);
module.exports = User;