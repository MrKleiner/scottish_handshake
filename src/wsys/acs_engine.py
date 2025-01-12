import fnmatch
import sys
from pathlib import Path

if sys.argv[-1] == '-dbg':
	devprint = print
else:
	devprint = lambda *args, **kwargs: None


class AccessRule:
	def __init__(
		self,
		read=False,
		write=False,
		prohibit=False,
		pattern=None,
		inclusive=False,
		inclusive_rw=None,
		immediate_only=True,
	):
		self.read = read
		self.write = write
		self.prohibit = prohibit  # Flag for explicit prohibition
		self.pattern = pattern  # Pattern for matching folders/files with wildcards
		self.inclusive = inclusive
		self.inclusive_rw = inclusive_rw or (False, False)
		self.immediate_only = immediate_only

	def __repr__(self):
		return (
			'WaferACSRule()'
		)


def smart_add(self, rule):
	self.rules.append(rule)
	if rule.inclusive:
		rule_stack = rule.pattern.split('/')
		while rule_stack:
			if not rule_stack.pop():
				continue
			new_pattern = '/'.join(rule_stack)
			if not new_pattern.strip():
				break
			r, w = rule.inclusive_rw
			print(
				'Adding inclusive for group',
				getattr(self, 'group_name', self.username),
				new_pattern
			)
			self.rules.append(AccessRule(
				read=r,
				write=w,
				prohibit=rule.prohibit,
				pattern=new_pattern,
				inclusive=False,
				immediate_only=rule.immediate_only
			))


class AccessGroup:
	def __init__(self, group_name):
		self.group_name = group_name
		self.rules = []  # List of rules for this group

	def add_rule(self, rule):
		smart_add(self, rule)

	def get_rules(self):
		return self.rules

	def __repr__(self):
		return f"AccessGroup(group_name={self.group_name}, rules={self.rules})"


class WaferUser:
	def __init__(self, userid, username='', iddqd=False):
		# This user's unique ID
		self.userid = userid

		# Display name for this user
		self.username = username

		# List of AccessRule objects for this user
		self.rules = []

		# List of groups this user belongs to
		self.groups = []

		# Godmode
		self.iddqd = iddqd

	def add_rule(self, rule):
		smart_add(self, rule)

	def add_group(self, group):
		self.groups.append(group)

	def get_access_rules(self):
		# Collect all rules from groups and user's own rules
		combined_rules = self.rules.copy()
		for group in self.groups:
			for rule in group.get_rules():
				combined_rules.append(rule)
		return tuple(combined_rules)

	def __repr__(self):
		return (
			'<WaferUser>('
			f'{self.userid} | '
			f'{self.username} | '
			f'{self.iddqd} | '
			f'[{self.rules}]'
			')'
		)


class AccessSystem:
	def __init__(self):
		self.users = {}

	def add_user(self, user):
		self.users[user.username] = user

	def get_access(self, user, requested_path):
		# Step 1: Get the requested path by the user
		devprint(f'User {user.username} requested access to {requested_path}')

		if user.iddqd:
			return (True, True,)

		# Step 2: Get user's rules (including group rules)
		user_rules = user.get_access_rules()
		
		# Step 3: Validate the requested path against the user's rules
		access = self.validate_access(requested_path, user_rules)

		if access:
			base_r, base_w = (access.read, access.write,)
			incl_r, incl_w = access.inclusive_rw
			return (
				bool(incl_r + base_r),
				bool(incl_w + base_w)
			)
			"""
			if access.inclusive:
				return access.inclusive_rw
			else:
				# return access
				# return '!! KING !!'
				return (access.read, access.write,)
			"""
		else:
			devprint(f'Access denied for {user.username} on {requested_path}')
			return (False, False,)

	@staticmethod
	def is_immediate_child(requested_path, base_pattern):
		"""
		Checks if requested_path matches base_pattern and is an immediate child.
		:param requested_path: The path being checked (e.g., "/pootis/file.txt").
		:param base_pattern: The base pattern to match (e.g., "/pootis/*").
		:return: True if it's an immediate child, False otherwise.
		"""
		# Check if the requested_path matches the pattern
		if not fnmatch.fnmatch(requested_path, base_pattern):
			return False

		# Get the base directory from the pattern
		base_dir = base_pattern.rstrip('/*')
		base_depth = base_dir.count('/') + 1  # Depth of the base directory

		# Calculate the depth of the requested path
		requested_depth = requested_path.count('/')

		# Immediate children must have exactly one more level than the base
		return requested_depth == base_depth

	def validate_access(self, requested_path, user_rules):
		for rule in user_rules:
			# If the rule's pattern ends with '/*', check for immediate child
			if rule.pattern.endswith('/*') and rule.immediate_only:
				if self.is_immediate_child(requested_path, rule.pattern):
					devprint(f'Access granted for {requested_path} based on rule: {rule}')
					return rule
			# Otherwise, just check with fnmatch
			elif fnmatch.fnmatch(requested_path, rule.pattern):
				devprint(f'Access granted for {requested_path} based on rule: {rule}')
				return rule

		devprint(f'No matching rule found for {requested_path}')
		return False





def devsep():
	print('')
	print('')

def test_user(acs, usr, sample_path):
	print(f'{usr.username} > Wants > {sample_path}')
	r, w = acs.get_access(usr, sample_path)
	print(
		'Read:', r, '|', 'Write:', w
	)
	print('')

def test_tree(acs, usr, sample_path):
	stack = sample_path.split('/')
	while stack:
		new_path = '/'.join(stack)
		if not new_path.strip():
			break
		test_user(acs, usr, new_path)
		stack.pop()

def build_real_tree(real_dir, acs, usr, sample_path):
	stack = sample_path.strip('/').split('/')
	print('STACK:', stack)
	"""
	while stack:
		new_path = '/'.join(stack)
		if not new_path.strip():
			break
		test_user(acs, usr, new_path)
		stack.pop()
	"""
	real_dir = Path(real_dir)

	pstack = []

	sample_path = Path(sample_path)

	for chunk in stack:
		listing = []
		# if not chunk.strip():
		# 	continue

		target = real_dir / '/'.join(pstack)
		for entry in target.glob('*'):
			r, w = acs.get_access(
				usr,
				'/' + str(entry.relative_to(real_dir).as_posix())
			)
			if r or w:
				listing.append(entry.name)

		print(
			usr.username, 'Listing', target, listing
		)
		print()

		pstack.append(chunk)


def adv_test():
	"""
		+ ROOT
		|
		+---+ Basket
		    |
		    +---+ Season 1
		        |
		        +---+ Dnipro
		            |
		            +---+ photosession
		            |   |
		            |   +---+ photo
		            |   |   | ps_photo1.jpeg
		            |   |   | ps_photo2.jpeg
		            |   |
		            |   +---+ video
		            |       | ps_video1.ts
		            |       | ps_video2.ts
		            |
		            +---+ Mega Game 1
		            |   |
		            |   +---+ photo
		            |   |   | mg_photo1.jpeg
		            |   |   | mg_photo2.jpeg
		            |   |
		            |   +---+ video
		            |   |   | mg_video1.ts
		            |   |   | mg_video2.ts
		            |   |
		            |   +---+ other
		            |       | mg_rubbish1.exe
		            |       | mg_rubbish2.tar
	"""

	from pathlib import Path

	# Create access rules
	read_write_rule = AccessRule(read=True, write=True, pattern="/root/pootis/sandwich_*/dispenser/*")
	read_only_rule = AccessRule(read=True, write=False, pattern="/root/pootis/*/file.txt")
	prohibit_rule = AccessRule(prohibit=True, pattern="/root/prohibited/*")

	# Create users
	user1 = WaferUser("alice")
	user2 = WaferUser("bob")

	# Create access groups
	admin_group = AccessGroup("admin")
	user_group = AccessGroup("user")

	# Add rules to groups
	admin_group.add_rule(read_write_rule)  # Admin group has full access to sandwich dispensers
	user_group.add_rule(read_only_rule)  # User group has read-only access to specific files

	# Add groups to users
	user1.add_group(admin_group)  # Alice is in the admin group
	user2.add_group(user_group)   # Bob is in the user group

	# Add user-specific rules
	user1.add_rule(prohibit_rule)  # Alice is explicitly prohibited from accessing /root/prohibited/
	user2.add_rule(read_only_rule)  # Bob has read-only access to specific files

	# Create the access system and add users
	access_system = AccessSystem()
	access_system.add_user(user1)
	access_system.add_user(user2)

	# Check access for user1 (Alice)
	access_system.get_access(user1, "/root/pootis/sandwich_123/dispenser/file.txt")  # Should be granted based on admin group rule
	access_system.get_access(user1, "/root/pootis/sandwich_123/file.txt")  # Should be denied due to prohibition rule

	# Check access for user2 (Bob)
	access_system.get_access(user2, "/root/pootis/sandwich_123/dispenser/file.txt")  # Should be read-only based on user group rule
	access_system.get_access(user2, "/root/prohibited/secret.txt")  # Should be denied due to prohibition rule


	devsep()


	# ACS system
	wafer_acs = AccessSystem()



	# =============
	#    Dnipro
	# =============

	# Photo user
	photo_usr = WaferUser('dnipro_photo')
	# Photo RW
	photo_usr.add_rule(AccessRule(
		read=True,
		write=True,
		# /<SPORT TYPE>/<Any Season>/<Team>/<Any Folder>/photo
		pattern='/Basket/*/Dnipro/*/photo/*',
		inclusive=True,
		inclusive_rw=(True, False),
		# immediate_only=False,
	))

	# Video user
	video_usr = WaferUser('dnipro_video')
	# Video RW
	video_usr.add_rule(AccessRule(
		read=True,
		write=True,
		# /<SPORT TYPE>/<Any Season>/<Team>/<Any Folder>/photo
		pattern='/Basket/*/Dnipro/*/video/*',
		inclusive=True,
		inclusive_rw=(True, False),
		# immediate_only=False,
	))

	wafer_acs.add_user(photo_usr)
	wafer_acs.add_user(video_usr)


	SAMPLE_ROOT = Path('E:/!webdesign/wafer/src/dev/sample_struct')

	devsep()

	print('============== IMAGINARY ==============')

	devsep()


	test_tree(
		wafer_acs,
		photo_usr,
		'/Basket/Season 1/Dnipro/photosession/photo'
	)
	test_tree(
		wafer_acs,
		photo_usr,
		'/Basket/Season 1/Dnipro/photosession/video'
	)
	devsep()
	test_tree(
		wafer_acs,
		video_usr,
		'/Basket/Season 1/Dnipro/photosession/video'
	)
	test_tree(
		wafer_acs,
		video_usr,
		'/Basket/Season 1/Dnipro/photosession/photo'
	)




	devsep()

	print('============== REAL ==============')

	devsep()


	build_real_tree(
		SAMPLE_ROOT,
		wafer_acs,
		photo_usr,
		'/Basket/Season 1/Dnipro/photosession/photo/*'
	)
	devsep()
	build_real_tree(
		SAMPLE_ROOT,
		wafer_acs,
		photo_usr,
		'/Basket/Season 1/Dnipro/photosession/video/*'
	)
	devsep()
	build_real_tree(
		SAMPLE_ROOT,
		wafer_acs,
		video_usr,
		'/Basket/Season 1/Dnipro/photosession/video/*'
	)
	devsep()
	build_real_tree(
		SAMPLE_ROOT,
		wafer_acs,
		video_usr,
		'/Basket/Season 1/Dnipro/photosession/photo/*'
	)

	return

	devsep()
	print('============== HAX ==============')
	devsep()


	build_real_tree(
		SAMPLE_ROOT,
		wafer_acs,
		photo_usr,
		'/Basket/Season 1/Dnipro/photosession/photo/../'
	)
	devsep()
	build_real_tree(
		SAMPLE_ROOT,
		wafer_acs,
		photo_usr,
		'/Basket/Season 1/Dnipro/../photosession/video'
	)
	devsep()
	build_real_tree(
		SAMPLE_ROOT,
		wafer_acs,
		video_usr,
		'/Basket/Season 1/../../Dnipro/photosession/video'
	)
	devsep()
	build_real_tree(
		SAMPLE_ROOT,
		wafer_acs,
		video_usr,
		'/Basket/Season 1/Dnipro/../../photosession/photo'
	)


if __name__ == '__main__':
	adv_test()