'use strict';
var nconf = require('./common/nconf')
var Q = require("q");  // npm install q
var exec = require('child_process').exec;
var GitHubApi = require("github");

var github = new GitHubApi({
    Promise: Q.Promise,
    timeout: 5000
});
var tmp = require('tmp');
var git = require('./common/git');

var Logger = require('./common/logger')


module.exports.handler = (event, context, callback) => {
    var logger = new Logger()

    logger.info("#### Gitmask is running...")

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
        logger.info("FATAL! We cannot handle scm's other than github.com")
        return callback(null, JSON.stringify(logger.get()))
    }

    logger.info('Destination Repository: ' + dest_org + '/' + dest_repo )
    logger.info('Destination Ref: ' + dest_ref)
    // logger.info('Anonymous Commmits: ' + oldrev + '..' + newrev)

    logger.info('Authenticating to Github')
    // user token
    github.authenticate({
        type: "token",
        token: nconf.get('GITHUB_API_TOKEN')
    });

    logger.info('Forking repository anonymously')
    github.repos.fork({
        owner: dest_org,
        repo: dest_repo
    })
        .then(function(){
            logger.info('Cloning forked repository')

            var tmpobj = tmp.dirSync();

            return git.cloneRepo(logger, nconf.get('GITHUB_API_TOKEN'), 'capsuleCD', dest_repo, tmpobj.name, dest_ref)
        })
        .then(function(clone_stdout){
            logger.info('Anonymizing and applying patches')
        })
        .then(function(){
            logger.info('Pushing local changes up to github')
        })
        .then(function(){
            logger.info('Creating pull request with Ghost user')
        })
        .then(function(){
            logger.info('Creating message on PR issue')
        })
        .then(function(){
            logger.info('Deleting forked repository')
        })
        .then(function(){
            logger.info('Your pull request is live at the following url: ')
        })
        .then(function(){
            return callback(null, logger.get());
        })
        .fail(function(err){
            logger.info("AN ERROR OCCURRED")
            logger.info(err)
            return callback(null, logger.get())
        })
};
