'use strict';
const debug = require('debug')('gitmask:bundle');
var nconf = require('./common/nconf')
var q = require("q");  // npm install q
var fs = require('fs');
var crypto = require('crypto');

var AWS = require('aws-sdk');
var s3 = new AWS.S3({apiVersion: '2006-03-01'});

var GitHubApi = require("github");
var github = new GitHubApi({
    Promise: q.Promise,
    timeout: 5000
});


var tmp = require('tmp');
var git = require('./common/git');


module.exports.handler = (event, context, callback) => {

    // authenticate to github
    // fork the repository anonymously on github
    // clone the forked repository locally
    // download the s3 bundle
    // validate that the bundle file can be applied to this repository.  (git bundle verify ../commits.bundle)
    // get the bundle ref/branch name (so we can do a fetch) (git bundle list-heads ../commits.bundle | awk 'NR==1{ print $2; }')
    // fetch the bundled commits into this repository. (git fetch ../commits.bundle $(bundle branch name):gitmask-anon-branch)
    // checkout the new branch (git checkout gitmask-anon-branch)
    // squash the commits (rewrite-owner, commit message, commit datetime)
    // push the branch up to forked repository
    // open a PR against origin repository, destination branch
    // make a commit with info about gitmask.
    // delete forked repository

    var upload_key = event.Records[0].s3.object.key;
    var upload_bucket = event.Records[0].s3.bucket.name;
    var upload_key_parts = upload_key.split('/');
    //ignore the userhash.h
    var scm = upload_key_parts[0];
    var org = upload_key_parts[1];
    var repo = upload_key_parts[2];
    var branch = upload_key_parts[3];
    var bundle_id = upload_key_parts[4];

    var bundlePath = `/tmp/${bundle_id}`
    var localBranchName = `gitmask-${crypto.randomBytes(10).toString('hex')}`

    var gitmask_org = 'gitmask-anonymous'

    debug("Begin processing bundle: ", upload_key_parts);

    debug('Authenticating to Github')
    github.authenticate({
        type: "token",
        token: nconf.get('GITHUB_API_TOKEN')
    })

    debug('Fork the repository anonymously on github')
    github.repos.fork({
        owner: org,
        repo: repo
    })
        .then(function(){
            debug('Clone the forked repository locally')
            var tmpobj = tmp.dirSync();

            var remote = authRemoteUrl(nconf.get('GITHUB_API_TOKEN'), gitmask_org, repo)
            return git.cloneRepo(remote, tmpobj.name)
                .then(function(){
                    debug('Download the git bundle from s3 for processing')
                    var options = {
                        Bucket    : upload_bucket,
                        Key    : upload_key,
                    };
                    s3.getObject(options)

                    var bundleFile = fs.createWriteStream(bundlePath);
                    s3.getObject(options).createReadStream().pipe(bundleFile);
                })
                .then(function(){
                    debug('Validate that the bundle file can be applied to this repository')
                    return git.validateBundle(tmpobj.name, bundlePath)
                })
                .then(function(){
                    debug('Get the bundle ref/branch name (so we can do a fetch)')
                    return git.bundleBranchName(bundlePath);
                })
                .then(function(bundleBranchName){
                    debug('Found bundle branch name', bundleBranchName)

                    debug('Fetch the bundled commits into local repository')
                    return git.fetchBundleCommits(tmpobj.name, bundlePath, bundleBranchName, localBranchName)
                })
                .then(function(){
                    debug('Checkout the new branch')
                    return git.checkoutBranch(tmpobj.name, localBranchName)
                })
                .then(function(){
                    debug('Squash the commits')
                    //TODO: NEED TO SQUASH AND ANONYMIZE PRS.
                })
                .then(function(){
                    debug('Push the local branch up to forked repository')
                    return git.pushRepo(tmpobj.name, localBranchName)
                })
                .then(function(){
                    debug('Open a PR against dest repository, destination branch');
                    return github.pullRequests.create({
                        owner: org,
                        repo: repo,
                        title: 'Gitmask Anonymous PR',
                        head: `${gitmask_org}:${localBranchName}`,
                        base: branch,
                        body: `This is an anonymous PR submitted via Gitmask - https://www.gitmask.com`

                    })
                })
                .then(function(){
                    debug('Delete forked repository');
                    return github.repos.delete({
                        owner: gitmask_org,
                        repo: repo
                    })
                })
        })






    //
    // logger.info('Forking repository anonymously')
    // github.repos.fork({
    //     owner: dest_org,
    //     repo: dest_repo
    // })
    //     .then(function(){
    //         logger.info('Cloning forked repository')
    //
    //         var tmpobj = tmp.dirSync();
    //
    //         return git.cloneRepo(logger, nconf.get('GITHUB_API_TOKEN'), 'gitmask-anonymous', dest_repo, tmpobj.name, dest_ref)
    //             .then(function(){
    //                 logger.info('Anonymizing and applying patches')
    //
    //                 logger.info(new Buffer(event.body, 'base64'))
    //
    //
    //             })
    //             .then(function(){
    //                 logger.info('Pushing local changes up to github')
    //             })
    //     })
    //     .then(function(){
    //         logger.info('Creating pull request with Ghost user')
    //     })
    //     .then(function(){
    //         logger.info('Creating message on PR issue')
    //     })
    //     .then(function(){
    //         logger.info('Deleting forked repository')
    //     })
    //     .then(function(){
    //         logger.info('Your pull request is live at the following url: ')
    //     })
    //     .then(function(){
    //         return callback(null, logger.get());
    //     })
    //
    //     .fail(function(err){
    //         logger.info("AN ERROR OCCURRED")
    //         logger.info(err)
    //         return callback(null, logger.get())
    //     })
};


//helpers

function authRemoteUrl(authToken, org, repo){
    return `https://${authToken}:@github.com/${org}/${repo}`
}
