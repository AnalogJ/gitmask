const {
    collect
} = require('isomorphic-git/dist/for-node/isomorphic-git/internal-apis');
// const git = require('isomorphic-git/internal-apis');
const writeReceivePackAdResponse = require('./lib/wire/writeReceivePackAdResponse')


const helper = require('./common/helpers');

module.exports.handler = async (event, context) => {
    console.log(event)
    try {

        if (event.queryStringParameters == null
            || event.queryStringParameters == undefined
            || event.queryStringParameters.service == null
        ) {
            throw new Error("Only Git Smart Http Protocol is supported. Please update your git version")
        }

        if (event.queryStringParameters.service == 'git-upload-pack'){
            throw new Error("Git pull is not supported.")
        }
        if (event.queryStringParameters.service != 'git-receive-pack'){
            throw new Error("Unsupported action")
        }





        const res = await writeReceivePackAdResponse({
            service: event.queryStringParameters.service,
            //https://git-scm.com/docs/protocol-capabilities
            capabilities: [
                'report-status',
                'delete-refs',
                'quiet',
                'atomic',
                'ofs-delta'
            ],
            symrefs: { HEAD: 'refs/heads/master' },
            refs: {
                HEAD: '77809f09ab44042d55e17632ea6081d7da90f450',
                'refs/heads/beta': 'c9f7aa5d2012d1c6f207f615375589b3439f6aaa',
                'refs/heads/master': '77809f09ab44042d55e17632ea6081d7da90f450',

            }
        })

        const buffer = await collect(res)


        return {
            statusCode:  200,
                headers: {'Content-Type': `application/x-${event.queryStringParameters.service}-advertisement`},
                body: buffer.toString('utf8')
        }
    }
    catch(e) {
        return helper.errorHandler(e)

    }

}
