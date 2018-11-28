//file that specifically used to test client file
var client = require("./rpc_client");
//function: callback function, take the response, in this case, it just print the response to see if the function "add" works
client.add(1, 2, function(response){
	console.log("1+2 = " + response);
});

client.searchArea("94080", function(response){
	console.log("searchArea: " + response);
});