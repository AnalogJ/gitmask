

# Resources
- http://weininger.net/configuration-of-nginx-for-gitweb-and-git-http-backend.html
- https://gist.github.com/massar/9399764
- https://stackoverflow.com/questions/22891148/nginx-how-to-run-a-shell-script-on-every-request
- https://github.com/markvnext/nginx-luarocks-docker/blob/master/nginx.sh
- https://git-scm.com/docs/git-http-backend
- https://apuntesderootblog.wordpress.com/2015/06/01/how-to-run-gitweb-and-git-http-backend-with-nginx-in-fedora/
- https://help.github.com/articles/changing-author-info/
- https://help.github.com/articles/pushing-to-a-remote/



# Why?
popcornhour
shadowproxy
bitcoin
truecrypt
rapid7/metasploit-framework
magnumripper/JohnTheRipper
tor
bittorrent


http://www.eremedia.com/sourcecon/how-to-find-almost-any-github-users-email-address/
http://www.businessinsider.com/joke-github-dicss-project-goes-nuts-2015-3
https://github.com/letsgetrandy/brototype
https://github.com/letsgetrandy/DICSS
http://developers.slashdot.org/story/15/03/22/1748238/a-software-project-full-of-male-anatomy-jokes-causes-controversy




# Examples
git bundle create commits.bundle public_branch..local_branch \
&& curl -v -H "Content-Type:application/x-binary" -X POST \
	--data-binary "@commits.bundle" https://git.gitmask.com/beta/patch/github.com/AnalogJ/tags_analogj_test

curl -L -H "Content-Type:application/json" -v -X POST \
	--data-binary "@commits.bundle" https://git.gitmask.com/beta/bundle/github.com/AnalogJ/tags_analogj_test/master

curl -v -H "Content-Type:application/json" -X POST \
	--data-binary "@commits.bundle" http://localhost:3000/bundle/github.com/analogj/test/master

curl -L -v -H -X POST --data-binary "@commits.bundle" http://localhost:3000/bundle/github.com/analogj/test/master



# WORKING!! 2 Step
curl -v -X PUT \
	--upload-file commits.bundle https://git.gitmask.com/beta/bundle/github.com/AnalogJ/tags_analogj_test/master
curl -v -X PUT \
	--upload-file commits.bundle "<PUT LOCATION URL HERE, IN QUOTES>"

# WORKING 1 STEP

curl -v -L -X PUT \
	--upload-file commits.bundle https://git.gitmask.com/beta/bundle/github.com/AnalogJ/tags_analogj_test/master

docker run -it -v "$PWD":/var/task lambci/lambda /bin/bash


# Resources
- https://git-scm.com/blog/2010/03/10/bundles.html