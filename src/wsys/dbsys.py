import json
import sqlite3
from pathlib import Path

try:
	from waferdev import (
		DEVDIR,
		devtitle,
		devsep,
		dict_prety_print,
	)
except ImportError as e:
	pass



class BasicDBConnection:
	"""
		Some basic shit for managing SQLite database connections.
	"""
	def __init__(self, dbpath):
		self.dbpath = dbpath

		self._connection = None
		self._cursor_obj = None
		self._exec = None
		self._exec_many = None
		self._exec_script = None
		self._commit = None
		self._close = None

		self._fetchone = None
		self._fetchall = None

	@property
	def connection(self):
		if self._connection:
			return self._connection

		self._connection = sqlite3.connect(str(self.dbpath))
		return self._connection

	@property
	def cursor_obj(self):
		if self._cursor_obj:
			return self._cursor_obj

		self._cursor_obj = self.connection.cursor()
		return self._cursor_obj

	@property
	def exec(self):
		if self._exec:
			return self._exec

		self._exec = self.cursor_obj.execute
		return self._exec

	@property
	def exec_many(self):
		if self._exec_many:
			return self._exec_many

		self._exec_many = self.cursor_obj.executemany
		return self._exec_many

	@property
	def exec_script(self):
		if self._exec_script:
			return self._exec_script

		self._exec_script = self.cursor_obj.executescript
		return self._exec_script

	@property
	def commit(self):
		if self._commit:
			return self._commit

		if not self._connection:
			return (lambda: None)

		self._commit = self.connection.commit
		return self._commit

	@property
	def close(self):
		if self._close:
			return self._close

		if not self._connection:
			return (lambda: None)

		self._close = self.connection.close
		return self._close

	@property
	def fetchone(self):
		if self._fetchone:
			return self._fetchone

		self._fetchone = self.cursor_obj.fetchone
		return self._fetchone

	@property
	def fetchall(self):
		if self._fetchall:
			return self._fetchall

		self._fetchall = self.cursor_obj.fetchall
		return self._fetchall


	def __enter__(self):
		return self

	def __exit__(self, type, value, traceback):
		self.connection.commit()
		self.close()


class BasicKVStorageTableInstance:
	# todo: This is unacceptable...
	# or is it?
	KEYTYPE_MAP_TODB = {
		# bool:   0,
		# str:    1,
		# int:    2,
		# float:  3,

		# list:   4,
		# dict:   4,
		# tuple:  4,


		bool: (
			0,
			lambda val: str(int(val)),
		),
		str: (
			1,
			lambda val: val,
		),
		int: (
			2,
			lambda val: str(val),
		),
		float: (
			3,
			lambda val: str(val),
		),

		list: (
			4,
			lambda val: json.dumps(val),
		),
		dict: (
			4,
			lambda val: json.dumps(val),
		),
		tuple: (
			4,
			lambda val: json.dumps(val),
		),
	}

	KEYTYPE_MAP_FROMDB = {
		# bool:   0,
		# str:    1,
		# int:    2,
		# float:  3,

		# list:   4,
		# dict:   4,
		# tuple:  4,


		0: lambda val: bool(val),
		1: lambda val: str(val),
		2: lambda val: int(val),
		3: lambda val: float(val),

		4: lambda val: json.loads(val),
		4: lambda val: json.loads(val),
		4: lambda val: json.loads(val),
	}

	def __init__(self, db_con, table_id):
		self.db_con = db_con
		self.table_id = table_id

	def stage_key(self, kname, kval):
		if not type(kval) in self.KEYTYPE_MAP_TODB:
			raise ValueError(
				f"""Key of type {type(kval)} is not accepted."""
			)

		ktype, converter = self.KEYTYPE_MAP_TODB[type(kval)]

		self.db_con.exec(
			f"""
				INSERT INTO {self.table_id} (key_id, key_type, key_val)
				VALUES (:key_id, :key_type, :key_val)
			""",
			{
				'key_id':   kname,
				'key_type': ktype,
				'key_val':  converter(kval),
			}
		)

	def __getitem__(self, kname):
		self.db_con.exec(
			f'SELECT * FROM {self.table_id} WHERE key_id = :key_id',
			{
				'key_id': kname,
			}
		)
		key_data = self.db_con.fetchone()

		if not key_data:
			return None

		_, key_type, key_val = key_data
		return self.KEYTYPE_MAP_FROMDB[key_type](key_val)

	def __setitem__(self, kname, kval):
		self.stage_key(kname, kval)
		self.db_con.commit()

	def __iter__(self):
		self.db_con.exec(
			f"""SELECT * FROM {self.table_id};"""
		)

		# table_contents = {}
		for kname, ktype, kval in self.db_con.fetchall():
			# table_contents[kname] = kval
			yield kname, self.KEYTYPE_MAP_FROMDB[ktype](kval)

		# return table_contents

	def apply(self, data_dict):
		for k, v in data_dict.items():
			self.stage_key(k, v)
		self.db_con.commit()


class BasicKVStorageTables:
	def __init__(self, db_con):
		self.db_con = db_con

	def create(self, table_id, exist_ok=True):
		self.db_con.exec(f'''
			CREATE TABLE IF NOT EXISTS {table_id} (
				key_id TEXT NOT NULL UNIQUE ON CONFLICT REPLACE,
				key_type INT NOT NULL,
				key_val TEXT
			)
		''')
		self.db_con.commit()

		return BasicKVStorageTableInstance(
			self.db_con,
			table_id
		)

	def __getitem__(self, table_id):
		self.db_con.exec(
			"""SELECT name FROM sqlite_master WHERE type='table' AND name=?""",
			(table_id,)
		)
		if not self.db_con.fetchone():
			# raise ValueError(
			# 	f"""Group {table_id} doesn't exist."""
			# )
			return None

		return BasicKVStorageTableInstance(
			self.db_con,
			table_id
		)


class BasicKVStorage:
	"""
		SQLite database file storing key:value items.
		Retarded, but good for preserving integrity n shit.
		+------------+----------+---------+
		| key_id     | key_type | key_val |
		===================================
		| fuck       |    0     |    1    |
		+------------+----------+---------+
		| fuck.shit  |    2     |  1337   |
		+------------+----------+---------+

		- key_id(SQL STRING)
		  The name of the key. Always unique.

		- key_type(SQL INT)
		  The type of the stored key. Evaluated when the key is retreived.
		  Types are:
		      - 0: Boolean.
		      - 1: String.
		      - 2: Integer.
		      - 3: Floating point number.
		      - 4: JSON String.

		- key_val(SQL STRING)
		  The key's value. Can be null.
	"""

	def __init__(self, db_filepath):
		# todo: Is Path() needed?
		self.db_filepath = Path(db_filepath)
		self._db_con = None
		self._tables = None

		self._default_table = None

	@property
	def db_con(self):
		if self._db_con:
			return self._db_con

		self._db_con = BasicDBConnection(self.db_filepath)
		return self._db_con

	@property
	def tables(self):
		if self._tables:
			return self._tables

		self._tables = BasicKVStorageTables(self.db_con)

		return self._tables

	@property
	def groups(self):
		return self.tables

	@property
	def default_table(self):
		if self._default_table:
			return self._default_table

		table = self.tables['main']

		if not table:
			self.tables.create('main')
			table = self.tables['main']

		self._default_table = table

		return self._default_table

	def __getitem__(self, key_id):
		self.default_table[key_id]

	def __setitem__(self, key_id, key_val):
		self.default_table[key_id] = key_val

	def __iter__(self):
		# todo: But what about list() ?
		for i in self.default_table:
			yield i

	def apply(self, dict_data):
		self.default_table.apply(dict_data)


















def test_BasicKVStorage():
	devtitle('BasicKVStorage')

	SAMPLE_DB = DEVDIR / 'sample_basic_kv.db'
	SAMPLE_DB.unlink(missing_ok=True)
	basic_cfg = BasicKVStorage(
		SAMPLE_DB
	)

	print('Empty init:')
	dict_prety_print(dict(basic_cfg))

	basic_cfg['sex'] = 33

	devsep()
	print('Setting sex to 33:')
	dict_prety_print(dict(basic_cfg))

	basic_cfg.apply({
		'fuck': 'shit',
		'ded': ['a', 'b', 'c'],
		'nen': 0.6776,
		'b': True,
	})

	devsep()
	print('Mass apply:')
	dict_prety_print(dict(basic_cfg))

	basic_cfg['sex'] = 222222

	devsep()
	print('Updating sex as a single param:')
	dict_prety_print(dict(basic_cfg))

if __name__ == '__main__':
	devtitle('TESTING')
	devsep()
	test_BasicKVStorage()
	devsep()
	devtitle('DONE')



