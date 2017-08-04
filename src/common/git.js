var exec = require('child_process').exec;
var q = require("q");  // npm install q
require("lambda-git")({
    updateEnv: true
});

function cloneRepo(logger, repoOwner, repoName, destination, ref){
    var deferred = q.defer();

    var cmd = `/tmp/git/usr/bin/git clone --depth 1 https://github.com/${repoOwner}/${repoName} ${destination}`
    if(ref){
        cmd = `/tmp/git/usr/bin/git clone -b ${ref} --single-branch --depth 1 https://github.com/${repoOwner}/${repoName} ${destination}`
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