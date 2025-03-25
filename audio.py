import urllib.request
import datetime as dt
import sys
import sqlite3
from docopt import docopt

def recorder(url, filename, duration, blocksize):
    """Record audio stream from the given URL."""
    print(f"Recording from {url} to {filename}.mp3 for {duration} seconds with blocksize {blocksize}")
    stream = urllib.request.urlopen(url)
    start_time = dt.datetime.now()

    with open(f"{filename}.mp3", 'wb') as f:
        while (dt.datetime.now() - start_time).seconds < int(duration):
            f.write(stream.read(int(blocksize)))

    # Save metadata to database
    conn = sqlite3.connect('recordings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS recordings
                 (url TEXT, filename TEXT, date TEXT, time TEXT, duration INTEGER)''')
    c.execute("INSERT INTO recordings (url, filename, date, time, duration) VALUES (?, ?, ?, ?, ?)",
              (url, filename, start_time.date(), start_time.time(), duration))
    conn.commit()
    res = c.execute("SELECT * FROM recordings")
    print(res.fetchall())
    conn.close()

def list_recordings():
    """List all recordings from the database."""
    conn = sqlite3.connect('recordings.db')
    c = conn.cursor()
    c.execute("SELECT * FROM recordings")
    rows = c.fetchall()
    for row in rows:
        print(row)
    conn.close()

def main():
    """Main entry point for the script."""
    doc = """Audiorecorder

    Usage:
      cli_audiorecorder.py <url> [--filename=<name>] [--duration=<time>] [--blocksize=<size>]
      cli_audiorecorder.py -l | --list
      cli_audiorecorder.py -h | --help

    Options:
      -h --help             Show this screen.
      --filename=<name>     Name of recording [default: myRadio].
      --duration=<time>     Duration of recording in seconds [default: 30].
      --blocksize=<size>    Block size for read/write in bytes [default: 64].
      -l --list             List all recordings.
    """
    arguments = docopt(doc)

    if arguments['--list']:
        list_recordings()
    else:
        url = arguments['<url>']
        filename = arguments['--filename']
        duration = arguments['--duration']
        blocksize = arguments['--blocksize']
        recorder(url, filename, duration, blocksize)

if __name__ == '__main__':
    main()
