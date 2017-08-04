#!/usr/bin/env python
import subprocess, os
import sys, json, datetime
import glob
import datetime

cust_env = os.environ.copy()
cust_env['DOMAIN'] = cust_env.get('DOMAIN','git.gitmask.com')
cust_env['API_GATEWAY_NAME'] = cust_env.get('API_GATEWAY_NAME', 'beta-gitmask-api')
cust_env['PROVIDER'] = cust_env.get('PROVIDER', 'cloudflare')
#export LEXICON_CLOUDFLARE_USERNAME=*Should be set in env*
#export LEXICON_CLOUDFLARE_TOKEN=*Should be set in env*

###############################################################################
# The script below expects the following environmental variables to be defined:
# - DOMAIN
# - API_GATEWAY_NAME
# - PROVIDER
# - LEXICON_*_USERNAME & LEXICON_*_TOKEN
#
# When provided with the correct environmental variables it will do the following:
# - validate that the specified AWS API Gateway exists
# - generate a new set of letsencrypt certificates for the specified Domain
# - register custom domain name with AWS (and create a distribution domain name)
# - add a CNAME dns record mapping your custom domain to AWS distribution domain
# - map custom domain to API Gateway name
#
# Nothing below this line should be changed.
###############################################################################


print "Generating letsencrypt SSL Certificates for '{0}'".format(cust_env['DOMAIN'])
subprocess.call([
  'docker', 'run',
  '-e', 'PROVIDER={0}'.format(cust_env['PROVIDER']),
  '-e', 'LEXICON_CLOUDFLARE_USERNAME',
  '-e', 'LEXICON_CLOUDFLARE_TOKEN',
  '-e', 'LEXICON_CLOUDFLARE_TOKEN'.format(cust_env['LEXICON_'+cust_env['PROVIDER'].upper()+'_TOKEN']),
  '-e', 'DOMAIN={0}'.format(cust_env['DOMAIN']),
  '-e', 'API_GATEWAY_NAME={0}'.format(cust_env['API_GATEWAY_NAME']),
  '-e', 'AWS_ACCESS_KEY_ID',
  '-e', 'AWS_DEFAULT_REGION',
  '-e', 'AWS_SECRET_ACCESS_KEY',
  # '-v', '{0}/certs:/srv/certs'.format(os.getcwd()),
  '--rm',
  'analogj/aws-api-gateway-letsencrypt'
])

