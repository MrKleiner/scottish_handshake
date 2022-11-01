




# load users database
# token is not passed intentionally
def profiler_load_users(prms=None, dt=None, sv=None):
	from pathlib import Path
	import json

	users = []

	user_db = json.loads(Path(sv['cfg']['auth_db_loc']).read_bytes())

	for usr in user_db:
		users.append({
			'login': usr,
			'pswd': user_db[usr]['pswd']
		})

	return json.dumps(users)


# save users database
# todo: keep a few backups of the databse, like .bend1, .blend2, blend3
# important todo: for now this also responsible for creating new profiles...
def save_user_profiles(prms=None, dt=None, sv=None):
	from pathlib import Path
	import json
	import random
	import sys
	sys.path.append('.')
	from util import eval_hash

	old_db_loc = Path(sv['cfg']['auth_db_loc'])

	old_db = json.loads(old_db_loc.read_bytes())

	# don't forget to update clearance db
	cldb_loc = Path(sv['cfg']['clearance_db'])
	cldb = json.loads(cldb_loc.read_bytes())

	new_db = {}

	new_cl_db = {}

	# eval input into json
	inp = json.loads(dt)

	# overwrite old db with new data
	for usr in inp:
		# if this user does not exist - create it
		if not old_db.get(usr):
			# important todo: this is absolutely fucking retarded
			# generate random access token
			seed = str(random.random()) + str(random.random()) + str(random.random())
			super_token = eval_hash(seed, 'sha256')

			new_db[usr] = {
				'pswd': inp[usr],
				'token': super_token
			}

			# add token to clearance db
			new_cl_db[super_token] = {
				'admin': [],
				'folders': []
			}
		else:
			new_db[usr] = {
				'pswd': inp[usr],
				'token': old_db[usr]['token']
			}
			new_cl_db[old_db[usr]['token']] = cldb[old_db[usr]['token']]

	old_db_loc.write_bytes(json.dumps(new_db, indent=4).encode())
	cldb_loc.write_bytes(json.dumps(new_cl_db, indent=4).encode())

	return json.dumps('good')


# Load access definition list
# Again, no tokens on purpose
def profiler_load_access_list(prms=None, dt=None, sv=None):
	from pathlib import Path
	import json

	# collapse token clearance and nicknames into a single dict
	clr_dict = {}

	clearance_db = json.loads(Path(sv['cfg']['clearance_db']).read_bytes())
	user_db = json.loads(Path(sv['cfg']['auth_db_loc']).read_bytes())

	for usr in user_db:
		clr_dict[usr] = clearance_db[user_db[usr]['token']]

	return json.dumps(clr_dict)



# Load access definition list
# Again, no tokens on purpose
def profiler_save_access_list(prms=None, dt=None, sv=None):
	from pathlib import Path
	import json

	# evaluate input as json
	input_cl = json.loads(dt)

	# new_clr_dict = {}

	cl_db_path = Path(sv['cfg']['clearance_db'])
	clearance_db = json.loads(cl_db_path.read_bytes())
	user_db = json.loads(Path(sv['cfg']['auth_db_loc']).read_bytes())

	for usr in input_cl:
		clearance_db[user_db[usr]['token']]['folders'] = input_cl[usr]['folders']
		clearance_db[user_db[usr]['token']]['admin'] = input_cl[usr]['admin']

	cl_db_path.write_bytes(json.dumps(clearance_db).encode())

	return 'clearance db save ok'


def spawn_match_struct(prms=None, dt=None, sv=None):
	from pathlib import Path
	import json

	sysroot = Path(json.loads((sv['root'] / 'db' / 'root.json').read_bytes())['root_path'])
	# check whether the team exists or nah
	if not (sysroot / prms['team']).is_dir():
		return json.dumps({'status': 'fail', 'reason': 'requested team does not exist', 'details': str(sysroot / prms['team'])})

	# now check for duplicate folders
	if (sysroot / prms['team'] / prms['newfld']).is_dir():
		return json.dumps({'status': 'fail', 'reason': 'duplicate names', 'details': str(sysroot / prms['team'] / prms['newfld'])})

	# finally, create the folder WITH subfolders n shit
	tgt_match = (sysroot / prms['team'] / prms['newfld'])
	tgt_match.mkdir()
	(tgt_match / 'video').mkdir(exist_ok=True)
	(tgt_match / 'photo').mkdir(exist_ok=True)
	(tgt_match / 'moments').mkdir(exist_ok=True)
	(tgt_match / 'pressa').mkdir(exist_ok=True)
	(tgt_match / 'photosession').mkdir(exist_ok=True)

	return json.dumps({'status': 'all_good'})