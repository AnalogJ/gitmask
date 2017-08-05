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


module.exports.cloneRepo = function(gitRemote, destination){
    return execGitCmd(`git clone --depth 1 ${gitRemote} ${destination}`)
}

module.exports.validateBundle = function(repoPath, bundlePath){
    // return execGitCmd(`git bundle verify ${bundlePath}`, repoPath)
}

module.exports.bundleBranchName = function(bundlePath){
    return execGitCmd(`git bundle list-heads ${bundlePath} | awk 'NR==1{ print $2; }'`)
}

module.exports.fetchBundleCommits = function(repoPath, bundlePath, bundleBranchName, localBranchName){
    return execGitCmd(`git fetch ${bundlePath} ${bundleBranchName}:${localBranchName}`, repoPath)
}

module.exports.checkoutBranch = function(repoPath, branchName){
    return execGitCmd(`git checkout ${branchName}`, repoPath)
}


module.exports.pushRepo = function(repoPath, branchName){
    return execGitCmd(`git push origin ${branchName}`, repoPath)
}


function execGitCmd(cmd, cwd, env){
    var opts = {}
    if(cwd){
        opts.cwd = cwd;
    }
    if(env){
        opts.env = env
    }
    else{
        opts.env = process.env
    }

    var deferred = q.defer();
    exec(cmd, opts, function(err, stdout, stderr) {
        console.log(" >> STDERR:", stderr)
        if (err) return deferred.reject(err);
        return deferred.resolve(stdout)
    });
    return deferred.promise
}