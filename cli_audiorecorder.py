import urllib.request
import datetime
import sys

def recorder(url, filename, duration, blocksize):
    """shows this help"""
    print(arguments)
    stream = urllib.request.urlopen(url)
    start_time = datetime.datetime.now()

    f = open(f"{filename}.mp3", 'wb')

    while (datetime.datetime.now() - start_time).seconds < (duration - 3):
        data = stream.read(blocksize)
        f.write(data)
        if (datetime.datetime.now() - start_time).seconds >= (duration - 3):
            break

arguments = sys.argv[1:]
url, filename, duration, blocksize = arguments
duration = int(duration)
blocksize = int(blocksize)
recorder(url,filename, duration, blocksize)
