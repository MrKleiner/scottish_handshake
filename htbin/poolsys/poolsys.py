



def list_root_shite(prms=None, dt=None, sv=None):
	import json
	from pathlib import Path

	# todo: this should be available by this time. Probably...
	sysroot = json.loads((sv['root'] / 'db' / 'root.json').read_bytes())['root_path']

	return json.dumps([fld.name for fld in Path(sysroot).glob('*') if fld.is_dir()])


