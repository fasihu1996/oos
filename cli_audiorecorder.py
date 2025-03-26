import urllib.request, certifi, ssl, os, datetime as dt, sqlite3
from docopt import docopt

def recorder(url, filename, duration, blocksize):
    """Record audio stream from the given URL."""
    print(f"Recording from {url} to {filename}.mp3 for {duration} seconds with blocksize {blocksize}")
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    stream = urllib.request.urlopen(url, context=ssl_context)
    start_time = dt.datetime.now()
    blocks_target = int(duration) * 16000 / int(blocksize)
    blocks_written = 0

    with open(f"{filename}.mp3", 'wb') as f:
        while blocks_written < blocks_target:
            f.write(stream.read(int(blocksize)))
            blocks_written += 1


    conn = sqlite3.connect('recordings.db')
    c = conn.cursor()
    current_time = start_time.time().strftime("%H:%M:%S")

    c.execute('''CREATE TABLE IF NOT EXISTS recordings
                 (identifier INTEGER PRIMARY KEY, url TEXT, filename TEXT, date TEXT, time TEXT, duration INTEGER)''')
    c.execute("INSERT INTO recordings (url, filename, date, time, duration) VALUES (?, ?, ?, ?, ?)",
              (url, filename, start_time.date().isoformat(), current_time, duration))
    conn.commit()
    print("\nRecording successfully saved and logged in database.\n")
    list_recordings()
    conn.close()

def list_recordings():
    """List all recordings from the database."""
    conn = sqlite3.connect('recordings.db')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM recordings")
    count = c.fetchone()
    if count == 0:
        print("No recordings found!")
    else:
        c.execute("SELECT * FROM recordings")
        rows = c.fetchall()
        print(f"{'IDs':3}{'Title':>20}   {'URL':<60}{'Date':>15}{'Timestamp':>15}{'Length':>10}")
        for row in rows:
            identifier, url, title, date, time, duration = row
            print(f"{identifier:3}{title:>20}   {url:<60}{date:>15}{time:>15}{duration:>10}")
    conn.close()

def clear_database():
    """Clears all entries from the database"""
    if os.path.isfile('recordings.db'):
        conn = sqlite3.connect('recordings.db')
        c = conn.cursor()
        c.execute("DELETE FROM recordings")
        conn.commit()
        conn.close()
        return "The database has been cleared"
    else:
        return "The database does not exist yet"

def main():
    """Main entry point for the script."""
    doc = """Audiorecorder

    Usage:
      cli_audiorecorder.py <url> [--filename=<name>] [--duration=<time>] [--blocksize=<size>]
      cli_audiorecorder.py -l | --list
      cli_audiorecorder.py -h | --help
      cli_audiorecorder.py -c | --clear

    Options:
      -h --help             Show this screen.
      --filename=<name>     Name of recording [default: myRadio].
      --duration=<time>     Duration of recording in seconds [default: 30].
      --blocksize=<size>    Block size for read/write in bytes [default: 64].
      -l --list             List all recordings.
      -c --clear            Clear the database.
    """
    arguments = docopt(doc)

    if arguments['--list']:
        list_recordings()
    elif arguments['--clear']:
        print(clear_database())
    else:
        url = arguments['<url>']
        filename = arguments['--filename']
        duration = arguments['--duration']
        blocksize = arguments['--blocksize']
        recorder(url, filename, duration, blocksize)

if __name__ == '__main__':
    main()
