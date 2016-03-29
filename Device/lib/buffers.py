import jsonfile, json

def get_all_data():
    reader = jsonfile.JSONFile()
    reader.open_file('/home/pi/TrailSafe/Device/temp_data/buffer.data')
    return reader.read()

def dequeue():
    try:
        writer = jsonfile.JSONFile()
        writer.open_file('/home/pi/TrailSafe/Device/temp_data/buffer.data')
        buffers = get_all_data()
        data = buffers['buffer'].pop()
        writer.write(buffers)
        return dict(data)
    except:
        return None

def queue(data):
    writer = jsonfile.JSONFile()
    writer.open_file('/home/pi/TrailSafe/Device/temp_data/buffer.data')
    buffers = get_all_data()
    buffers['buffer'].append(data)
    writer.write(buffers)
    
