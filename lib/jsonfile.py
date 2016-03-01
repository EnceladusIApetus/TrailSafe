import json

global f, paths

f = None
paths = None

def new_file(path):
	global f, paths
	f = open(path, 'w')
	paths = path

def open_file(path):
	global f, paths

	try:
		f = open(path, 'r')
		paths = path
		return True
	except:
		return False

def read():
	global f

	try:
		x = json.load(f)
		reopen()
		return x
	except:
		return None

def update(obj):
	x = read()

	if x is not None:
		x.update(obj)
	else:
		x = obj

	write(x)

def reopen():
	global f, paths
	f.close()
	f = open(paths, 'r')

def write(obj):
	global f
	f = open(paths, 'w')
	json.dump(obj, f, sort_keys=True, indent=2)
	f.close()
	reopen()

def delete(key):
	x = read()
	del x[key]
	write(x)