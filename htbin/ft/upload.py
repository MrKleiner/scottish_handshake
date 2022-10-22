







class imaliar:
	# sorry...
	# WILL FIX ASAP !!!!!!!!!!!!!!
	def __init__(self, prms={}, dt='', sv={}):
		import json
		from pathlib import Path

		self.prms = prms
		self.bin = dt
		self.server = sv
		self.sysroot = Path(json.loads((sv['root'] / 'db' / 'root.json').read_bytes())['root_path'])

		# todo: this is something that has to be globally available
		self.allowed_vid = [
			'mp4',
			'mov',
			'webm',
			'ts',
			'mts',
			'mkv',
			'avi'
		]

		self.allowed_img = [
			'jpg',
			'jpeg',
			'jp2',
			'j2k',
			'png',
			'tif',
			'tiff',
			'tga',
			'webp',
			'psd',
			'apng',
			'gif',
			'avif',
			'bmp',
			'dib',
			'raw',
			'arw',
			'jfif',
			'jif',
			'hdr'
		]


	@property
	def accept_file(self):
		from pathlib import Path
		import json
		# this is literally 0.01% of what was promised...
		# FOR NOW !!!!!!!!!!!!
		# this is why it's a class and not a lonely function
		# for now there has to be an illusion of working shit
		# but THEN, a REAL deal would begin...
		dest = Path(self.prms['dest'])

		# important todo: this is a dirty auth
		# dirty because it doesn't check whether it's the subfolder of the match struct

		# no auth no shit
		if not self.server['auth_cl']:
			return json.dumps({'status': '1809246/anything'})

		# admin can upload wherever
		if not 'admin' in self.server['auth_cl']['admin']:
			# check league allowance
			if dest.parent.parent.parent.name in self.server['auth_cl']['folders'] or '%command' in self.server['auth_cl']['folders']:
				pass
			else:
				return json.dumps({'status': '1809246/root'})

			# now check whether allowed to upload to photos or moments
			if not dest.parent.name in self.server['auth_cl']['admin']:
				return json.dumps({'status': '1809246/struct'})

		(self.sysroot / str(dest)).write_bytes(self.bin)
		return json.dumps({'status': 'lizard', 'dst_name': dest.name})



	@property
	# init new LFS file in the temp dir
	def lfs_create(self):
		from pathlib import Path
		import json, sys, random
		sys.path.append('.')
		from util import eval_hash

		# only allow this if user actually has the rights to write to the final dir
		filedest = Path(self.prms['file_dest'])

		# important todo: this is a dirty auth
		# dirty because it doesn't check whether it's the subfolder of the match struct

		# no auth no shit
		if not self.server['auth_cl']:
			return json.dumps({'status': '1809246/anything'})

		# admin can upload wherever
		if not 'admin' in self.server['auth_cl']['admin']:
			# check league allowance
			if not filedest.parent.parent.parent.name in self.server['auth_cl']['folders']:
				return json.dumps({'status': '1809246/root'})

			# now check whether allowed to upload to photos or moments
			if not filedest.parent.name in self.server['auth_cl']['admin']:
				return json.dumps({'status': '1809246/struct'})

		# create random name
		seed = str(random.random()) + str(random.random()) + str(random.random())
		super_token = eval_hash(seed, 'sha256')

		# with open('pissoff.shit', 'r+b') as f:

		# init empty file
		tmp_loc_path = Path(self.server['cfg']['preview_db']) / 'temp_shite' / f"""{super_token}.{self.prms['flname']}"""
		tmp_loc_path.write_bytes(b'')

		# return target
		return json.dumps({'status': 'ok', 'target': str(tmp_loc_path)})


	# add to previously created lfs object
	@property
	def lfs_append(self):
		import json
		from pathlib import Path
		tmp_loc_path = Path(self.server['cfg']['preview_db']) / 'temp_shite' / self.prms['target']
		
		if not tmp_loc_path.is_file():
			return json.dumps({'status': 'error', 'reason': 'target does not exist...'})

		with open(str(tmp_loc_path), 'ab') as f:
			f.write(self.bin)

		return json.dumps({'status': 'ok'})


	# stop writing and move to target dir
	@property
	def lfs_collapse(self):
		import json, shutil
		from pathlib import Path

		target_dir = Path(self.prms['tgt_dir'])
		src_lfs = Path(self.prms['src_lfs'])
		tmp_loc_path = Path(self.server['cfg']['preview_db'])

		if (tmp_loc_path / 'temp_shite' / src_lfs).is_file():
			remove_token = src_lfs.name.split('.')
			del remove_token[0]
			shutil.move(str(tmp_loc_path / 'temp_shite' / src_lfs), str(self.sysroot / target_dir / '.'.join(remove_token)))
			return json.dumps({'status': 'ok'})
		else:
			return json.dumps({'status': 'erro', 'reason': 'source file does not exist'})