




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



# generates an array of dicts according to predefined query
# simply lists every single file for now
# {
# 	'path': full abs paths,
# 	'name': aka city,
# 	'date': date
# }
def vdman_list_pool(prms=None, dt=None, sv=None):
	from pathlib import Path
	import json

	# IMPORTANT FUCKING TODO:
	# AS OF NOW IT'S POSSIBLE TO PASS ANY ABSOLUTE PATH TO THIS FUNCTION 
	# AND GET THE CONTENTS OF THE FOLDER

	paths = []

	scan_paths = json.loads(((sv['root']) / 'db' / 'catalogue' / 'video_index.pootis').read_bytes())

	# scan the folder it points to, if it exists
	for fl in Path(prms['fld_path']).glob('*.mp4'):
		paths.append({
			'name': fl.name,
			'date': 'date',
			'path': str(fl)
		})

	return json.dumps(paths)




# tgtheight = 0
# lel = 0
# calc_v_seconds = 0

# ffmpeg -i in.mp4 -vf select='eq(n\,100)+eq(n\,184)+eq(n\,213)' -vsync 0 frames%d.jpg

# takes filepath as an input
# returns path to generated image

def previewgen_old(cfg):
	vname = file
	# todo: make sure file exists before doing anything
	# todo: return some sort of a fail code to indicate the problem in the gui
	vidcap = cv2.VideoCapture(vname)
	success,image = vidcap.read()
	count = 0
	length = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
	vfps = float(vidcap.get(cv2.CAP_PROP_FPS))

	global lel, tgtheight, calc_v_seconds

	calc_v_seconds = length / vfps
	# print('fps: ', vfps)
	# print('seconds_length: ', calc_v_seconds)
	

	# frames to extract

	if calc_v_seconds < 720:
		lel = 45
	if calc_v_seconds > 720:
		lel = 55
	if calc_v_seconds > 2230:
		lel = 100
	if calc_v_seconds < 120:
		lel = 20

	# print('preview frame count: ', lel)

	# print('step rough: ', (length / lel))
	step = math.floor(length / lel)

	frames = []

	stepped = 0

	for fr in range(lel):
		stepped = stepped + step
		frames.append(stepped)

	# print('total length: ' + str(length))
	# print('step: ', step)
	# print('future frames: ', frames)

	aligner = []

	# todo: align everything to 320 ??
	# So that you wont get an unnecesarily big preview from a 4k video?
	maxwidth = 320

	scale_percent = 25 # percent of original size
	width = int(image.shape[1] * scale_percent / 100)
	height = int(image.shape[0] * scale_percent / 100)

	if width <= maxwidth:
		backfac = maxwidth / width
		width = int(width * backfac)
		height = int(height * backfac)

	if image.shape[1] <= maxwidth:
		width = image.shape[1]
		height = image.shape[0]


	dim = (width, height)
	tgtheight = height

	for fnum, calc_fr in enumerate(frames):

		# mk_fname = os.path.join(vname.replace('.', '') + '_' + str(calc_fr) + '.png')
		# todo: better way of "replacing the dot"

		# replacedot = vname.split('\\')
		# replacedot[-1] = replacedot[-1].replace('.', '')
		mk_fname = eval_m5(vname) + '_' + str(calc_fr) + '.png'

		# save frame as JPEG file
		resized = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
		# cv2.imwrite(vname.replace('.', '') + '_' + str(calc_fr) + '.jpg', resized, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
		cv2.imwrite(mk_fname, resized, [int(cv2.IMWRITE_JPEG_QUALITY), 100])

		f.write('\n FUCK')
		# f.write(atob(vname))
		f.write(mk_fname)
		aligner.append(mk_fname)
		success,image = vidcap.read()
		# print('Read a new frame: ', success)
		vidcap.set(1, int(calc_fr))
		print('frame', fnum, 'of total', len(frames))


	# print( length )
	f.write(str(aligner))
	imgs = [ PIL.Image.open(i) for i in aligner ]
	imgs_comb = np.vstack([np.asarray(i) for i in imgs])
	imgs_comb = PIL.Image.fromarray(imgs_comb)
	imgs_comb.save( vname.replace('.', '_') + '.jpg', quality=30, optimize=True, progressive=True )


	for file in aligner:
		os.remove(file)
	
	# return str(vname)
	getparent = Path(vname).parent
	getname = Path(vname.replace('.', '_') + '.jpg').name

	return str(getparent) + '\\' + str(getname)






# cfg = {
# 	'file': path to a file,
# 	'scale': reduce video quality by a given percentage, like 0.20 = 20% of original resolution,
# 	'frames': amount of frames to extract,
#	'ffmpeg': path to ffmpeg. None = use system ffmpeg
# }

# ffprobe.exe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -print_format json "C:\custom\vid_db\pin\glasgow.23_11_2022.23-45.mp4"

# returns bytes of the generated image
# in a gigabin format
def vdman_gen_vid_preview(vpath=None):
	from pathlib import Path
	# don't bother if the path does not exist
	if not Path(vpath).is_file():
		return None









