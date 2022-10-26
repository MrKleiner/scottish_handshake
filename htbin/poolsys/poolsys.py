from dataclasses import dataclass, field


# @dataclass(frozen=True, order=True)
class poolsys:
	# parameters passed as through URL params
	# prms: dict = field(default_factory=dict)
	# data passed through the request
	# data: str | bytes = b''
	# server info, stuff like server root
	# server: dict = field(default_factory=dict)
	def __init__(self, prms={}, dt='', sv={}):
		import json
		from pathlib import Path

		self.prms = prms
		self.data = dt
		self.server = sv
		self.sysroot = Path(json.loads((sv['root'] / 'db' / 'root.json').read_bytes())['root_path'])

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
	def list_leagues(self):
		import json
		from pathlib import Path

		return json.dumps([fld.name for fld in self.sysroot.glob('*') if fld.is_dir()])


	@property
	def list_matches_w_subroot(self):
		import json
		from pathlib import Path
		try:
			mws = {}

			for cmd in self.sysroot.glob('*'):
				if not cmd.is_dir():
					continue

				mws[cmd.name] = [match.name for match in cmd.glob('*') if match.is_dir()]

			return json.dumps(mws)
		except Exception as e:
			return json.dumps({})


	@property
	def list_league_matches(self):
		import json
		from pathlib import Path

		if not self.prms['league_name']:
			return []

		return json.dumps([fld.name for fld in (self.sysroot / Path(self.prms['league_name'])).glob('*') if fld.is_dir()])


	@property
	def list_match_struct(self):
		import json
		from pathlib import Path

		return json.dumps([fld.name for fld in (self.sysroot / Path(self.prms['match_name'])).glob('*') if fld.is_dir()])


	@property
	def list_media(self):
		import json, os
		from pathlib import Path

		matches = []

		for match in (self.sysroot / Path(self.prms['target'])).glob('*'):
			if match.is_dir():
				continue

			if match.suffix.strip('.').lower() in self.allowed_vid:
				matches.append({
					'lfs': (True if os.stat(str(match)).st_size >= ((1024**2)*3) else False),
					'stats': f"""{((1024**2)*3)}/{os.stat(str(match)).st_size}""",
					'etype': 'vid',
					'path': str(match),
					'flname': match.name
				})
				continue
			if match.suffix.strip('.').lower() in self.allowed_img:
				matches.append({
					'lfs': (True if os.stat(str(match)).st_size >= ((1024**2)*20) else False),
					'stats': f"""{((1024**2)*20)}/{os.stat(str(match)).st_size}""",
					'etype': 'img',
					'path': str(match),
					'flname': match.name
				})
				continue

			matches.append({
				'lfs': (True if os.stat(str(match)).st_size >= ((1024**2)*3) else False),
				'stats': f"""{((1024**2)*3)}/{os.stat(str(match)).st_size}""",
				'etype': 'file',
				'path': str(match),
				'flname': match.name
			})
		
		return json.dumps(matches)


	@property
	def list_files(self):
		return []

	@property
	def load_media_preview(self):
		import json
		from pathlib import Path
		import subprocess as sp

		tgt_path = Path(self.prms['media_path'])

		if tgt_path.suffix.strip('.').lower() in self.allowed_vid:
			# return self.generate_vid_preview
			return 'videofile'

		if not tgt_path.suffix.strip('.').lower() in self.allowed_img:
			return 'regular file'.encode()

		# if this file exists in the previews pool - get it and return immediately
		preview_path = (tgt_path.parent / 'prdb_lzpreviews' / f'{tgt_path.name}.lzpreview.webp')
		if preview_path.is_file():
			return preview_path.read_bytes()

		# create dir if doesn't exist
		(tgt_path.parent / 'prdb_lzpreviews').mkdir(exist_ok=True)

		ffmpeg_prms = [
			# mpeg
			'/usr/bin/ffmpeg',
			# input
			# '-i', str(engines / pl['img']),
			'-i', str(tgt_path),
			# resize
			# '-hwaccel', 'cuda',
			# '-hwaccel_output_format', 'cuda',
			# '--enable-nvenc',
			# '--enable-ffnvcodec',
			# '-h', 'encoder=h264_nvenc',
			# does nothing
			# (it works, but it's only for videos)
			# '-vcodec', 'h264_nvenc',
			# change size
			# this will upscale sometimes
			# '-vf', 'scale=500:-1',
			# while this is smart
			# this is quite a hires preview
			# '-vf', 'scale=w=min(iw\\,500):h=-2',
			# this one is smaller
			'-vf', 'scale=w=min(iw\\,400):h=-2',
			# format
			'-c:v', 'webp',
			# ffmpeg encoding type
			'-f', 'image2pipe',
			# lossless
			# quite a heavy load
			# '-lossless', '1',
			# make it take even less space
			'-lossless', '0',
			# lossless compression
			# (now is lossy)
			'-compression_level', '6',
			'-qscale', '50',
			# output to stdout
			'pipe:'
			# 'fuckoff.webp'
			# str(tgt_path.parent / 'prdb_lzpreviews' / f'{tgt_path.name}.lzpreview.webp')
		]


		# webp = subprocess.run(ffmpeg_prms, capture_output=True)
		webp = None
		with sp.Popen(ffmpeg_prms, stdout=sp.PIPE, bufsize=10**8) as img_pipe:
			# myFile.write(img_pipe.stdout.read())
			webp = img_pipe.stdout.read()

		# Save preview
		preview_path.write_bytes(webp)

		# return str(self.prms['media_path']).encode()
		return webp
		# return (tgt_path.parent / 'prdb_lzpreviews' / f'{tgt_path.name}.lzpreview.webp').read_bytes()
		# return tgt_path.read_bytes()


	@property
	def load_fullres_pic(self):
		from pathlib import Path
		import os
		if os.stat(self.prms['target']).st_size > ((1024**2)*100):
			return 'file is too big'.encode()

		return Path(self.prms['target']).read_bytes()
	

	# obvious todo: hardcoded 100 frames = bad
	@property
	def generate_vid_preview(self):
		import sys, json
		import subprocess as sp
		from pathlib import Path
		sys.path.append('.')
		from gigabin_py import gigabin
		from util import eval_hash, even_points
		return

		prdb = Path(self.server['cfg']['preview_db'])

		tgt_vid = Path(self.prms['media_path'])
		# todo: also evaluate file checksum ?
		preview_name = eval_hash(str(tgt_vid), 'sha256')

		# ---------------------------
		# extract all frames
		# ---------------------------


		#
		# first, get resolution of the video
		#

		# ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 input.mp4
		ffprobe_prms = [
			'/usr/bin/ffprobe',
			'-v', 'error',
			'-select_streams', 'v:0',
			'-show_entries', 'stream=width,height',
			'-of', 'csv=s=x:p=0',
			str(tgt_vid)
		]
		vid_res = None
		with sp.Popen(ffprobe_prms, stdout=sp.PIPE, bufsize=10**8) as img_pipe:
			pipe_data = img_pipe.stdout.read().decode().split('x')
			vid_res = (int(pipe_data[0]), int(pipe_data[1]))


		#
		# then, get frame count
		#

		# todo: previous example has some cool selection (no need for json shit)
		# important todo: combine this wit the previous command
		# ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -print_format csv
		ffprobe_prms = [
			'/usr/bin/ffprobe',
			'-v', 'error',
			'-select_streams', 'v:0',
			'-count_frames',
			'-show_entries',
			'stream=nb_read_frames',
			'-print_format', 'json',
			str(tgt_vid)
		]
		vid_fr_count = None
		with sp.Popen(ffprobe_prms, stdout=sp.PIPE, bufsize=10**8) as img_pipe:
			vid_fr_count = int(json.loads(img_pipe.stdout.read())['streams'][0]['nb_read_frames'])



		#
		# now, construct ffmpeg params for frames extraction
		#

		# ffmpeg -i in.mp4 -vf select='eq(n\,100)+eq(n\,184)+eq(n\,213)' -vsync 0 frames%d.jpg
		ffmpeg_prms = [
			# executable
			'/usr/bin/ffmpeg',
			# input
			'-i', str(tgt_vid),

			# filters
			# '-vf', ("""select='""" + '+'.join([f'eq(n\\,{int(frnum)})' for frnum in even_points(1,vid_fr_count,3)]) + """'"""),
			'-vf', """select='eq(n\\,100)+eq(n\\,184)+eq(n\\,213)'""",

			# compression
			'-c:v', 'webp',

			'-lossless', '0',
			'-compression_level', '6',
			'-qscale', '50',
			# output
			str(prdb / 'temp_shite' / f'{preview_name}%d.webp')
		]
		# extract frames to a temp location on raid
		# todo: the output doesn't really has to be captured
		# echo_sh = None
		# with sp.Popen(ffmpeg_prms, stdout=sp.PIPE, bufsize=10**8) as img_pipe:
		# 	echo_sh = img_pipe.stdout.read()

		sp.run(ffmpeg_prms)

		# return 'fuckoff'.encode()

		#
		# collapse frames and info into a gigabin
		#
		chad = gigabin((prdb / 'temp_shite' / f'{preview_name}.chad'), True)

		# add previews one by one
		for giga in range(3):
			giga_name = (prdb / 'temp_shite' / f'{preview_name}{giga+1}.webp')
			chad.add_solid(
				f'frn{giga+1}',
				giga_name.read_bytes(),
				False
			)
			# delete file afterwards
			# giga_name.unlink(missing_ok=True)


		index_json = {
			'dimensions': vid_res,
			'lizards': 'sexy',
			'debug': str(prdb / 'temp_shite' / f'{preview_name}{1}.webp')
		}

		# write info
		chad.add_solid(
			'index',
			json.dumps(index_json).encode(),
			True
		)


		# finally, return gigabin with all the previews
		return (prdb / 'temp_shite' / f'{preview_name}.chad').read_bytes()
	

	@property
	def load_lfs(self):
		rt = b''
		rt += f"""Content-Disposition: attachment; filename="{self.prms['lfs_name']}"\r\n""".encode()
		rt += f"""X-Sendfile: {self.prms['lfs']}\r\n\r\n""".encode()
		return rt