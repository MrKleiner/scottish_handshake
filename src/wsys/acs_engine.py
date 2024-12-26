from collections import defaultdict

class AccessRule:
	def __init__(self, name, read=False, write=False, recursive=False):
		self.name = name
		self.read = read
		self.write = write
		self.recursive = recursive

class AccessGroup:
	def __init__(self, name):
		self.name = name
		self.rules = []

	def add_rule(self, rule):
		self.rules.append(rule)

	def remove_rule(self, rule):
		self.rules.remove(rule)

class User:
	def __init__(self, username):
		self.username = username
		self.rules = []
		self.groups = []

	def add_rule(self, rule):
		self.rules.append(rule)

	def add_group(self, group):
		self.groups.append(group)

	def remove_rule(self, rule):
		self.rules.remove(rule)

	def remove_group(self, group):
		self.groups.remove(group)

def check_access(user, path, operation, rules_store, global_rules):
	"""
	Check if a user has access to a given path for a specific operation.
	:param user: User object
	:param path: Path to the folder/file
	:param operation: 'read' or 'write'
	:param rules_store: Dictionary containing specific rules for paths per user
	:param global_rules: Dictionary containing global rules for paths
	:return: True if access is allowed, False otherwise
	"""
	user_specific_rules = rules_store[user.username] if user.username in rules_store else {}
	
	# Check user-specific rules
	if path in user_specific_rules:
		if operation == 'read' and user_specific_rules[path].read:
			return True
		elif operation == 'write' and user_specific_rules[path].write:
			return True
	
	# Check rules from groups the user belongs to
	for group in user.groups:
		for rule in group.rules:
			if rule.recursive and path.startswith(rule.name):
				if operation == 'read' and rule.read:
					return True
				elif operation == 'write' and rule.write:
					return True
	
	# Check global rules
	if path in global_rules:
		if operation == 'read' and global_rules[path].read:
			return True
		elif operation == 'write' and global_rules[path].write:
			return True
	
	return False

# Example setup
global_rules = {
	'/public': AccessRule(name='/public', read=True, write=False, recursive=True)
}

rules_store = defaultdict(dict)  # Stores rules per user and path

# Creating users, rules, and groups
user1 = User('alice')
user2 = User('bob')

read_rule = AccessRule(name='/docs', read=True, recursive=True)
write_rule = AccessRule(name='/docs', write=True, recursive=False)

group1 = AccessGroup(name='Editors')
group1.add_rule(read_rule)
group1.add_rule(write_rule)

user1.add_group(group1)

# Adding specific rules to users
rules_store['bob']['/docs'] = AccessRule(name='/docs', read=True, write=False, recursive=False)

# Access checks
print(check_access(user1, '/docs/file1.txt', 'read', rules_store, global_rules))  # True
print(check_access(user2, '/docs/file1.txt', 'write', rules_store, global_rules))  # False