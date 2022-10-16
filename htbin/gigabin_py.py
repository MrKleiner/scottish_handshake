



class gigabin:

	def __init__(self, src=None, force=None):
		from pathlib import Path
		import json, base64
		self.giga_identifier = 'gigachad'

		self.header = None
		self.bin = None

		self.head_len = len(self.giga_identifier) + 32

		# if a path was passed - read it
		if Path(str(src)).is_file():
			# raise Exception('Given data structure does not represent a valid gigabin format')
			# with open(str(src_bin), 'rb') as bootleg:
			# 	bootleg.seek(8192 + bin_info['7z_exe']['offset'], 0)
			# 	bootleg.read()
			
			# open file and validate that it's gigachad
			with open(str(src), 'rb') as chad:
				# first 7 bytes store the identifier
				if src.read(7).decode() != self.giga_identifier:
					raise Exception('Given data structure does not represent a valid gigabin format')

				#
				# Get header
				#
				chad.seek(7)
				head_size = int(chad.read(32).decode().replace('!', ''))
				all_size = chad.seek(0, os.SEEK_END)
				all_size = all_size.tell()
				# read header bytes
				chad.seek(all_size - head_size, 0)
				self.header = json.loads(base64.b64decode(chad.read(head_size)))
				self.bin = Path(src)
		else:
			self.header = {
				'stores': {},
				'version': '0.17',
				'total_size': None,
				'comment': ''
			}
			self.bin = Path(force)

			# init new file
			with open(str(self.bin), 'ab') as chad:
				chad.write(b'')
				chad.write(self.giga_identifier.encode())
				chad.write(('!'*32).encode())
				chad.write(self.mkheader())

		self.files = self.header['stores']


	# acts as a generator when chunk type is array
	def read_file(self, name=None, read_as='bytes'):
		fl_info = self.header['stores'][name]
		if not name or not fl_info:
			return None


		#
		# monoblock
		#
		if fl_info['type'] == 'solid':
			chunk_info = self.header['stores'][name]['bits']
			return self.read_bit(chunk_info, read_as)



	# acts as a generator when chunk type is array
	def read_file_arr(self, name=None, read_as='bytes'):
		fl_info = self.header['stores'][name]
		if not name or not fl_info:
			return None

		#
		# array
		#
		if fl_info['type'] == 'array':
			with open(str(self.bin), 'rb') as chad:
				for ch in fl_info['bits']:
					chad.seek(ch[0] + self.head_len, 0)
					chunk = chad.read(ch[1])
					if read_as == 'buffer':
						yield chunk

					if read_as == 'text':
						yield chunk.decode()

					if read_as == 'json':
						import json
						yield json.loads(chunk)



	def mkheader(self):
		import base64
		import json
		return base64.b64encode(json.dumps(self.header).encode())



	# takes bit info array as an input
	# only makes sense for one-time reads
	def read_bit(self, bit=None, btype='buffer'):
		with open(str(self.bin), 'rb') as chad:
			if not bit:
				return None

			# read bytes
			chad.seek(bit[0] + self.head_len, 0)
			chunk = chad.read(bit[1])

			if btype == 'buffer':
				return chunk

			if btype == 'text':
				return chunk.decode()

			if btype == 'json':
				import json
				return json.loads(chunk)

			return chunk


	# takes an array of names to delete
	def delete_file(self, names=[]):
		import os
		if len(names) <= 0:
			return None

		# del self.header['stores'][name]

		head = self.header['stores']

		# don't write shit if no mathces were found
		# todo: do smart dict collision test
		matched = False
		for nm in names:
			if nm in head:
				matched = True
				break
		if matched == False:
			return None

		newfile = self.bin.with_name(f'{self.bin.name}.rw')

		newheader = None

		# Delete items from the dict
		for del_i in names:
			del self.header['stores'][del_i]

		# re-append everything except specified
		with open(str(self.bin), 'rb') as original:
			with open(str(newfile), 'wb') as chad:
				# write identifier + preserve header space
				chad.write(self.giga_identifier.encode())
				# reserve header size space
				chad.write(('!'*32).encode())

				# Always account for header length
				for chunk in head:
					# if chunk in names:
					# 	continue

					if head[chunk]['type'] == 'array':
						# re-write bits one by one
						for bit_idx, bit in enumerate(chunk['bits']):
							# set cursor to the begnning of the data in the src file
							original.seek(self.head_len + bit[0], 0)
							# write this piece to the new file
							write_data = original.read(bit[1])
							write_data_length = len(write_data)
							chad.write(write_data)
							# get current offset
							chad.seek(0, os.SEEK_END)
							# update header
							self.header['stores'][chunk]['bits'][bit_idx] = (
								# offset
								(chad.tell() - self.head_len - write_data_length),
								# data length
								write_data_length,
								# hash
								None
							)

					if head[chunk]['type'] == 'solid':
						bit = head[chunk]['bits']
						# set cursor to the begnning of the data in the src file
						original.seek(self.head_len + bit[0], 0)
						# write this piece to the new file
						write_data = original.read(bit[1])
						write_data_length = len(write_data)
						chad.write(write_data)
						# get current offset
						chad.seek(0, os.SEEK_END)
						# update header
						self.header['stores'][chunk]['bits'] = (
							# offset
							# IMPORTANT: minus write data length, because as of moment
							# of reading the data shift
							# the file already has the payload appended
							# problem: I fucking hate inclusive/not inclusive
							# in this case it's.... WHATEVER
							# seems like we have to subtract 1........
							# important todo: ^^^^^^
							(chad.tell() - self.head_len - write_data_length),
							# data length
							write_data_length,
							# hash
							None
						)

				# add header
				newheader = self.mkheader()
				chad.write(newheader)

				# write header length
				chad.seek(8, 0)
				chad.write(str(len(newheader)).encode())



		# delete original file and rename the new one
		self.bin.unlink(missing_ok=True)
		os.rename(str(newfile), str(self.bin))


	# info should cointain:
	# name: filename
	# data: data to store / pass an empty array to init a new array
	# overwrite: true/false/append
	# append = append data to Array type

	# important todo: make this class compatible with
	# with open() shit
	# so that it's possible to open the file and avoid many rewrites
	# utill the work is done
	def add_file(self, info=None):
		from pathlib import Path
		import os, json
		if not info:
			raise Exception('gigabin: Invalid file payload')

		store = self.header['stores'];

		# don't do shit if file exists, but overwrite is set to false
		if store.get(info['name']) and (info.get('overwrite') != True and info.get('overwrite') != 'append'):
			# console.warn('gigabin: File exists in the file pool, but overwrite is set to false');
			# print('cant add shit')
			return None


		# first - delete existing name, if any
		if not info.get('overwrite') == 'append':
			print('deleting...', [info['name']])
			self.delete_file([info['name']])

		# if empty array was passed - init a new array
		if info['data'] == []:
			# print('init new array with the name', info['name'])
			self.header['stores'][info['name']] = {
				'type': 'array',
				'bits': []
			}
			# print(self.header)
			return True

		# else - write given chunk
		# todo: makes this accept file paths and be stepped
		file_header = len(self.mkheader())
		# first - erase header
		with open(str(self.bin), 'r+b') as chad:
			# print('invalid arg', (file_header*(-1)))
			chad.seek((file_header*(-1)), os.SEEK_END)

			# chad.seek(-1, os.SEEK_END)
			chad.truncate()

			# Then, move to the end
			chad.seek(0, os.SEEK_END)
			current_offs = chad.tell()
			# now append data to the end of the file
			chad.write(info['data'])

			# update header
			if info.get('overwrite') == 'append':
				# print('I swear it exists', self.header['stores'])
				self.header['stores'][info['name']]['bits'].append((
					(current_offs - self.head_len),
					len(info['data']),
					None
				))
			else:
				self.header['stores'][info['name']] = {
					'type': 'solid',
					# tuples? why use tuples? They're never directly accessed later...
					'bits': ((current_offs - self.head_len), len(info['data']), None)
				}
			# compile header
			newhead = self.mkheader()

			# update header length
			chad.seek(len(self.giga_identifier), 0)
			# flush header length
			chad.write(('!'*32).encode())
			# write new header length
			chad.seek(len(self.giga_identifier), 0)
			chad.write(str(len(newhead)).encode())
			# append header to the end of the file
			chad.seek(0, os.SEEK_END)
			chad.write(newhead)


	# add solid type
	def add_solid(self, info=None):






def mdma():
	from pathlib import Path
	thedir = Path(__file__).parent
	(thedir / 'gigasex.chad').unlink(missing_ok=True)
	kurwa = gigabin(None, (thedir / 'gigasex.chad'))

	kurwa.add_file({
		'name': 'lizard',
		'data': '0_1_2_3_4_5_6_7_8_9'.encode(),
		'overwrite': True
	})
	kurwa.add_file({
		'name': 'sex',
		'data': 'POOTIS'.encode(),
		'overwrite': True
	})

	print(kurwa.read_file('lizard', 'text'))

	kurwa.delete_file(['sex'])

	sex = [
		r"C:\custom\vid_db\pin\glasgow.23_11_2022.23-45.mp4",
		r"C:\custom\vid_db\pin\bristol.17_09_2022.13-25.mp4",
		r"C:\custom\vid_db\pin\bigcity.19_03_2021.19-00.mp4"
	]

	print(kurwa.read_file('lizard', 'text'))

	for sid, nen in enumerate(sex):
		kurwa.add_file({
			'name': f'dicks{str(sid)}',
			'data': Path(nen).read_bytes(),
			'overwrite': False
		})

	for sid, nen in enumerate(sex):
		(thedir / f'balls{sid}.mp4').write_bytes(kurwa.read_file(f'dicks{str(sid)}', 'buffer'))

mdma()
