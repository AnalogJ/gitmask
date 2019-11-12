const { GitPktLine, pkg } = require('isomorphic-git/dist/for-node/isomorphic-git/internal-apis');

module.exports = async function writeReceivePackAdResponse ({ service, capabilities, refs, symrefs }) {
    const stream = []
    // Compose capabilities string
    let syms = ''
    // for (const [key, value] of Object.entries(symrefs)) {
    //     syms += `symref=${key}:${value} `
    // }
    let caps = `\x00${[...capabilities].join(' ')} ${syms}agent=${pkg.agent}`

    stream.push(GitPktLine.encode(`# service=${service}\n`))
    stream.push(GitPktLine.flush())
    // Note: In the edge case of a brand new repo, zero refs (and zero capabilities)
    // are returned.
    for (const [key, value] of Object.entries(refs)) {
        stream.push(GitPktLine.encode(`${value} ${key}${caps}\n`))
        caps = ''
    }
    stream.push(GitPktLine.flush())
    return stream
}
