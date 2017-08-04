const debug = require('debug')('gitmask:logger');
function Logger() {
    this._log = [];
}

Logger.prototype.info = function(message) {
    this._log.push(`INFO: ${message}`)
    debug(message)
};

Logger.prototype.get = function(){
    return this._log;
}

module.exports = Logger;