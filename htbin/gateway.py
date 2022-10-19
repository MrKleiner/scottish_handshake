#!/usr/bin/python3.9
import os, sys, json, hashlib, base64, cgi, cgitb
# from tools import *
from pathlib import Path
from random import seed
from random import random

# MODULES
from vidman.vidman import *
from profiles.login import *
from profiles.profiler import *
from poolsys.poolsys import *
cgitb.enable()

output = sys.stdout.buffer.write




# =============================================
#					Setup
# =============================================

# parse url params into a dict, if any
get_cgi_params = cgi.parse()
url_params = {}
for it in get_cgi_params:
	url_params[it] = ''.join(get_cgi_params[it])

# read body content, if any
byte_data = b''
try:
	byte_data = sys.stdin.buffer.read()
except:
	pass


# fuck it, it's always byte data
output(b'Content-Type: application/octet-stream\n\n')
# sys.stdout.buffer.write(b'sex')

# server root folder
server_root = Path(__file__).parent.parent

# basic server meta
server = {
	'root': server_root,
	'cfg': json.loads((server_root / 'htbin' / 'server_config.json').read_bytes())
}

# auth_db root
auth_db = json.loads(Path(server['cfg']['clearance_db']).read_bytes())



# =============================================
#					Setup
# =============================================







# =============================================
#					Init all systems (why??)
# =============================================

pool_sys = poolsys(url_params, byte_data, server)



# =============================================
#					Init all systems (why??)
# =============================================















# =============================================
#					Trigger
# =============================================


# classified info:

# reject reasons:
# 1809246: bad auth
# 1809246/nen: missing params

# 2446: invalid auth username
# 314: invalid auth password



# structure: Params, Data, server root folder
# only bother if auth parameter is present
# auth = clearance token
if url_params.get('action') and url_params.get('auth'):
	# auth clearance
	auth_cl = auth_db.get(url_params['auth'])



	#
	# Admin
	#


	#
	# List users
	#
	if url_params['action'] == 'list_users' and 'admin' in auth_cl['admin']:
		output(profiler_load_users(url_params, byte_data, server).encode())

	#
	# Save users
	#
	if url_params['action'] == 'save_user_profiles' and 'admin' in auth_cl['admin']:
		output(save_user_profiles(url_params, byte_data, server).encode())


	#
	# Load List user allowance
	#
	if url_params['action'] == 'load_access_list' and 'admin' in auth_cl['admin']:
		output(profiler_load_access_list(url_params, byte_data, server).encode())


	#
	# Save List user allowance
	#
	if url_params['action'] == 'save_allowance_list' and 'admin' in auth_cl['admin']:
		output(profiler_save_access_list(url_params, byte_data, server).encode())












	#
	# Auth. Public.
	#
	if url_params['action'] == 'login':
		# returns login token
		output(do_login_token(url_params, byte_data, server).encode())






	#
	# File sys
	#
	if url_params['action'] == 'poolsys.list_leagues':
		output(pool_sys.list_leagues.encode())

	if url_params['action'] == 'poolsys.list_league_matches':
		output(pool_sys.list_league_matches.encode())

	if url_params['action'] == 'poolsys.list_match_struct':
		output(pool_sys.list_match_struct.encode())

	if url_params['action'] == 'poolsys.list_media':
		output(pool_sys.list_media.encode())

	if url_params['action'] == 'poolsys.load_media_preview':
		output(pool_sys.load_media_preview)

	if url_params['action'] == 'poolsys.load_fullres_pic':
		output(pool_sys.load_fullres_pic)






else:
	output(json.dumps({'status': 'incomplete_request'}).encode())





