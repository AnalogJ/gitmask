'use strict';
const debug = require('debug')('gitmask:bundle');
var nconf = require('./common/nconf')
var AWS = require('aws-sdk');
var s3 = new AWS.S3({apiVersion: '2006-03-01'});
var constants = require('./common/constants');
var utils = require('./common/utils');
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

    var scm = utils.normalizeInput(event.pathParameters.scm);
    var org = utils.normalizeInput(event.pathParameters.org);
    var repo = utils.normalizeInput(event.pathParameters.repo);
    var branch = utils.normalizeInput(event.pathParameters.branch)

    const response = {
        statusCode: 307,
        headers: {
            "Location": s3.getSignedUrl('putObject', {
                Bucket: constants.buckets.upload,
                Key: `${scm}/${org}/${repo}/${branch}/${id}.git.bundle`,
                Expires: 60 //seconds
            })
        },
        body: ""
    };

    debug("Redirecting user to:", response);

    return callback(null, response);
};
