
const helper = require('./common/helpers');

module.exports.handler = async (event, context) => {
    console.log(event)
    try {
        console.log(typeof event.body);




    }
    catch(e){
        return helper.errorHandler(e)
    }
}
