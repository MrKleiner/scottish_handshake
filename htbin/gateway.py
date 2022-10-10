#!\python\bin\python.exe
import os, sys, json, hashlib, base64, cgi
# from tools import *
from pathlib import Path
from random import seed
from random import random

# MODULES
from vidman.vidman import *
from profiles.login import *





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
sys.stdout.buffer.write(b'Content-Type: application/octet-stream\n\n')
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

	if url_params['action'] == 'upd_vid_pool_paths' and 'vdman' in auth_cl:
		# takes a json containing all the video pool paths
		# no parse, no whatever
		sys.stdout.buffer.write(vdman_upd_pool_paths(url_params, byte_data, server).encode())

	if url_params['action'] == 'get_vid_pool_paths' and 'vdman' in auth_cl:
		# returns the video pool sources catalogue as json
		sys.stdout.buffer.write(vdman_get_pool_paths(url_params, byte_data, server))

	#
	# Auth. Public.
	#
	if url_params['action'] == 'login':
		# returns the video pool sources catalogue as json
		sys.stdout.buffer.write(do_login_token(url_params, byte_data, server).encode())
else:
	sys.stdout.buffer.write(json.dumps({'status': 'incomplete_request'}).encode())





