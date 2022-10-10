




def vdman_upd_pool_paths(prms=None, dt=None, sv=None):
	from pathlib import Path
	import json

	(sv['root'] / 'db' / 'catalogue' / 'video_index.pootis').write_bytes(dt)
	
	return json.dumps({'status': 'success'})

def vdman_get_pool_paths(prms=None, dt=None, sv=None):
	from pathlib import Path
	import json

	video_index_catalogue = (sv['root'] / 'db' / 'catalogue' / 'video_index.pootis').read_bytes()

	return video_index_catalogue