import json

class JSONFile:

	def __init__(self):
		self.f = None
		self.paths = None

	def new_file(self, path):
		self.f = open(path, 'w')
		self.paths = path

	def open_file(self, path):
		try:
			self.f = open(path, 'r')
			self.paths = path
			return True
		except:
			return False

	def read(self):
		try:
			x = json.load(self.f)
			self.reopen()
			return x
		except:
			return None

	def update(self, obj):
		x = self.read()

		if x is not None:
			x.update(obj)
		else:
			x = obj

		self.write(x)

	def reopen(self):
		self.f.close()
		self.f = open(self.paths, 'r')

	def write(self, obj):
		self.f = open(self.paths, 'w')
		json.dump(obj, self.f, sort_keys=True, indent=2)
		self.f.close()
		self.reopen()

	def delete(self, key):
		x = self.read()
		del x[key]
		self.write(x)