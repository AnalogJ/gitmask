'use strict';
const debug = require('debug')('gitmask:bundle');
var nconf = require('./common/nconf')
var AWS = require('aws-sdk');
var s3 = new AWS.S3({apiVersion: '2006-03-01'});
var constants = require('./common/constants');
var crypto = require('crypto');

//this function generates a signed url for the upload bucket, which can be used by curl (calibre, web) to upload git bundle files to s3
module.exports.handler = (event, context, callback) => {

    //validate inputs
    debug("Repository options: ", event.pathParameters)

    if(event.pathParameters.scm != 'github.com'){
        debug("FATAL! We cannot handle scm's other than github.com");
        return callback(new Error("Invalid SCM, must be github.com", null))
    }

    var id = crypto.randomBytes(20).toString('hex');

    const response = {
        statusCode: 307,
        headers: {
            "Location": s3.getSignedUrl('putObject', {
                Bucket: constants.buckets.upload,
                Key: `${event.pathParameters.scm}/${event.pathParameters.org}/${event.pathParameters.repo}/${event.pathParameters.branch}/${id}.git.bundle`,
                Expires: 60
            }) // "https://requestb.in/yzm8fbyz"
        },
        body: ""
    };

    debug("Redirecting user to:", response);

    return callback(null, response);
};
