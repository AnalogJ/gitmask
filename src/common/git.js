var exec = require('child_process').exec;
var q = require("q");  // npm install q
var fs = require('fs')
var path = require('path');

var targetDirectory = path.resolve(__dirname, "../../opt/")
var GIT_TEMPLATE_DIR = path.resolve(targetDirectory, 'usr/share/git-core/templates');
var GIT_EXEC_PATH = path.resolve(targetDirectory, 'usr/libexec/git-core');

process.env.PATH = path.resolve(targetDirectory, 'usr/bin') + ":" + process.env.PATH  ;
process.env.GIT_TEMPLATE_DIR = GIT_TEMPLATE_DIR;
process.env.GIT_EXEC_PATH = GIT_EXEC_PATH;


function cloneRepo(logger, token, repoOwner, repoName, destination, ref){
    var deferred = q.defer();

    var cmd = `git clone --depth 1 https://${token}:@github.com/${repoOwner}/${repoName} ${destination}`
    if(ref){
        cmd = `git clone -b ${ref} --single-branch --depth 1 https://${token}:@github.com/${repoOwner}/${repoName} ${destination}`
    }

    logger.info("Cloning repository with the following command.")
    logger.info(cmd)
    logger.info(JSON.stringify(process.env))
    exec(cmd, {
        env: process.env
    }, function(err, stdout, stderr) {
        if (err) return deferred.reject(err);
        return deferred.resolve(stdout)
    });
    return deferred.promise
}


module.exports.cloneRepo = cloneRepo