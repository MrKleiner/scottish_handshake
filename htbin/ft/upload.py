







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
			if not dest.parent.parent.parent.name in self.server['auth_cl']['folders']:
				return json.dumps({'status': '1809246/root'})

			# now check whether allowed to upload to photos or moments
			if not dest.parent.name in self.server['auth_cl']['admin']:
				return json.dumps({'status': '1809246/struct'})

		(self.sysroot / str(dest)).write_bytes(self.bin)
		return json.dumps({'status': 'lizard', 'dst_name': dest.name})















