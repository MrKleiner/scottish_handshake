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
from ft.upload import *
cgitb.enable()
from zipfile import ZipFile
# output = sys.stdout.buffer.write
from util import eval_hash

# important todo: it'd actually be better to do this multi-file...
# the setup could be totally done trough classes
# so that the setup in the very beginning of every file is as short as initting a class


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

server['auth_cl'] = auth_db.get(url_params.get('auth'))

tmpdir = Path(server['cfg']['preview_db']) / 'temp_shite'

# =============================================
#					Setup
# =============================================





def give_file():
	# fuck it, it's always byte data
	sys.stdout.buffer.write(b'Content-Type: application/octet-stream\r\n')
	sys.stdout.buffer.write(f"""Content-Disposition: attachment; filename="photos.zip"\r\n""".encode())
	sys.stdout.buffer.write(f"""X-Sendfile: {str(url_params['dlink']).strip()}\r\n\r\n""".encode())

def gen_file():
	zp_paths = json.loads(byte_data)
	zip_path = str(tmpdir / eval_hash(str(str(random()) + str(random())))) + '.zip'
	with ZipFile(zip_path, 'w') as zip:
		for file in zp_paths:
			zip.write(str(file), Path(file).name)
	sys.stdout.buffer.write(b'Content-Type: application/octet-stream\n\n')
	sys.stdout.buffer.write(zip_path.encode())


if url_params.get('action') == 'gen_file':
	gen_file()
if url_params.get('action') == 'give_file':
	give_file()