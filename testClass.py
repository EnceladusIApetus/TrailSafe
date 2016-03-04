from lib import jsonfile

x = jsonfile.JSONFile()
x.open_file("C:\\msys64\\home\\Pakin\\TrailSafe\\config\\config.ini")
x = x.read()
print x