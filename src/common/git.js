var exec = require('child_process').exec;


function cloneRepo(repoOwner, repoName, destination, ref){
    var deferred = q.defer();

    var cmd = `git clone --depth 1 https://github.com/${repoOwner}/${repoName} ${destination}`
    if(ref){
        cmd = `git clone -b ${ref} --single-branch --depth 1 https://github.com/${repoOwner}/${repoName} ${destination}`
    }

    exec(cmd, {}, function(err, stdout, stderr) {
        if (err) return deferred.reject(err);
        return deferred.resolve(stdout)
    });
    return deferred.promise
}


module.exports.cloneRepo = cloneRepo