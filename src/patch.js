'use strict';
const debug = require('debug')('gitmask:patch');
var nconf = require('./common/nconf')
module.exports.handler = (event, context, callback) => {

    var versionInfo = {
        'deploySha': nconf.get('DEPLOY_SHA')
    };

    return callback(null, versionInfo);
};
