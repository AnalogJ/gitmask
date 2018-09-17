var nconf = require('./nconf');
module.exports = {


    deploy_sha: nconf.get('DEPLOY_SHA'),
    buckets: {
        // upload bucket contains files that are temporarily located in S3, and will need to be processed, ie:
        // - files manually uploaded via WebUI
        upload: nconf.get('GITMASK_SERVICE') + '-' + nconf.get('STAGE') + '-upload',
    }
}
