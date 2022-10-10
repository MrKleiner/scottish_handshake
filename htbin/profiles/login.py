





def do_login_token(prms=None, dt=None, sv=None):
	from pathlib import Path
	import json

	# evaluate server database
	authdb = json.loads(Path(sv['cfg']['auth_db_loc']).read_bytes())

	username_fromdb = authdb.get(prms['username'])

	# check if username exists
	if username_fromdb:
		pswd_fromdb = authdb[prms['username']]['pswd']

		# if received pswd and db pswd match - return token
		if pswd_fromdb == prms['password']:
			return json.dumps({'status': 'success', 'token': authdb[prms['username']]['token']})
		else:
			return json.dumps({'status': 'overflow', 'reason': '314'})
	else:
		return json.dumps({'status': 'margin_error', 'reason': '2446'})



