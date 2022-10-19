
# RAM-Efficient
# applicable entries are: md5/sha256/sha512
def hash_file(filepath=None, meth='md5', mb_read=100):
	import hashlib
	from pathlib import Path

	if filepath == None or not Path(filepath).is_file():
		return False

	file = str(filepath) # Location of the file (can be set a different way)

	# The size of each read from the file
	# default: 65535
	BLOCK_SIZE = (1024**2)*mb_read
	
	# Create the hash object, can use something other than `.sha256()` if you wish
	file_hash = hashlib.md5()
	if meth == 'sha256':
		file_hash = hashlib.sha256()
	if meth == 'sha512':
		file_hash = hashlib.sha512()

	with open(file, 'rb') as f: # Open the file to read it's bytes
		fb = f.read(BLOCK_SIZE) # Read from the file. Take in the amount declared above
		while len(fb) > 0: # While there is still data being read from the file
			file_hash.update(fb) # Update the hash
			fb = f.read(BLOCK_SIZE) # Read the next block from the file

	return(file_hash.hexdigest()) # Get the hexadecimal digest of the hash



# fast
# takes bytes or strings as an input
# hash 
# h: md5/sha256/sha512
def eval_hash(st, h='md5'):
	import hashlib

	if isinstance(st, bytes):
		hasher = st
	else:
		text = str(st)
		hasher = text.encode()

	hash_obj = hashlib.md5(hasher)
	if h == 'sha256':
		hash_obj = hashlib.sha256(hasher)
	if h == 'sha512':
		hash_obj = hashlib.sha512(hasher)

	return hash_obj.hexdigest()



# get evenly distributed points from a range
def even_points(low,up,leng):
	list = []
	step = (up - low) / float(leng)
	for i in range(leng):
		list.append(low)
		low = low + step
	return list