



class gigabin:

	def __init__(self, src=None, force=None):
		from pathlib import Path
		import json, base64
		self.giga_identifier = 'gigachad'

		self.header = None
		self.bin = None

		self.head_len = 7+32

		# if a path was passed - read it
		if Path(src).is_file():
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
				chad.write('gigabin'.encode())
				chad.write(('!'*32).encode())


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


		#
		# array
		#
		if fl_info['type'] == 'array':
			with open(str(self.bin), 'rb') as chad:
				for ch in fl_info['bits']:
					chad.seek(ch[0])
					chunk = chad.read(ch[1])
					if read_as == 'buffer':
						yield chunk

					if read_as == 'text':
						yield chunk.decode()

					if read_as == 'json':
						import json
						yield json.loads(chunk)



	def mkheader():
		import base64
		import json
		return base64.b64encode(jsin.dumps(self.header).encode())



	# takes bit info array as an input
	# only makes sense for one-time reads
	def read_bit(self, bit=None, btype='buffer'):
		with open(str(self.bin), 'rb') as chad:
			if not bit:
				return None

			# read bytes
			chad.seek(bit[0], 0)
			chunk = chad.read(bit[1])

			if read_as == 'buffer':
				return chunk

			if read_as == 'text':
				return chunk.decode()

			if read_as == 'json':
				import json
				return json.loads(chunk)

			return chunk


	# takes an array of names to delete
	def delete_file(names=[]):
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

		# re-append everything except specified
		with open(str(self.bin), 'rb') as original:
			with open(str(newfile), 'ab') as chad:
				# write identifier + preserve header space
				chad.write(self.giga_identifier)
				# reserve header size space
				chad.write('!'*32)

				# Always account for header length
				for chunk in head:
					if chunk in names:
						del self.header['stores'][chunk]
						continue

					if head[chunk]['type'] == 'array':
						# re-write bits one by one
						for bit_idx, bit in enumerate(chunk['bits'])
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
								(chad.tell()-self.head_len),
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
							(chad.tell() - self.head_len),
							# data length
							write_data_length,
							# hash
							None
						)

				# add header
				newheader = self.mkheader()
				chad.write()



		# delete original file and rename the new one
		self.bin.unlink(missing_ok=True)
		os.rename(str(newfile), str(self.bin))


	# info should cointain:
	# name: filename
	# data: data to store / pass an empty array to init a new array
	# overwrite: true/false

	# important todo: make this class compatible with
	# with open() shit
	# so that it's possible to open the file and avoid many rewrites
	# utill the work is done
	def add_file(info=None):
		from pathlib import Path
		import os, json
		if not info:
			raise Exception('gigabin: Invalid file payload')

		store = this.header['stores'];

		# don't do shit if file exists, but overwrite is set to false
		if store.get(info['name']) and info.get('overwrite') != True:
			# console.warn('gigabin: File exists in the file pool, but overwrite is set to false');
			return None


		# first - delete existing name, if any
		self.delete_file([info['name']])

		# if empty array was passed - init a new array
		if info['data'] == []:
			self.header['stores'][info['name']] = {
				'type': 'array',
				'bits': []
			}
			return True

		# else - write given chunk
		# todo: makes this accept file paths and be stepped
		file_header = len(self.mkheader())
		# first - erase header
		with open(str(self.bin), 'r+b') as chad:
			chad.seek(file_header*(-1), os.SEEK_END)
			chad.truncate()

			# Then, move to the end
			chad.seek(0, os.SEEK_END)
			current_offs = chad.tell()
			# now append data to the end of the file
			chad.write(info['data'])
			# update header
			self.header['stores'][info['name']] = {
				'type': 'solid',
				# tuples? why use tuples? They're never directly accessed later...
				'bits': ((current_offs - self.head_len), len(info['data']), None)
			}
			# compile header
			newhead = self.mkheader()

			# update header length
			chad.seek(8, 0)
			# flush header length
			chad.write('!'*32)
			# write new header length
			chad.seek(8, 0)
			chad.write(len(newhead))
			# append header to the end of the file
			chad.seek(0, os.SEEK_END)
			chad.write(newhead)









def mdma():
	thedir = Path(__file__).parent
	kurwa = gigabin(None, (thefile / 'gigasex.chad'))


mdma()
