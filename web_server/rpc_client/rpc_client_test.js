var client = require('./rpc_client');

client.add(1, 2, function(response) {
    console.log("1 + 2 = " + response);
});

client.searchArea('94080', function(response) {
    console.log('94080: ' + response);
});
