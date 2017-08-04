'use strict';
const debug = require('debug')('gitmask:patch');
var nconf = require('./common/nconf')
// require("lambda-git")();
var Q = require("q");  // npm install q
var exec = require('child_process').exec;
var GitHubApi = require("github");

var github = new GitHubApi({
    Promise: Q.Promise,
    timeout: 5000
});
var tmp = require('tmp');
var git = require('./common/git');


module.exports.handler = (event, context, callback) => {

    var log = []
    log.push("#### Gitmask is running...")

    //determine the repo that we need to fork
    var dest_scm = event.path.scm
    var dest_org = event.path.org
    var repo_parts = event.path.repo.split("@") //use @ syntax to split ref, ie. github.com/AnalogJ/capsulecd@feature_branch or 1.2.4
    var dest_repo =repo_parts[0];
    var dest_ref = "";
    if(repo_parts.length == 2){
        dest_ref = repo_parts[1]
    }

    if(dest_scm != 'github.com'){
        log.push("FATAL! We cannot handle scm's other than github.com")
        return callback(null, log)
    }

    log.push('Destination Repository: ' + dest_org + '/' + dest_repo )
    log.push('Destination Ref: ' + dest_ref)
    // log.push('Anonymous Commmits: ' + oldrev + '..' + newrev)

    log.push('Authenticating to Github')
    // user token
    github.authenticate({
        type: "token",
        token: nconf.get('GITHUB_API_TOKEN')
    });

    log.push('Forking repository anonymously')
    github.repos.fork({
        owner: dest_org,
        repo: dest_repo
    })
        .then(function(){
            log.push('Cloning forked repository')

            var tmpobj = tmp.dirSync();

            return git.cloneRepo('capsuleCD', dest_repo, tmpobj.name, dest_ref)
        })
        .then(function(clone_stdout){
            log.push('Anonymizing and applying patches')
        })
        .then(function(){
            log.push('Pushing local changes up to github')
        })
        .then(function(){
            log.push('Creating pull request with Ghost user')
        })
        .then(function(){
            log.push('Creating message on PR issue')
        })
        .then(function(){
            log.push('Deleting forked repository')
        })
        .then(function(){
            log.push('Your pull request is live at the following url: ')
        })
        .then(function(){
            return callback(null, log);
        })
};
