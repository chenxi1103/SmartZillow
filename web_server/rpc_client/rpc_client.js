var jayson = require('jayson');

// create a client connected to backend server
var client = jayson.client.http({
    hostname: 'localhost',
    port: 4040
});

// In most time, callback is required in nodejs, it depends what should we do after successfully calling the fuction in backend
// This fucntion is calling the function in pyjsonrpc server (backend)
function add(a, b, callback){
    // first parameter: function name you want to call
    // second parameter: list of required parameters
    // third parameter(function): 
    // 1st err: represent the error that happens during the process of calling function from server
    // 2nd error: represent the error happends in running this function (e.g. a or b is not a number)
    // response: the result after run successfully
    client.request('add',[a, b], function(err, error, response){
        if(err) throw err;
        console.log(response);
        callback(response);
    });
}

function searchArea(query, callback){
    client.request('searchArea',[query], function(err, error, response){
        if(err) throw err;
        console.log(response);
        callback(response);
    });
}

// Need to export the client functions. Otherwise, other node file cannot see this function\

module.exports = {
    add: add,
    searchArea: searchArea
}