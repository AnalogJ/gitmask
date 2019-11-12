'use strict';
const nconf = require('./nconf');

module.exports = {

    successHandler: function(payload, success_code, headers){
        var response = {
            statusCode: success_code || 200,
            headers: headers || {},
            body: JSON.stringify(payload,null, 2),
        }
        return response
    },

    /*
    * Error handler can be used as follows:
    * var Helpers = require('../helpers');
    * Helpers.errorHandler(cb)(err)
    * or
    * Promise.fail(Helpers.errorHandler(cb))
    *
    * */
    errorHandler: function(err, headers){
        if (typeof err === 'string'){
            //this is a string error message, wrap it in an error obj
            err = new Error(err)
        }
        else if(!err instanceof Error){
            //this is an object or something other than an error obj
            //do nothing for now.
        }

        console.error("Inside Error Handler:");
        console.dir(err) //make sure we log the full error message

        //if this is a production environment. we need to be careful about the data we return on error.
        if (nconf.get('STAGE') != 'beta'){
            err = new Error(err.message || 'Unknown error')
        }

        var response = {
            statusCode: err.status || err.statusCode || err.code || 500,
            headers: headers || {},
            body: JSON.stringify({error: err}),
        }
        return response
    }
}
