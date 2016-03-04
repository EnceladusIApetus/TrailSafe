import json

class JSONFile():
	f = None
	paths = None

	def new_file(self, path):
		global f, paths
		f = open(path, 'w')
		paths = path

	def open_file(self, path):
		global f, paths
		try:
			f = open(path, 'r')
			paths = path
			return True
		except:
			return False

	def read(self):
		global f;
		try:
			x = json.load(f)
			self.reopen()
			return x
		except:
			return None

	def update(self, obj):
		x = read()

		if x is not None:
			x.update(obj)
		else:
			x = obj

		write(x)

	def reopen(self):
		global f, paths
		f.close()
		f = open(paths, 'r')

	def write(self, obj):
		global f
		f = open(paths, 'w')
		json.dump(obj, f, sort_keys=True, indent=2)
		f.close()
		reopen()

	def delete(self, key):
		x = read()
		del x[key]
		write(x)