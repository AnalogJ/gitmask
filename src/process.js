'use strict';
const debug = require('debug')('gitmask:bundle');
var nconf = require('./common/nconf')
var q = require("q");  // npm install q
var fs = require('fs');
var crypto = require('crypto');
var utils = require('./common/utils');

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
    var scm = utils.normalizeInput(upload_key_parts[0]);
    var org = utils.normalizeInput(upload_key_parts[1]);
    var repo = utils.normalizeInput(upload_key_parts[2])
    var branch = utils.normalizeInput(upload_key_parts[3])
    var bundle_id = upload_key_parts[4]; //we control this part (and includes a '.' so dont normalize)

    var bundlePath = `/tmp/${bundle_id}`;
    var bundleLocalBranchName = `gitmask-bundle`; //this is the name of the branch containing all the commits before squashing.
    var anonLocalBranchName = `gitmask-${crypto.randomBytes(10).toString('hex')}` //this is the squashed and anonymized branch that we push



    var gitmask_org = nconf.get('GITHUB_USER')

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

                    var deferred = q.defer();
                    var options = {
                        Bucket    : upload_bucket,
                        Key    : upload_key,
                    };
                    var bundleFile = fs.createWriteStream(bundlePath);
                    s3.getObject(options)
                        .createReadStream()
                        .pipe(bundleFile)
                        .on('close', function(){
                            deferred.resolve({})
                        })
                        .on('error', function(){
                            deferred.reject("An error occured while retrieving bundle.")
                        })

                    return deferred.promise
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
                    bundleBranchName = bundleBranchName.trim();
                    debug('Found bundle branch name', bundleBranchName)

                    debug('Fetch the bundled commits into local repository')
                    return git.fetchBundleCommits(tmpobj.name, bundlePath, bundleBranchName, bundleLocalBranchName)
                })
                .then(function(){
                    debug('Checkout the new branch')
                    return git.checkoutBranch(tmpobj.name, bundleLocalBranchName)
                })
                .then(function(){
                    debug('Squash the commits')
                    return git.squashCommits(tmpobj.name, branch, anonLocalBranchName, bundleLocalBranchName)

                })
                .then(function(){
                    debug('Push the anonymized local branch up to forked repository')
                    return git.pushRepo(tmpobj.name, anonLocalBranchName)
                })
                .then(function(){
                    debug('Open a PR against dest repository, destination branch');
                    return github.pullRequests.create({
                        owner: org,
                        repo: repo,
                        title: 'Gitmask Anonymous PR',
                        head: `${gitmask_org}:${anonLocalBranchName}`,
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
                .then(function(){
                    callback(null, {})
                })
                .fail(function(err){
                    debug("!!!!!!AN ERROR OCCURRED!!!!!!")
                    debug(err)

                    //cleanup
                    debug('Delete forked repository');
                    return github.repos.delete({
                        owner: gitmask_org,
                        repo: repo
                    })
                        .then(function(){
                            return callback(null, err)
                        })
                })

        })
};


//helpers

function authRemoteUrl(authToken, org, repo){
    return `https://${authToken}:@github.com/${org}/${repo}`
}
