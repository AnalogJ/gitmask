module.exports.normalizeInput = function (str){
    return str.replace(/[^a-z0-9\-\.\_]+/gi, '');
}